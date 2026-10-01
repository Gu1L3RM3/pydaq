import sys
import os
import ast
import serial
import serial.tools.list_ports
import warnings
from pathlib import Path
import numpy as np

from PySide6 import QtWidgets
from PySide6.QtWidgets import (
    QFileDialog,
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMenu,
    QLabel
)
from PySide6.QtGui import *
from PySide6.QtCore import *

from pydaq.utils.base import Base
from pydaq.legacy_qt.widgets import ClickableLineEdit
from .error_window_gui import Error_window

from ..uis.ui_PyDAQ_data_driven_control_Arduino_widget import Ui_Arduino_Data_Driven_Control
from ..guis.data_driven_control_window_dialog import Data_Driven_Control_Window_Dialog
from pydaq.data_driven_control import DataDrivenControl

def parse_vector_text(text, field_name):
    """
    Parse vector text from UI.

    Example:
        "[0,0,0,0.1548]" -> np.array([0.0, 0.0, 0.0, 0.1548])

    Coefficients are interpreted in q^-1.
    """

    text = text.strip()

    if not text:
        raise ValueError(f"[PYDAQ] {field_name} cannot be empty.")

    try:
        value = ast.literal_eval(text)
    except Exception as exc:
        raise ValueError(
            f"[PYDAQ] Invalid vector format for {field_name}. "
            f"Use list format, for example: [1,-1.213,0.3679]."
        ) from exc

    vector = np.asarray(value, dtype=float).flatten()

    if vector.size == 0:
        raise ValueError(f"[PYDAQ] {field_name} cannot be empty.")

    return vector


def load_vector_file(path, field_name):
    """Load a one-dimensional NCbT vector from a PyDAQ .dat file."""
    path = path.strip()
    if not path:
        raise ValueError(f"[PYDAQ] File path for {field_name} cannot be empty.")
    file_path = Path(path)
    if file_path.suffix.lower() != ".dat":
        raise ValueError(f"[PYDAQ] Invalid file for {field_name}. Only PyDAQ .dat files are supported.")
    if not file_path.is_file():
        raise ValueError(f"[PYDAQ] File not found for {field_name}: {path}")
    try:
        data = np.loadtxt(file_path, delimiter=",")
    except ValueError:
        data = np.loadtxt(file_path)
    data = np.asarray(data, dtype=float).flatten()
    if data.size == 0:
        raise ValueError(f"[PYDAQ] The {field_name} .dat file is empty.")
    if not np.all(np.isfinite(data)):
        raise ValueError(f"[PYDAQ] The {field_name} .dat file contains invalid values.")
    return data

from .ddc_matrix_inputs import install_matrix_inputs

