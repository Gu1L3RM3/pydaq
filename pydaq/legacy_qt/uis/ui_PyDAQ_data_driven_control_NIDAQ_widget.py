# -*- coding: utf-8 -*-

################################################################################
## Form generated/adapted for PYDAQ Data-Driven Control NI-DAQ widget
##
## Based on PyDAQ_pid_control_NIDAQ_widget.ui structure.
##
## WARNING! All changes made in this file may be lost when recompiling UI file.
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QSize,
    Qt
)

from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget
)


class Ui_NIDAQ_Data_Driven_Control(object):
    def setupUi(self, NIDAQ_Data_Driven_Control):
        if not NIDAQ_Data_Driven_Control.objectName():
            NIDAQ_Data_Driven_Control.setObjectName(
                u"NIDAQ_Data_Driven_Control"
            )

        NIDAQ_Data_Driven_Control.resize(850, 1180)

        NIDAQ_Data_Driven_Control.setStyleSheet(
            u"QWidget{\n"
            "    background-color: rgb(64, 64, 64);\n"
            "    color: rgb(255, 255, 255);\n"
            "    font: 12pt \"Helvetica\";\n"
            "}\n"
            "\n"
            "\n"
            "QComboBox,\n"
            "QLineEdit,\n"
            "QPlainTextEdit,\n"
            "QSpinBox,\n"
            "QDoubleSpinBox{\n"
            "    background-color: rgb(77, 77, 77);\n"
            "    color: rgb(255, 255, 255);\n"
            "    border-top: 1.5px solid rgb(46, 46, 46);\n"
            "    border-left: 1.5px solid rgb(46, 46, 46);\n"
            "    border-bottom: 1.5px solid rgb(166, 166, 166);\n"
            "    border-right: 1.5px solid rgb(166, 166, 166);\n"
            "}\n"
            "\n"
            "QComboBox QAbstractItemView{\n"
            "    background-color: rgb(77, 77, 77);\n"
            "    color: rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton{\n"
            "    background-color: rgb(0, 79, 0);\n"
            "    border-top: 1.5px solid rgb(127, 167, 127);\n"
            "    border-left: 1.5px solid rgb(127, 167, 127);\n"
            "    border-bottom: 1.5px solid rgb(0, 0, 0);\n"
            "    border-right: 1.5px solid rgb(0, 0, 0);\n"
            "    font: 12pt \"Helvetica\";\n"
            "    text-align:center;\n"
            "}\n"
            "\n"
            "QPushButton:hover{\n"
            "    background-color: rgb(0, 50, 0);\n"
            "}\n"
            "\n"
            "QPushButton:pressed{\n"
            "    border: 2px solid rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QPushButton#reload_devices{\n"
            "    image: url(:/imgs/imgs/reload.png);\n"
            "    width: 11px;\n"
            "}\n"
            "\n"
            "QRadioButton::indicator{\n"
            "    border-radius: 6px;\n"
            "    border-top: 1.5px solid rgb(0, 0, 0);\n"
            "    border-left: 1.5px solid rgb(0, 0, 0);\n"
            "    border-bottom: 1.5px solid rgb(160, 160, 160);\n"
            "    border-right: 1.5px solid rgb(160, 160, 160);\n"
            "}\n"
            "\n"
            "QRadioButton::indicator::checked{\n"
            "    background-color: white;\n"
            "}\n"
            "\n"
            "QRadioButton::indicator::unchecked:hover{\n"
            "    background-color: #9F9F9F;\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::up-button,\n"
            "QSpinBox::up-button{\n"
            "    image: url(:/imgs/imgs/drop_up_arrow.png);\n"
            "    width: 11px;\n"
            "    background-color: rgb(0, 79, 0);\n"
            "}\n"
            "\n"
            "QDoubleSpinBox::down-button,\n"
            "QSpinBox::down-button{\n"
            "    image: url(:/imgs/imgs/drop_down_arrow.png);\n"
            "    width: 11px;\n"
            "    background-color: rgb(0, 79, 0);\n"
            "}\n"
        )

        self.gridLayout = QGridLayout(NIDAQ_Data_Driven_Control)
        self.gridLayout.setObjectName(u"gridLayout")

        # ============================================================
        # Main configuration widget
        # ============================================================
        self.widget_top = QWidget(NIDAQ_Data_Driven_Control)
        self.widget_top.setObjectName(u"widget_top")

        self.gridLayout_2 = QGridLayout(self.widget_top)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.line = QFrame(self.widget_top)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 0))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setLineWidth(1)
        self.line.setStyleSheet(u"QFrame#line { background-color: rgb(80, 80, 80); border: none; max-width: 1px; }")

        self.gridLayout_2.addWidget(self.line, 0, 2, 20, 1)

        # ============================================================
        # Simulate?
        # ============================================================
        self.label_simulate = QLabel(self.widget_top)
        self.label_simulate.setObjectName(u"label_simulate")

        self.gridLayout_2.addWidget(self.label_simulate, 1, 0, 1, 1)

        self.widget_simulate = QWidget(self.widget_top)
        self.widget_simulate.setObjectName(u"widget_simulate")

        self.horizontalLayout_simulate = QHBoxLayout(self.widget_simulate)
        self.horizontalLayout_simulate.setObjectName(u"horizontalLayout_simulate")

        self.yes_simulate_radio = QRadioButton(self.widget_simulate)
        self.yes_simulate_radio.setObjectName(u"yes_simulate_radio")

        self.simulate_radio_group = QButtonGroup(NIDAQ_Data_Driven_Control)
        self.simulate_radio_group.setObjectName(u"simulate_radio_group")
        self.simulate_radio_group.addButton(self.yes_simulate_radio)

        self.horizontalLayout_simulate.addWidget(self.yes_simulate_radio)

        self.no_simulate_radio = QRadioButton(self.widget_simulate)
        self.no_simulate_radio.setObjectName(u"no_simulate_radio")
        self.no_simulate_radio.setChecked(True)
        self.simulate_radio_group.addButton(self.no_simulate_radio)

        self.horizontalLayout_simulate.addWidget(self.no_simulate_radio)

        self.horizontalSpacer_2 = QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout_simulate.addItem(self.horizontalSpacer_2)

        self.gridLayout_2.addWidget(self.widget_simulate, 1, 3, 1, 1)

        # ============================================================
        # Simulation plant equation
        # ============================================================
        self.label_system_equation = QLabel(self.widget_top)
        self.label_system_equation.setObjectName(u"label_system_equation")

        self.gridLayout_2.addWidget(self.label_system_equation, 2, 0, 1, 1)

        self.label_i_polinomial = QLabel(self.widget_top)
        self.label_i_polinomial.setObjectName(u"label_i_polinomial")

        self.gridLayout_2.addWidget(self.label_i_polinomial, 2, 1, 1, 1)

        self.widget_polynomial = QWidget(self.widget_top)
        self.widget_polynomial.setObjectName(u"widget_polynomial")

        self.horizontalLayout_polynomial = QHBoxLayout(self.widget_polynomial)
        self.horizontalLayout_polynomial.setObjectName(
            u"horizontalLayout_polynomial"
        )

        self.label_numerator = QLabel(self.widget_polynomial)
        self.label_numerator.setObjectName(u"label_numerator")
        self.horizontalLayout_polynomial.addWidget(self.label_numerator)

        self.lineEdit_numerator = QLineEdit(self.widget_polynomial)
        self.lineEdit_numerator.setObjectName(u"lineEdit_numerator")
        self.horizontalLayout_polynomial.addWidget(self.lineEdit_numerator)

        self.label_denominator = QLabel(self.widget_polynomial)
        self.label_denominator.setObjectName(u"label_denominator")
        self.horizontalLayout_polynomial.addWidget(self.label_denominator)

        self.lineEdit_denominator = QLineEdit(self.widget_polynomial)
        self.lineEdit_denominator.setObjectName(u"lineEdit_denominator")
        self.horizontalLayout_polynomial.addWidget(self.lineEdit_denominator)

        self.gridLayout_2.addWidget(self.widget_polynomial, 2, 3, 1, 1)

        # ============================================================
        # NI-DAQ device
        # ============================================================
        self.label_nidaq = QLabel(self.widget_top)
        self.label_nidaq.setObjectName(u"label_nidaq")
        self.label_nidaq.setMinimumSize(QSize(154, 30))
        self.label_nidaq.setMaximumSize(QSize(160, 16777215))

        self.gridLayout_2.addWidget(self.label_nidaq, 3, 0, 1, 1)

        self.widget_nidaq = QWidget(self.widget_top)
        self.widget_nidaq.setObjectName(u"widget_nidaq")

        self.horizontalLayout_nidaq = QHBoxLayout(self.widget_nidaq)
        self.horizontalLayout_nidaq.setObjectName(u"horizontalLayout_nidaq")

        self.device_combo = QComboBox(self.widget_nidaq)
        self.device_combo.setObjectName(u"device_combo")
        self.device_combo.setMinimumSize(QSize(0, 0))
        self.device_combo.setMaximumSize(QSize(9000000, 16777215))

        self.horizontalLayout_nidaq.addWidget(self.device_combo)

        self.reload_devices = QPushButton(self.widget_nidaq)
        self.reload_devices.setObjectName(u"reload_devices")
        self.reload_devices.setMinimumSize(QSize(22, 22))
        self.reload_devices.setMaximumSize(QSize(22, 22))

        self.horizontalLayout_nidaq.addWidget(self.reload_devices)

        self.gridLayout_2.addWidget(self.widget_nidaq, 3, 3, 1, 1)

        # ============================================================
        # AI channel
        # ============================================================
        self.label_ai_channel = QLabel(self.widget_top)
        self.label_ai_channel.setObjectName(u"label_ai_channel")

        self.gridLayout_2.addWidget(self.label_ai_channel, 4, 0, 1, 1)

        self.widget_ai_channel = QWidget(self.widget_top)
        self.widget_ai_channel.setObjectName(u"widget_ai_channel")

        self.horizontalLayout_ai_channel = QHBoxLayout(self.widget_ai_channel)
        self.horizontalLayout_ai_channel.setObjectName(
            u"horizontalLayout_ai_channel"
        )

        self.ai_channel_combo = QComboBox(self.widget_ai_channel)
        self.ai_channel_combo.setObjectName(u"ai_channel_combo")

        self.horizontalLayout_ai_channel.addWidget(self.ai_channel_combo)

        self.gridLayout_2.addWidget(self.widget_ai_channel, 4, 3, 1, 1)

        # ============================================================
        # AO channel
        # ============================================================
        self.label_ao_channel = QLabel(self.widget_top)
        self.label_ao_channel.setObjectName(u"label_ao_channel")

        self.gridLayout_2.addWidget(self.label_ao_channel, 5, 0, 1, 1)

        self.widget_ao_channel = QWidget(self.widget_top)
        self.widget_ao_channel.setObjectName(u"widget_ao_channel")

        self.horizontalLayout_ao_channel = QHBoxLayout(self.widget_ao_channel)
        self.horizontalLayout_ao_channel.setObjectName(
            u"horizontalLayout_ao_channel"
        )

        self.ao_channel_combo = QComboBox(self.widget_ao_channel)
        self.ao_channel_combo.setObjectName(u"ao_channel_combo")

        self.horizontalLayout_ao_channel.addWidget(self.ao_channel_combo)

        self.gridLayout_2.addWidget(self.widget_ao_channel, 5, 3, 1, 1)

        # ============================================================
        # Terminal config
        # ============================================================
        self.label_terminal = QLabel(self.widget_top)
        self.label_terminal.setObjectName(u"label_terminal")

        self.gridLayout_2.addWidget(self.label_terminal, 6, 0, 1, 1)

        self.widget_terminal_config = QWidget(self.widget_top)
        self.widget_terminal_config.setObjectName(u"widget_terminal_config")

        self.horizontalLayout_terminal = QHBoxLayout(self.widget_terminal_config)
        self.horizontalLayout_terminal.setObjectName(u"horizontalLayout_terminal")

        self.terminal_config_combo = QComboBox(self.widget_terminal_config)
        self.terminal_config_combo.setObjectName(u"terminal_config_combo")

        self.horizontalLayout_terminal.addWidget(self.terminal_config_combo)

        self.gridLayout_2.addWidget(self.widget_terminal_config, 6, 3, 1, 1)

        # ============================================================
        # Setpoint
        # ============================================================
        self.label_setpoint = QLabel(self.widget_top)
        self.label_setpoint.setObjectName(u"label_setpoint")
        self.label_setpoint.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_setpoint, 7, 0, 1, 1)

        self.widget_setpoint = QWidget(self.widget_top)
        self.widget_setpoint.setObjectName(u"widget_setpoint")

        self.horizontalLayout_setpoint = QHBoxLayout(self.widget_setpoint)
        self.horizontalLayout_setpoint.setObjectName(u"horizontalLayout_setpoint")

        self.doubleSpinBox_setpoint = QDoubleSpinBox(self.widget_setpoint)
        self.doubleSpinBox_setpoint.setObjectName(u"doubleSpinBox_setpoint")
        self.doubleSpinBox_setpoint.setMaximumSize(QSize(100, 16777215))
        self.doubleSpinBox_setpoint.setDecimals(6)
        self.doubleSpinBox_setpoint.setMaximum(999999999999.0)
        self.doubleSpinBox_setpoint.setSingleStep(0.01)
        self.doubleSpinBox_setpoint.setValue(5.0)

        self.horizontalLayout_setpoint.addWidget(self.doubleSpinBox_setpoint)

        self.comboBox_setpoint = QComboBox(self.widget_setpoint)
        self.comboBox_setpoint.setObjectName(u"comboBox_setpoint")
        self.comboBox_setpoint.addItem("")
        self.comboBox_setpoint.addItem("")
        self.comboBox_setpoint.addItem("")
        self.comboBox_setpoint.setMinimumSize(QSize(190, 0))
        self.comboBox_setpoint.setMaximumSize(QSize(9000000, 16777215))

        self.horizontalLayout_setpoint.addWidget(self.comboBox_setpoint)

        self.gridLayout_2.addWidget(self.widget_setpoint, 7, 3, 1, 1)

        # ============================================================
        # Unit
        # ============================================================
        self.label_unit = QLabel(self.widget_top)
        self.label_unit.setObjectName(u"label_unit")
        self.label_unit.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_unit, 8, 0, 1, 1)

        self.widget_unit = QWidget(self.widget_top)
        self.widget_unit.setObjectName(u"widget_unit")

        self.horizontalLayout_unit = QHBoxLayout(self.widget_unit)
        self.horizontalLayout_unit.setObjectName(u"horizontalLayout_unit")

        self.lineEdit_unit = QLineEdit(self.widget_unit)
        self.lineEdit_unit.setObjectName(u"lineEdit_unit")
        self.lineEdit_unit.setMaximumSize(QSize(9999999, 16777215))

        self.horizontalLayout_unit.addWidget(self.lineEdit_unit)

        self.gridLayout_2.addWidget(
            self.widget_unit,
            8,
            3,
            1,
            1,
            Qt.AlignmentFlag.AlignVCenter
        )

        # ============================================================
        # Calibration equations
        # ============================================================
        self.label_equation = QLabel(self.widget_top)
        self.label_equation.setObjectName(u"label_equation")
        self.label_equation.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_equation, 9, 0, 1, 1)

        self.label_i_equation = QLabel(self.widget_top)
        self.label_i_equation.setObjectName(u"label_i_equation")

        self.gridLayout_2.addWidget(
            self.label_i_equation,
            9,
            1,
            1,
            1,
            Qt.AlignmentFlag.AlignRight
        )

        self.widget_equation = QWidget(self.widget_top)
        self.widget_equation.setObjectName(u"widget_equation")

        self.horizontalLayout_equation = QHBoxLayout(self.widget_equation)
        self.horizontalLayout_equation.setObjectName(u"horizontalLayout_equation")

        self.label_vunit = QLabel(self.widget_equation)
        self.label_vunit.setObjectName(u"label_vunit")
        self.horizontalLayout_equation.addWidget(self.label_vunit)

        self.lineEdit_equationvu = QLineEdit(self.widget_equation)
        self.lineEdit_equationvu.setObjectName(u"lineEdit_equationvu")
        self.horizontalLayout_equation.addWidget(self.lineEdit_equationvu)

        self.label_unitv = QLabel(self.widget_equation)
        self.label_unitv.setObjectName(u"label_unitv")
        self.horizontalLayout_equation.addWidget(self.label_unitv)

        self.lineEdit_equationuv = QLineEdit(self.widget_equation)
        self.lineEdit_equationuv.setObjectName(u"lineEdit_equationuv")
        self.horizontalLayout_equation.addWidget(self.lineEdit_equationuv)

        self.gridLayout_2.addWidget(self.widget_equation, 9, 3, 1, 1)

        # ============================================================
        # Sampling period
        # ============================================================
        self.label_periody = QLabel(self.widget_top)
        self.label_periody.setObjectName(u"label_periody")
        self.label_periody.setMinimumSize(QSize(0, 30))

        self.gridLayout_2.addWidget(self.label_periody, 10, 0, 1, 1)

        self.widget_period = QWidget(self.widget_top)
        self.widget_period.setObjectName(u"widget_period")

        self.horizontalLayout_period = QHBoxLayout(self.widget_period)
        self.horizontalLayout_period.setObjectName(u"horizontalLayout_period")

        self.doubleSpinBox_period = QDoubleSpinBox(self.widget_period)
        self.doubleSpinBox_period.setObjectName(u"doubleSpinBox_period")
        self.doubleSpinBox_period.setDecimals(6)
        self.doubleSpinBox_period.setMaximum(999999999999.0)
        self.doubleSpinBox_period.setSingleStep(0.01)
        self.doubleSpinBox_period.setValue(0.05)

        self.horizontalLayout_period.addWidget(self.doubleSpinBox_period)

        self.gridLayout_2.addWidget(self.widget_period, 10, 3, 1, 1)

        # ============================================================
        # Beta
        # ============================================================
        self.label_beta = QLabel(self.widget_top)
        self.label_beta.setObjectName(u"label_beta")

        self.gridLayout_2.addWidget(self.label_beta, 11, 0, 1, 1)

        self.label_i_beta = QLabel(self.widget_top)
        self.label_i_beta.setObjectName(u"label_i_beta")

        self.gridLayout_2.addWidget(self.label_i_beta, 11, 1, 1, 1)

        self.plainTextEdit_beta = QPlainTextEdit(self.widget_top)
        self.plainTextEdit_beta.setObjectName(u"plainTextEdit_beta")
        self.plainTextEdit_beta.setMinimumSize(QSize(0, 140))

        self.gridLayout_2.addWidget(self.plainTextEdit_beta, 11, 3, 1, 1)

        # ============================================================
        # Reference model M(q)
        # ============================================================
        self.label_reference_model = QLabel(self.widget_top)
        self.label_reference_model.setObjectName(u"label_reference_model")

        self.gridLayout_2.addWidget(self.label_reference_model, 12, 0, 1, 1)

        self.widget_reference_model = QWidget(self.widget_top)
        self.widget_reference_model.setObjectName(u"widget_reference_model")

        self.horizontalLayout_reference_model = QHBoxLayout(
            self.widget_reference_model
        )
        self.horizontalLayout_reference_model.setObjectName(
            u"horizontalLayout_reference_model"
        )

        self.label_num_M = QLabel(self.widget_reference_model)
        self.label_num_M.setObjectName(u"label_num_M")
        self.horizontalLayout_reference_model.addWidget(self.label_num_M)

        self.lineEdit_num_M = QLineEdit(self.widget_reference_model)
        self.lineEdit_num_M.setObjectName(u"lineEdit_num_M")
        self.horizontalLayout_reference_model.addWidget(self.lineEdit_num_M)

        self.label_den_M = QLabel(self.widget_reference_model)
        self.label_den_M.setObjectName(u"label_den_M")
        self.horizontalLayout_reference_model.addWidget(self.label_den_M)

        self.lineEdit_den_M = QLineEdit(self.widget_reference_model)
        self.lineEdit_den_M.setObjectName(u"lineEdit_den_M")
        self.horizontalLayout_reference_model.addWidget(self.lineEdit_den_M)

        self.gridLayout_2.addWidget(
            self.widget_reference_model,
            12,
            3,
            1,
            1
        )

        # ============================================================
        # Instrument length l
        # ============================================================
        self.label_l = QLabel(self.widget_top)
        self.label_l.setObjectName(u"label_l")

        self.gridLayout_2.addWidget(self.label_l, 13, 0, 1, 1)

        self.widget_l = QWidget(self.widget_top)
        self.widget_l.setObjectName(u"widget_l")

        self.horizontalLayout_l = QHBoxLayout(self.widget_l)
        self.horizontalLayout_l.setObjectName(u"horizontalLayout_l")

        self.spinBox_l = QSpinBox(self.widget_l)
        self.spinBox_l.setObjectName(u"spinBox_l")
        self.spinBox_l.setMinimum(1)
        self.spinBox_l.setMaximum(999999)
        self.spinBox_l.setValue(20)

        self.horizontalLayout_l.addWidget(self.spinBox_l)

        self.gridLayout_2.addWidget(self.widget_l, 13, 3, 1, 1)

        # ============================================================
        # NCbT data files
        # ============================================================
        self.label_data_files = QLabel(self.widget_top)
        self.label_data_files.setObjectName(u"label_data_files")

        self.gridLayout_2.addWidget(self.label_data_files, 14, 0, 1, 1)

        self.widget_data_files = QWidget(self.widget_top)
        self.widget_data_files.setObjectName(u"widget_data_files")

        self.gridLayout_data_files = QGridLayout(self.widget_data_files)
        self.gridLayout_data_files.setObjectName(u"gridLayout_data_files")

        self.label_u_data = QLabel(self.widget_data_files)
        self.label_u_data.setObjectName(u"label_u_data")
        self.gridLayout_data_files.addWidget(self.label_u_data, 0, 0, 1, 1)

        self.lineEdit_u_data_path = QLineEdit(self.widget_data_files)
        self.lineEdit_u_data_path.setObjectName(u"lineEdit_u_data_path")
        self.gridLayout_data_files.addWidget(
            self.lineEdit_u_data_path,
            0,
            1,
            1,
            1
        )

        self.pushButton_load_u = QPushButton(self.widget_data_files)
        self.pushButton_load_u.setObjectName(u"pushButton_load_u")
        self.gridLayout_data_files.addWidget(
            self.pushButton_load_u,
            0,
            2,
            1,
            1
        )

        self.label_y_data = QLabel(self.widget_data_files)
        self.label_y_data.setObjectName(u"label_y_data")
        self.gridLayout_data_files.addWidget(self.label_y_data, 1, 0, 1, 1)

        self.lineEdit_y_data_path = QLineEdit(self.widget_data_files)
        self.lineEdit_y_data_path.setObjectName(u"lineEdit_y_data_path")
        self.gridLayout_data_files.addWidget(
            self.lineEdit_y_data_path,
            1,
            1,
            1,
            1
        )

        self.pushButton_load_y = QPushButton(self.widget_data_files)
        self.pushButton_load_y.setObjectName(u"pushButton_load_y")
        self.gridLayout_data_files.addWidget(
            self.pushButton_load_y,
            1,
            2,
            1,
            1
        )

        self.label_r_data = QLabel(self.widget_data_files)
        self.label_r_data.setObjectName(u"label_r_data")
        self.gridLayout_data_files.addWidget(self.label_r_data, 2, 0, 1, 1)

        self.lineEdit_r_data_path = QLineEdit(self.widget_data_files)
        self.lineEdit_r_data_path.setObjectName(u"lineEdit_r_data_path")
        self.gridLayout_data_files.addWidget(
            self.lineEdit_r_data_path,
            2,
            1,
            1,
            1
        )

        self.pushButton_load_r = QPushButton(self.widget_data_files)
        self.pushButton_load_r.setObjectName(u"pushButton_load_r")
        self.gridLayout_data_files.addWidget(
            self.pushButton_load_r,
            2,
            2,
            1,
            1
        )

        self.label_t_data = QLabel(self.widget_data_files)
        self.label_t_data.setObjectName(u"label_t_data")
        self.gridLayout_data_files.addWidget(self.label_t_data, 3, 0, 1, 1)

        self.lineEdit_t_data_path = QLineEdit(self.widget_data_files)
        self.lineEdit_t_data_path.setObjectName(u"lineEdit_t_data_path")
        self.gridLayout_data_files.addWidget(
            self.lineEdit_t_data_path,
            3,
            1,
            1,
            1
        )

        self.pushButton_load_t = QPushButton(self.widget_data_files)
        self.pushButton_load_t.setObjectName(u"pushButton_load_t")
        self.gridLayout_data_files.addWidget(
            self.pushButton_load_t,
            3,
            2,
            1,
            1
        )

        self.gridLayout_2.addWidget(self.widget_data_files, 14, 3, 1, 1)

        # ============================================================
        # Estimated rho
        # ============================================================
        self.label_rho = QLabel(self.widget_top)
        self.label_rho.setObjectName(u"label_rho")

        self.gridLayout_2.addWidget(self.label_rho, 15, 0, 1, 1)

        self.plainTextEdit_rho = QPlainTextEdit(self.widget_top)
        self.plainTextEdit_rho.setObjectName(u"plainTextEdit_rho")
        self.plainTextEdit_rho.setMinimumSize(QSize(0, 80))
        self.plainTextEdit_rho.setReadOnly(True)

        self.gridLayout_2.addWidget(self.plainTextEdit_rho, 15, 3, 1, 1)

        # ============================================================
        # Save
        # ============================================================
        self.label_save = QLabel(self.widget_top)
        self.label_save.setObjectName(u"label_save")

        self.gridLayout_2.addWidget(self.label_save, 16, 0, 1, 1)

        self.widget_save = QWidget(self.widget_top)
        self.widget_save.setObjectName(u"widget_save")

        self.horizontalLayout_save = QHBoxLayout(self.widget_save)
        self.horizontalLayout_save.setObjectName(u"horizontalLayout_save")

        self.yes_save_radio = QRadioButton(self.widget_save)
        self.yes_save_radio.setObjectName(u"yes_save_radio")
        self.yes_save_radio.setChecked(True)

        self.save_radio_group = QButtonGroup(NIDAQ_Data_Driven_Control)
        self.save_radio_group.setObjectName(u"save_radio_group")
        self.save_radio_group.addButton(self.yes_save_radio)

        self.horizontalLayout_save.addWidget(self.yes_save_radio)

        self.no_save_radio = QRadioButton(self.widget_save)
        self.no_save_radio.setObjectName(u"no_save_radio")
        self.save_radio_group.addButton(self.no_save_radio)

        self.horizontalLayout_save.addWidget(self.no_save_radio)

        self.horizontalSpacer = QSpacerItem(
            40,
            20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout_save.addItem(self.horizontalSpacer)

        self.gridLayout_2.addWidget(self.widget_save, 16, 3, 1, 1)

        # ============================================================
        # Path
        # ============================================================
        self.label_path = QLabel(self.widget_top)
        self.label_path.setObjectName(u"label_path")

        self.gridLayout_2.addWidget(self.label_path, 17, 0, 1, 1)

        self.widget_path = QWidget(self.widget_top)
        self.widget_path.setObjectName(u"widget_path")

        self.horizontalLayout_path = QHBoxLayout(self.widget_path)
        self.horizontalLayout_path.setObjectName(u"horizontalLayout_path")

        self.path_line_edit = QLineEdit(self.widget_path)
        self.path_line_edit.setObjectName(u"path_line_edit")
        self.path_line_edit.setMinimumSize(QSize(0, 22))

        self.horizontalLayout_path.addWidget(self.path_line_edit)

        self.path_folder_browse = QPushButton(self.widget_path)
        self.path_folder_browse.setObjectName(u"path_folder_browse")
        self.path_folder_browse.setMinimumSize(QSize(90, 30))

        self.horizontalLayout_path.addWidget(self.path_folder_browse)

        self.gridLayout_2.addWidget(
            self.widget_path,
            17,
            3,
            1,
            1,
            Qt.AlignmentFlag.AlignVCenter
        )

        # ============================================================
        # Confirm button
        # ============================================================
        self.pushButton_confirm = QPushButton(self.widget_top)
        self.pushButton_confirm.setObjectName(u"pushButton_confirm")
        self.pushButton_confirm.setMinimumSize(QSize(90, 30))
        self.pushButton_confirm.setMaximumSize(QSize(140, 16777215))

        self.gridLayout_2.addWidget(
            self.pushButton_confirm,
            18,
            3,
            1,
            1,
            Qt.AlignmentFlag.AlignHCenter
        )

        self.gridLayout.addWidget(self.widget_top, 1, 0, 1, 1)

        # ============================================================
        # Controller preview / equation frame
        # ============================================================
        self.frame_equation = QFrame(NIDAQ_Data_Driven_Control)
        self.frame_equation.setObjectName(u"frame_equation")
        self.frame_equation.setMinimumSize(QSize(400, 150))
        self.frame_equation.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_equation.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_equation.setStyleSheet(u"QFrame#frame_equation { border: 1px solid rgb(80, 80, 80); }")

        self.gridLayout_5 = QGridLayout(self.frame_equation)
        self.gridLayout_5.setObjectName(u"gridLayout_5")

        self.widget_image = QWidget(self.frame_equation)
        self.widget_image.setObjectName(u"widget_image")
        self.widget_image.setMinimumSize(QSize(0, 130))

        self.image_layout = QVBoxLayout(self.widget_image)
        self.image_layout.setObjectName(u"image_layout")

        self.gridLayout_5.addWidget(self.widget_image, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.frame_equation, 2, 0, 1, 1)

        # Separator
        self.line_3 = QFrame(NIDAQ_Data_Driven_Control)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setMinimumSize(QSize(0, 0))
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Plain)
        self.line_3.setLineWidth(1)
        self.line_3.setStyleSheet(u"QFrame#line_3 { background-color: rgb(80, 80, 80); border: none; max-height: 1px; }")

        self.gridLayout.addWidget(self.line_3, 3, 0, 1, 1)

        # Start button
        self.pushButton_start = QPushButton(NIDAQ_Data_Driven_Control)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setMinimumSize(QSize(180, 30))
        self.pushButton_start.setMaximumSize(QSize(240, 30))

        self.gridLayout.addWidget(
            self.pushButton_start,
            4,
            0,
            1,
            1,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.retranslateUi(NIDAQ_Data_Driven_Control)

        QMetaObject.connectSlotsByName(NIDAQ_Data_Driven_Control)

    def retranslateUi(self, NIDAQ_Data_Driven_Control):
        NIDAQ_Data_Driven_Control.setWindowTitle(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"PYDAQ - Data-Driven Control NI-DAQ",
                None
            )
        )

        self.label_simulate.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Simulate?",
                None
            )
        )
        self.yes_simulate_radio.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Yes",
                None
            )
        )
        self.no_simulate_radio.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"No",
                None
            )
        )

        self.label_system_equation.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Simulated plant:",
                None
            )
        )
        self.label_i_polinomial.setToolTip(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"<html><head/><body><p>Transfer function of a polynomial "
                "system G(s)=N(s)/D(s).</p></body></html>",
                None
            )
        )
        self.label_i_polinomial.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"",
                None
            )
        )
        self.label_i_polinomial.clear()
        self.label_i_polinomial.hide()

        self.label_numerator.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Numerator:",
                None
            )
        )
        self.lineEdit_numerator.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"1",
                None
            )
        )
        self.label_denominator.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Denominator:",
                None
            )
        )
        self.lineEdit_denominator.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"1*s+0.2",
                None
            )
        )

        self.label_nidaq.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Device:",
                None
            )
        )
        self.reload_devices.setText("")

        self.label_ai_channel.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"AI channels:",
                None
            )
        )
        self.label_ao_channel.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"AO channels:",
                None
            )
        )

        self.label_terminal.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Terminal config.:",
                None
            )
        )

        self.label_setpoint.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Setpoint:",
                None
            )
        )
        self.comboBox_setpoint.setItemText(
            0,
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Voltage (V)",
                None
            )
        )
        self.comboBox_setpoint.setItemText(
            1,
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Temperature (C\u00b0)",
                None
            )
        )
        self.comboBox_setpoint.setItemText(
            2,
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Other",
                None
            )
        )

        self.label_unit.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Unit:",
                None
            )
        )
        self.lineEdit_unit.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Current (A)",
                None
            )
        )

        self.label_equation.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Equation:",
                None
            )
        )
        self.label_i_equation.setToolTip(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"<html><head/><body><p>Calibration equations should use x "
                "as variable. Example: 1*x or A*x+B.</p></body></html>",
                None
            )
        )
        self.label_i_equation.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"",
                None
            )
        )

        self.label_vunit.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"V(Unit)",
                None
            )
        )
        self.lineEdit_equationvu.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"1*x",
                None
            )
        )
        self.label_unitv.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Unit(V)",
                None
            )
        )
        self.lineEdit_equationuv.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"1*x",
                None
            )
        )

        self.label_periody.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Sampling period (s):",
                None
            )
        )

        self.label_beta.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"β:",
                None
            )
        )
        self.label_i_beta.setToolTip(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"<html><head/><body><p>β is mandatory in NCbT and defines "
                "the controller structure.</p></body></html>",
                None
            )
        )
        self.label_i_beta.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"",
                None
            )
        )
        self.label_i_beta.clear()
        self.label_i_beta.hide()
        self.plainTextEdit_beta.setPlainText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"[\n"
                "    ([1], [1, -1]),\n"
                "    ([0, 1], [1, -1]),\n"
                "    ([0, 0, 1], [1, -1]),\n"
                "    ([0, 0, 0, 0.0090559170], [1, -1]),\n"
                "    ([0, 0, 0, 0, 1], [1, -1]),\n"
                "    ([0, 0, 0, 0, 0, 1], [1, -1])\n"
                "]",
                None
            )
        )

        self.label_reference_model.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Reference model:",
                None
            )
        )
        self.label_num_M.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Numerator:",
                None
            )
        )
        self.lineEdit_num_M.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"[0, 0, 0, 0.0090559170]",
                None
            )
        )
        self.label_den_M.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Denominator:",
                None
            )
        )
        self.lineEdit_den_M.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"[1, -1.8096748361, 0.8187307531]",
                None
            )
        )

        self.label_l.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"l:",
                None
            )
        )

        self.label_data_files.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"NCbT data files:",
                None
            )
        )
        self.label_u_data.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"u:",
                None
            )
        )
        self.label_y_data.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"y:",
                None
            )
        )
        self.label_r_data.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"r:",
                None
            )
        )
        self.label_t_data.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"t:",
                None
            )
        )

        self.pushButton_load_u.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"BROWSE",
                None
            )
        )
        self.pushButton_load_y.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"BROWSE",
                None
            )
        )
        self.pushButton_load_r.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"BROWSE",
                None
            )
        )
        self.pushButton_load_t.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"BROWSE",
                None
            )
        )

        self.label_rho.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"rho:",
                None
            )
        )

        self.label_save.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Save data?",
                None
            )
        )
        self.yes_save_radio.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Yes",
                None
            )
        )
        self.no_save_radio.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"No",
                None
            )
        )

        self.label_path.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"Path:",
                None
            )
        )
        self.path_folder_browse.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u" BROWSE ",
                None
            )
        )

        self.pushButton_confirm.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u" CONFIRM ",
                None
            )
        )

        self.pushButton_start.setText(
            QCoreApplication.translate(
                "NIDAQ_Data_Driven_Control",
                u"DATA-DRIVEN CONTROL",
                None
            )
        )
