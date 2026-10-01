import ast
import os
import numpy as np
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox
from pathlib import Path
from pydaq.utils.base import NIDAQ_AVAILABLE, nidaqmx
from ..uis.ui_PyDAQ_data_driven_control_NIDAQ_widget import Ui_NIDAQ_Data_Driven_Control
from .data_driven_control_nidaq_window_dialog import Data_Driven_Control_NIDAQ_Window_Dialog

from .ddc_matrix_inputs import install_matrix_inputs

class Data_Driven_Control_NIDAQ_Widget(QWidget, Ui_NIDAQ_Data_Driven_Control):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        install_matrix_inputs(self, [('lineEdit_numerator','vector'),('lineEdit_denominator','vector'),('plainTextEdit_beta','beta'),('lineEdit_num_M','vector'),('lineEdit_den_M','vector')])
        self.path_line_edit.setText(os.path.join(os.path.expanduser('~'), 'Desktop'))
        self.terminal_config_combo.clear(); self.terminal_config_combo.addItems(['Diff','RSE','NRSE'])
        self.reload_devices.clicked.connect(self.reload_devices_handler)
        self.device_combo.currentIndexChanged.connect(self.update_channels)
        self.path_folder_browse.clicked.connect(self.locate_path)
        self.pushButton_start.clicked.connect(self.show_graph_window)
        self.pushButton_confirm.clicked.connect(self.confirm_parameters)
        for button_name, field_name in [('pushButton_load_u','lineEdit_u_data_path'),('pushButton_load_y','lineEdit_y_data_path'),('pushButton_load_r','lineEdit_r_data_path'),('pushButton_load_t','lineEdit_t_data_path')]:
            if hasattr(self, button_name) and hasattr(self, field_name):
                getattr(self, button_name).clicked.connect(lambda checked=False, target=field_name: self.locate_data_file(target))
        self.no_save_radio.setChecked(True)
        self.no_simulate_radio.setChecked(True)
        self.reload_devices_handler()

    def _nidaq_info(self):
        self.devices=[]
        if NIDAQ_AVAILABLE:
            self.devices=list(nidaqmx.system.System.local().devices)

    def reload_devices_handler(self):
        old=self.device_combo.currentData(); self._nidaq_info(); self.device_combo.blockSignals(True); self.device_combo.clear()
        for d in self.devices: self.device_combo.addItem(f'{d.product_type} ({d.name})', d.name)
        i=self.device_combo.findData(old)
        if i>=0:self.device_combo.setCurrentIndex(i)
        self.device_combo.blockSignals(False); self.update_channels()

    def update_channels(self):
        self.ai_channel_combo.clear(); self.ao_channel_combo.clear(); name=self.device_combo.currentData()
        if NIDAQ_AVAILABLE and name:
            d=nidaqmx.system.device.Device(name)
            self.ai_channel_combo.addItems(d.ai_physical_chans.channel_names)
            self.ao_channel_combo.addItems(d.ao_physical_chans.channel_names)

    def locate_path(self):
        p=QFileDialog.getExistingDirectory(self,'Choose a folder',self.path_line_edit.text())
        if p:self.path_line_edit.setText(p)

    def locate_data_file(self, target_name):
        path, _ = QFileDialog.getOpenFileName(self, 'Choose PyDAQ data file', self.path_line_edit.text(), 'PyDAQ data files (*.dat)')
        if path:
            getattr(self, target_name).setText(path)

    @staticmethod
    def validate_data_path(path, field_name):
        path = path.strip()
        if not path:
            return
        file_path = Path(path)
        if file_path.suffix.lower() != '.dat':
            raise ValueError(f'Only PyDAQ .dat files are supported for {field_name}.')
        if not file_path.is_file():
            raise ValueError(f'File not found for {field_name}: {path}')

    def _beta(self):
        b=ast.literal_eval(self.plainTextEdit_beta.toPlainText()); return b
    def _vec(self,w,name):
        try:return np.asarray(ast.literal_eval(w.text()),dtype=float).reshape(-1)
        except Exception as exc:raise ValueError(f'Invalid {name}. Use list syntax.') from exc

    def confirm_parameters(self):
        try:
            b=self._beta(); n=self._vec(self.lineEdit_num_M,'num_M'); d=self._vec(self.lineEdit_den_M,'den_M')
            for field, label in [('lineEdit_u_data_path','u'),('lineEdit_y_data_path','y'),('lineEdit_r_data_path','r'),('lineEdit_t_data_path','t')]:
                if hasattr(self, field): self.validate_data_path(getattr(self, field).text(), label)
            self.plainTextEdit_rho.setPlainText(f'beta entries: {len(b)}\nnum_M: {n.tolist()}\nden_M: {d.tolist()}')
        except Exception as exc: QMessageBox.warning(self,'Configuration',str(exc))

    def show_graph_window(self):
        simulate=self.yes_simulate_radio.isChecked()
        if not simulate and (not NIDAQ_AVAILABLE or not self.device_combo.currentData()):
            QMessageBox.warning(self,'NI-DAQ','No NI-DAQ device is available.'); return
        try:
            w=Data_Driven_Control_NIDAQ_Window_Dialog(self)
            w.set_parameters(
                self.device_combo.currentData(), self.ai_channel_combo.currentText(), self.ao_channel_combo.currentText(),
                self.terminal_config_combo.currentText(), self.doubleSpinBox_period.value(), self.doubleSpinBox_setpoint.value(),
                self._beta(), self._vec(self.lineEdit_num_M,'num_M'), self._vec(self.lineEdit_den_M,'den_M'),
                self.spinBox_l.value(), simulate, self.lineEdit_numerator.text(), self.lineEdit_denominator.text(),
                self.path_line_edit.text(), self.yes_save_radio.isChecked())
            w.exec()
        except Exception as exc: QMessageBox.critical(self,'Data-Driven Control NI-DAQ',str(exc))