class Data_Driven_Control_Arduino_Widget(QWidget, Ui_Arduino_Data_Driven_Control):
    """
    Arduino widget for PYDAQ Data-Driven Control using NCbT.

    This widget is based on PID_Control_Arduino_Widget, but replaces the PID
    gain configuration by the NCbT configuration.

    In NCbT:
        beta defines the controller structure.
        rho is computed by pyncbt.
        C(q) = sum_i rhoq
    """

    def __init__(self, *args):
        super(Data_Driven_Control_Arduino_Widget, self).__init__()
        self.setupUi(self)
        install_matrix_inputs(self, [('lineEdit_numerator','vector'),('lineEdit_denominator','vector'),('plainTextEdit_beta','beta'),('lineEdit_num_M','vector'),('lineEdit_den_M','vector')])

        # Hide old equation/image preview for now.
        if hasattr(self, "frame_equation"):
            self.frame_equation.hide()

        # r is optional and only used by NCbT_closed.
        if hasattr(self, "lineEdit_r_data_path"):
            self.lineEdit_r_data_path.setPlaceholderText(
                "only for NCbT closed loop"
        )

        # Calling the functions
        self.update_com_ports()
        self.setWindowTitle("PYDAQ - Data-Driven Control Arduino")

        self.reload_devices.clicked.connect(self.update_com_ports)

        self.on_unit_change()
        self.comboBox_setpoint.currentIndexChanged.connect(self.on_unit_change)

        self.simulate_radio_group.buttonClicked.connect(self.on_simulate_change)
        self.on_simulate_change()

        self.pushButton_confirm.released.connect(self.confirm_parameters)
        self.pushButton_start.clicked.connect(self.show_graph_window)

        self.path_folder_browse.released.connect(self.locate_path)

        # Optional NCbT data browse buttons.
        # These widgets must be created in the new .ui file.
        if hasattr(self, "pushButton_load_u"):
            self.pushButton_load_u.clicked.connect(self.locate_u_file)

        if hasattr(self, "pushButton_load_y"):
            self.pushButton_load_y.clicked.connect(self.locate_y_file)

        if hasattr(self, "pushButton_load_r"):
            self.pushButton_load_r.clicked.connect(self.locate_r_file)

        if hasattr(self, "pushButton_load_t"):
            self.pushButton_load_t.clicked.connect(self.locate_t_file)

        # Setting the starting values for some widgets
        self.path_line_edit.setText(
            os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
        )

        # NCbT parameters
        self.beta = None
        self.rho = None
        self.num_M = None
        self.den_M = None
        self.l = 20

        self.u_data_path = ""
        self.y_data_path = ""
        self.r_data_path = ""
        self.t_data_path = ""

        self._set_default_ncbt_fields()

        # Available channels - Arduino logic
        self.available_ai_channels = [f"A{i}" for i in range(6)]
        self.available_ao_channels = [f"D{i}" for i in range(0, 14)]

        # Updating combo boxes for single channel selection
        self.ai_channel_combo.clear()
        self.ao_channel_combo.clear()
        self.ai_channel_combo.addItems(self.available_ai_channels)
        self.ao_channel_combo.addItems(self.available_ao_channels)

    def _set_default_ncbt_fields(self):
        """
        Fill default NCbT fields if they exist in the UI.

        The beta shown here is only a starting example. In practice, beta is
        a user-defined controller structure and must be validated before
        starting the control dialog.
        """

        if hasattr(self, "plainTextEdit_beta"):
            self.plainTextEdit_beta.setPlainText(
                "[\n"
                "    ([1], [1, -1]),\n"
                "    ([0, 1], [1, -1]),\n"
                "    ([0, 0, 1], [1, -1]),\n"
                "    ([0, 0, 0, 1], [1, -1]),\n"
                "    ([0, 0, 0, 0, 1], [1, -1]),\n"
                "    ([0, 0, 0, 0, 0, 1], [1, -1])\n"
                "]"
            )

        if hasattr(self, "lineEdit_num_M"):
            self.lineEdit_num_M.setText("[0, 0, 0, 1]")

        if hasattr(self, "lineEdit_den_M"):
            self.lineEdit_den_M.setText("[1, -1.2, 0.4]")

        if hasattr(self, "spinBox_l"):
            self.spinBox_l.setValue(20)

    def update_com_ports(self):
        """Update COM ports and store the real device in itemData."""

        selected_device = self.comboBox_arduino.currentData()
        ports = list(serial.tools.list_ports.comports())

        self.comboBox_arduino.blockSignals(True)
        self.comboBox_arduino.clear()
        self.com_ports = []

        for port in ports:
            description = port.description or "Serial device"
            display_text = f"{port.device} - {description}"
            self.comboBox_arduino.addItem(display_text, port.device)
            self.com_ports.append(port.device)

        if selected_device:
            index_current = self.comboBox_arduino.findData(selected_device)
            if index_current >= 0:
                self.comboBox_arduino.setCurrentIndex(index_current)

        self.comboBox_arduino.blockSignals(False)

    def on_unit_change(self):
        """
        Show or hide calibration/unit widgets depending on selected unit.
        """

        selected_unit = self.comboBox_setpoint.currentText()

        if selected_unit == 'Other':
            self.widget_unit.show()
            self.label_unit.show()
            self.label_equation.show()
            self.widget_equation.show()
            self.label_i_equation.show()

        elif selected_unit == 'Voltage (V)':
            self.widget_unit.hide()
            self.label_unit.hide()
            self.label_equation.hide()
            self.widget_equation.hide()
            self.label_i_equation.hide()

        else:
            self.widget_unit.hide()
            self.label_unit.hide()
            self.label_equation.show()
            self.widget_equation.show()
            self.label_i_equation.show()

    def on_simulate_change(self):
        """
        Switch interface between simulation mode and Arduino hardware mode.
        """

        self.simulate = True if self.simulate_radio_group.checkedId() == -2 else False

        if self.simulate is False:
            self.widget_arduino.show()
            self.label_arduino.show()

            self.widget_polynomial.hide()
            self.label_system_equation.hide()
            self.label_i_polinomial.hide()

            self.ai_channel_combo.show()
            self.ao_channel_combo.show()
            self.label_ai_channel.show()
            self.label_ao_channel.show()
            self.widget_ai_channel.show()
            self.widget_ao_channel.show()

        elif self.simulate is True:
            self.widget_arduino.hide()
            self.label_arduino.hide()

            self.widget_polynomial.show()
            self.label_system_equation.show()
            self.label_i_polinomial.show()

            self.ai_channel_combo.hide()
            self.ao_channel_combo.hide()
            self.label_ai_channel.hide()
            self.label_ao_channel.hide()
            self.widget_ai_channel.hide()
            self.widget_ao_channel.hide()

    def confirm_parameters(self):
        """
        Carrega os dados, executa NCbT (open ou closed) e exibe rho.
        """
        try:
            # Lê parâmetros da UI
            self.beta = self.read_beta_from_ui()
            self.num_M = self.read_num_M_from_ui()
            self.den_M = self.read_den_M_from_ui()
            self.l = self.read_l_from_ui()

            self.numerator = self.lineEdit_numerator.text().strip()
            self.denominator = self.lineEdit_denominator.text().strip()
            self.setpoint = self.doubleSpinBox_setpoint.value()
            self.period = self.doubleSpinBox_period.value()
            self.equationvu = self.lineEdit_equationvu.text().strip()
            self.equationuv = self.lineEdit_equationuv.text().strip()
            self.getunit()

            # Caminhos dos arquivos
            u_path = self.lineEdit_u_data_path.text().strip()
            y_path = self.lineEdit_y_data_path.text().strip()
            r_path = self.lineEdit_r_data_path.text().strip() if hasattr(self, "lineEdit_r_data_path") else ""
            t_path = self.lineEdit_t_data_path.text().strip() if hasattr(self, "lineEdit_t_data_path") else ""

            # Validação obrigatória: u e y
            if not u_path or not y_path:
                raise ValueError("Missing u or y data files. Both are required for NCbT.")

            # Carrega os arquivos com tratamento de erro individual
            try:
                u = load_vector_file(u_path, "u")
            except Exception as e:
                raise ValueError(f"Failed to load u file '{u_path}': {e}")

            try:
                y = load_vector_file(y_path, "y")
            except Exception as e:
                raise ValueError(f"Failed to load y file '{y_path}': {e}")

            # t é opcional
            if t_path:
                try:
                    t = load_vector_file(t_path, "t")
                except Exception as e:
                    raise ValueError(f"Failed to load t file '{t_path}': {e}")
            else:
                t = None

            # Cria controlador sem rho (será estimado)
            ddc = DataDrivenControl(
                rho=None,
                beta=self.beta,
                setpoint=self.setpoint,
                numerator=self.numerator,
                denominator=self.denominator,
                calibration_equation_vu=self.equationvu,
                calibration_equation_uv=self.equationuv,
                unit=self.unit,
                period=self.period
            )

            # Decide modo com base na existência de r
            if r_path:
                try:
                    r = load_vector_file(r_path, "r")
                except Exception as e:
                    raise ValueError(f"Failed to load r file '{r_path}': {e}")

                # Valida tamanhos
                if len(u) != len(y) or len(u) != len(r) or (t is not None and len(u) != len(t)):
                    raise ValueError("u, y, r and t (if provided) must have the same length.")

                rho = ddc.tune_ncbt_closed_loop(
                    u=u, y=y, r=r,
                    num_M=self.num_M, den_M=self.den_M,
                    Ts=self.period, t=t, l=self.l, beta=self.beta
                )
                mode_text = "NCbT mode: Closed-loop"
                call_text = f"NCbT_closed(u, y, r, num_M, den_M, Ts={self.period}, l={self.l})"
            else:
                # Modo open-loop (r não fornecido)
                if t is not None and len(u) != len(t):
                    raise ValueError("u, y and t must have the same length.")

                rho = ddc.tune_ncbt_open_loop(
                    u=u, y=y,
                    num_M=self.num_M, den_M=self.den_M,
                    Ts=self.period, t=t, l=self.l, beta=self.beta
                )
                mode_text = "NCbT mode: Open-loop"
                call_text = f"NCbT_open(u, y, num_M, den_M, Ts={self.period}, l={self.l})"

            self.ddc = ddc
            self.rho = rho

            # Monta texto para exibir
            rho_display = f"{mode_text}\nUsing: {call_text}\n\nEstimated rho:\n"
            for i, val in enumerate(rho):
                rho_display += f"rho[{i}] = {val:.10g}\n"
            self.plainTextEdit_rho.setPlainText(rho_display)

            # Opcional: mostrar mensagem de sucesso (pode ser via status bar)
            print("[PYDAQ] Controller estimated successfully.")

        except Exception as e:
            err_msg = f"[PYDAQ] Error estimating data-driven controller:\n{str(e)}"
            warnings.warn(err_msg)
            error_w = Error_window()
            error_w.ui.confirm.setText(err_msg)
            error_w.exec()

    def show_controller_structure(self):
        """
        Show the NCbT controller structure.

        Before the NCbT estimation, rho is unknown. Therefore, the displayed
        expression is symbolic:

            C(q) = rhoq + rhoq + ...

        After running pyncbt, rho will be available in the control dialog.
        """

        try:
            beta = self.read_beta_from_ui()

        except Exception as e:
            warnings.warn(str(e))

            error_w = Error_window()
            error_w.ui.confirm.setText(
                "Invalid beta structure. Please check the controller basis."
            )
            error_w.exec()
            return

        text = "C(q) = "

        equation_parts = []

        for i in range(len(beta)):
            equation_parts.append(f"rhoq")

        text += " + ".join(equation_parts)
        text += "\n\nUser-defined beta:\n"

        for i, basis in enumerate(beta):
            num, den = basis
            text += f"\nbetaq:\n"
            text += f"  numerator   = {num}\n"
            text += f"  denominator = {den}\n"

        label = QLabel(text)
        label.setStyleSheet(
            "QLabel {"
            "background-color: #404040;"
            "color: white;"
            "font-family: Consolas;"
            "font-size: 11px;"
            "padding: 10px;"
            "}"
        )
        label.setWordWrap(True)

        # Remove previous equation/image widgets
        for i in reversed(range(self.image_layout.count())):
            widget_to_remove = self.image_layout.itemAt(i).widget()
            self.image_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        self.image_layout.addWidget(label)

    def show_graph_window(self):
        """
        Abre a janela de execução.
        Se rho ainda não foi estimado, a janela fará a coleta automática.
        """
        # 1. Validação do caminho
        if self.yes_save_radio.isChecked() and self.path_line_edit.text() == "":
            raise ValueError("Missing configuration: Empty save path.")
        self.path = self.path_line_edit.text()

        # 2. Lê parâmetros gerais da UI
        self.setpoint = self.doubleSpinBox_setpoint.value()
        self.getunit()
        self.equationvu = self.lineEdit_equationvu.text()
        self.equationuv = self.lineEdit_equationuv.text()
        self.period = self.doubleSpinBox_period.value()
        self.numerator = self.lineEdit_numerator.text()
        self.denominator = self.lineEdit_denominator.text()
        self.save = self.yes_save_radio.isChecked()
        self.simulate = self.yes_simulate_radio.isChecked()

        # 3. Lê os parâmetros NCbT diretamente da UI (NOVO)
        self.beta = self.read_beta_from_ui()
        self.num_M = self.read_num_M_from_ui()
        self.den_M = self.read_den_M_from_ui()
        self.l = self.read_l_from_ui()

        # (Opcional: prints para depuração)
        print(f"[DEBUG] beta = {self.beta}")
        print(f"[DEBUG] num_M = {self.num_M}")
        print(f"[DEBUG] den_M = {self.den_M}")
        print(f"[DEBUG] l = {self.l}")

        # 4. Configuração do hardware (Arduino)
        if self.simulate:
            self.channels = [" "]
            self.ao_channels = [" "]
            self.com_port = None
        else:
            self.channels = [self.ai_channel_combo.currentText()]
            self.ao_channels = [self.ao_channel_combo.currentText()]
            if not self.channels[0] or not self.ao_channels[0]:
                raise ValueError("Invalid channels.")
            self.com_port = self.comboBox_arduino.currentData()
            if not self.com_port:
                raise ValueError(
                    "No valid serial port is selected. Connect the Arduino "
                    "and click the reload button."
                )

        self.board = 'arduino'

        # 5. Cria a janela de controle
        plot_window = Data_Driven_Control_Window_Dialog(self)
        plot_window.check_board(
            self.board,
            self.com_port,
            self.ao_channels,
            self.channels,
            None,
            self.simulate
        )

        # 6. Passa todos os parâmetros (incluindo os NCbT lidos)
        plot_window.set_parameters(
            rho=None,                      # ativa coleta automática
            beta=self.beta,
            numerator=self.numerator,
            denominator=self.denominator,
            setpoint=self.setpoint,
            unit=self.unit,
            equationvu=self.equationvu,
            equationuv=self.equationuv,
            period=self.period,
            path=self.path,
            save=self.save,
            u_data_path=None,
            y_data_path=None,
            r_data_path=None,
            t_data_path=None,
            num_M=self.num_M,
            den_M=self.den_M,
            l=self.l
        )
        plot_window.send_values.connect(self.update_values)
        plot_window.exec()

    def locate_path(self):
        """
        Open folder browser to choose where data will be saved.
        """

        output_folder_path = QFileDialog.getExistingDirectory(
            self,
            caption="Choose a folder to save the data file"
        )

        if output_folder_path == "":
            pass
        else:
            self.path_line_edit.setText(output_folder_path.replace("/", "\\"))

    def locate_u_file(self):
        """
        Select u data file.
        """

        path = self.locate_data_file("Choose u data file")

        if path and hasattr(self, "lineEdit_u_data_path"):
            self.lineEdit_u_data_path.setText(path)

    def locate_y_file(self):
        """
        Select y data file.
        """

        path = self.locate_data_file("Choose y data file")

        if path and hasattr(self, "lineEdit_y_data_path"):
            self.lineEdit_y_data_path.setText(path)

    def locate_r_file(self):
        """
        Select r data file.
        """

        path = self.locate_data_file("Choose r data file")

        if path and hasattr(self, "lineEdit_r_data_path"):
            self.lineEdit_r_data_path.setText(path)

    def locate_t_file(self):
        """
        Select optional time data file.
        """

        path = self.locate_data_file("Choose time data file")

        if path and hasattr(self, "lineEdit_t_data_path"):
            self.lineEdit_t_data_path.setText(path)

    def locate_data_file(self, caption):
        """
        Select a data file for NCbT.

        The actual loading is performed later in the control dialog.
        """

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            caption,
            self.path_line_edit.text(),
            "PyDAQ data files (*.dat)"
        )

        return file_path

    def update_values(self, rho_text, setpoint):
        """
        Update widget values from the control dialog.

        For PID, this function updated Kp, Ki and Kd.
        For NCbT, the main returned parameter is rho.
        """

        if hasattr(self, "plainTextEdit_rho"):
            self.plainTextEdit_rho.setPlainText(rho_text)

        self.doubleSpinBox_setpoint.setValue(setpoint)

    def getunit(self):
        """
        Get selected measurement/control unit.
        """

        if self.comboBox_setpoint.currentIndex() != 2:
            self.unit = self.comboBox_setpoint.currentText()
        else:
            self.unit = self.lineEdit_unit.text()

    def read_beta_from_ui(self):
        """
        Read beta from the UI.

        beta must be a Python literal list, for example:

            [
                ([1], [1, -1]),
                ([0, 1], [1, -1])
            ]

        ast.literal_eval is used instead of eval.
        """

        if not hasattr(self, "plainTextEdit_beta"):
            raise ValueError("[PYDAQ] Beta field not found in UI.")

        text = self.plainTextEdit_beta.toPlainText().strip()

        if text == "":
            raise ValueError("[PYDAQ] beta cannot be empty.")

        try:
            beta = ast.literal_eval(text)

        except Exception as e:
            raise ValueError(f"[PYDAQ] Error parsing beta: {e}")

        self.validate_beta(beta)

        return beta

    def read_num_M_from_ui(self):
        """
        Read reference model numerator from UI.
        """

        if not hasattr(self, "lineEdit_num_M"):
            raise ValueError("[PYDAQ] num_M field not found in UI.")

        text = self.lineEdit_num_M.text().strip()

        if text == "":
            raise ValueError("[PYDAQ] num_M cannot be empty.")

        try:
            return np.asarray(ast.literal_eval(text), dtype=float).flatten()

        except Exception as e:
            raise ValueError(f"[PYDAQ] Error parsing num_M: {e}")

    def read_den_M_from_ui(self):
        """
        Read reference model denominator from UI.
        """

        if not hasattr(self, "lineEdit_den_M"):
            raise ValueError("[PYDAQ] den_M field not found in UI.")

        text = self.lineEdit_den_M.text().strip()

        if text == "":
            raise ValueError("[PYDAQ] den_M cannot be empty.")

        try:
            den_M = np.asarray(ast.literal_eval(text), dtype=float).flatten()

        except Exception as e:
            raise ValueError(f"[PYDAQ] Error parsing den_M: {e}")

        if len(den_M) == 0 or np.isclose(den_M[0], 0.0):
            raise ValueError("[PYDAQ] Invalid den_M.")

        return den_M

    def read_l_from_ui(self):
        """
        Read NCbT instrument length/order l.
        """

        if hasattr(self, "spinBox_l"):
            return int(self.spinBox_l.value())

        return 20

    def read_line_if_exists(self, widget_name):
        """
        Read text from a QLineEdit if it exists.
        """

        if hasattr(self, widget_name):
            return getattr(self, widget_name).text().strip()

        return ""

    def validate_beta(self, beta):
        """
        Validate beta format.

        Expected format:

            beta = [
                ([num_0], [den_0]),
                ([num_1], [den_1]),
                ...
            ]
        """

        if beta is None:
            raise ValueError("[PYDAQ] beta must be provided.")

        if not isinstance(beta, list):
            raise ValueError("[PYDAQ] beta must be a list.")

        if len(beta) == 0:
            raise ValueError("[PYDAQ] beta cannot be empty.")

        for i, basis in enumerate(beta):
            if not isinstance(basis, (list, tuple)) or len(basis) != 2:
                raise ValueError(
                    f"[PYDAQ] beta[{i}] must be (numerator, denominator)."
                )

            numerator, denominator = basis

            numerator = np.asarray(numerator, dtype=float).flatten()
            denominator = np.asarray(denominator, dtype=float).flatten()

            if numerator.size == 0:
                raise ValueError(f"[PYDAQ] beta[{i}] numerator cannot be empty.")

            if denominator.size == 0:
                raise ValueError(f"[PYDAQ] beta[{i}] denominator cannot be empty.")

            if np.isclose(denominator[0], 0.0):
                raise ValueError(
                    f"[PYDAQ] beta[{i}] first denominator coefficient cannot be zero."
                )
