# -*- coding: utf-8 -*-
"""Complete hand-written Qt interface for Data-Driven Control execution."""
from PySide6.QtCore import QCoreApplication, QLocale, QMetaObject, QSize, Qt
from PySide6.QtWidgets import (
    QCheckBox,QComboBox,QDialog,QDoubleSpinBox,QFormLayout,QGridLayout,
    QGroupBox,QHBoxLayout,QLabel,QLineEdit,QPlainTextEdit,QProgressBar,
    QPushButton,QScrollArea,QSpinBox,QTabWidget,QVBoxLayout,QWidget
)
try:
    from . import resources_1_rc
except ImportError:
    import resources_1_rc


STYLE="""
QDialog,QWidget{background-color:#404040;color:white;font:11pt Helvetica;}
QGroupBox{border:1px solid #a6a6a6;margin-top:12px;padding-top:8px;}
QGroupBox::title{subcontrol-origin:margin;left:10px;padding:0 4px;}
QComboBox,QLineEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox{background:#4d4d4d;color:white;border-top:1.5px solid #2e2e2e;border-left:1.5px solid #2e2e2e;border-bottom:1.5px solid #a6a6a6;border-right:1.5px solid #a6a6a6;min-height:25px;}
QSpinBox::up-button,QDoubleSpinBox::up-button{subcontrol-origin:border;subcontrol-position:top right;width:28px;height:50%;}
QSpinBox::down-button,QDoubleSpinBox::down-button{subcontrol-origin:border;subcontrol-position:bottom right;width:28px;height:50%;}
QSpinBox::up-arrow,QDoubleSpinBox::up-arrow{width:9px;height:7px;}
QSpinBox::down-arrow,QDoubleSpinBox::down-arrow{width:9px;height:7px;}
QPushButton{background:#004f00;border-top:1.5px solid #7fa77f;border-left:1.5px solid #7fa77f;border-bottom:1.5px solid black;border-right:1.5px solid black;min-height:30px;}
QPushButton:hover{background:#003200;} QPushButton:pressed{border:2px solid white;}
QTabWidget::pane{border:1px solid #a6a6a6;} QTabBar::tab{background:#4d4d4d;padding:7px 14px;} QTabBar::tab:selected{background:#8c8c8c;}
QProgressBar{border:1px solid #a6a6a6;text-align:center;background:#4d4d4d;} QProgressBar::chunk{background:#004f00;}

QScrollArea { border: none; }
QScrollBar:vertical {
    border: 1px solid rgb(140, 140, 140);
    background: rgb(140, 140, 140);
    width: 17px;
    margin: 17px 0 17px 0;
}
QScrollBar::handle:vertical {
    background: rgb(0, 79, 0);
    min-height: 20px;
}
QScrollBar::add-line:vertical {
    image: url(:/imgs/imgs/drop_down_arrow.png);
    border: 1px solid rgb(140, 140, 140);
    background: rgb(0, 79, 0);
    height: 15px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical {
    image: url(:/imgs/imgs/drop_up_arrow.png);
    border: 1px solid rgb(140, 140, 140);
    background: rgb(0, 79, 0);
    height: 15px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover,
QScrollBar::sub-line:vertical:hover,
QScrollBar::handle:vertical:hover { background: rgb(0, 50, 0); }
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical { background: none; }

QScrollBar:horizontal {
    border: 1px solid rgb(140, 140, 140);
    background: rgb(140, 140, 140);
    height: 17px;
    margin: 0 17px 0 17px;
}
QScrollBar::handle:horizontal {
    background: rgb(0, 79, 0);
    min-width: 20px;
}
QScrollBar::add-line:horizontal {
    image: url(:/imgs/imgs/drop_right_arrow.png);
    border: 1px solid rgb(140, 140, 140);
    background: rgb(0, 79, 0);
    width: 15px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal {
    image: url(:/imgs/imgs/drop_left_arrow.png);
    border: 1px solid rgb(140, 140, 140);
    background: rgb(0, 79, 0);
    width: 15px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:hover,
QScrollBar::sub-line:horizontal:hover,
QScrollBar::handle:horizontal:hover { background: rgb(0, 50, 0); }
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal { background: none; }
QSpinBox, QDoubleSpinBox {
    min-height: 25px;
    padding-right: 13px;
}
QSpinBox::up-button, QDoubleSpinBox::up-button {
    image: url(:/imgs/imgs/drop_up_arrow.png);
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 11px;
    background-color: rgb(0, 79, 0);
    border-top: 1.5px solid rgb(127, 167, 127);
    border-left: 1.5px solid rgb(127, 167, 127);
    border-bottom: 0px;
    border-right: 1.5px solid rgb(0, 0, 0);
}
QSpinBox::down-button, QDoubleSpinBox::down-button {
    image: url(:/imgs/imgs/drop_down_arrow.png);
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 11px;
    background-color: rgb(0, 79, 0);
    border-top: 0px;
    border-left: 1.5px solid rgb(127, 167, 127);
    border-bottom: 1.5px solid rgb(0, 0, 0);
    border-right: 1.5px solid rgb(0, 0, 0);
}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {
    background-color: rgb(0, 50, 0);
}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {
    border: 2px solid rgb(255, 255, 255);
}

"""

def ds(parent,minimum,maximum,value,dec=6,suffix=""):
    w=QDoubleSpinBox(parent);w.setLocale(QLocale.c());w.setDecimals(dec);w.setRange(minimum,maximum);w.setValue(value);w.setSuffix(suffix);return w

def spin(parent,minimum,maximum,value):
    w=QSpinBox(parent);w.setLocale(QLocale.c());w.setRange(minimum,maximum);w.setValue(value);return w

class Ui_Dialog_Plot_Data_Driven_NIDAQ_Window(object):
    def setupUi(self,dialog):
        dialog.setObjectName('Dialog_Plot_Data_Driven_NIDAQ_Window');dialog.resize(1180,820);dialog.setMinimumSize(QSize(980,680));dialog.setStyleSheet(STYLE)
        self.mainLayout=QVBoxLayout(dialog)
        self.header=QHBoxLayout();self.label_state_title=QLabel('State:');self.label_state=QLabel('IDLE');self.label_state.setStyleSheet('font-weight:bold;color:#7fff7f;')
        self.label_status=QLabel('Configure the experiment and press START COMPLETE CYCLE.');self.header.addWidget(self.label_state_title);self.header.addWidget(self.label_state);self.header.addWidget(self.label_status,1);self.mainLayout.addLayout(self.header)
        self.progressBar=QProgressBar();self.progressBar.setRange(0,100);self.progressBar.setValue(0);self.mainLayout.addWidget(self.progressBar)
        self.tabs=QTabWidget();self.mainLayout.addWidget(self.tabs,1)

        # PRBS tab
        self.tab_prbs=QWidget();self.tabs.addTab(self.tab_prbs,'PRBS Experiment');prbs_main=QHBoxLayout(self.tab_prbs)
        left=QVBoxLayout();prbs_main.addLayout(left,0);self.group_prbs=QGroupBox('PRBS parameters');f=QFormLayout(self.group_prbs)
        self.spin_prbs_bits=spin(self.group_prbs,2,32,6);self.spin_prbs_seed=spin(self.group_prbs,0,2147483647,101)
        self.spin_var_tb=spin(self.group_prbs,1,100000,1);self.spin_ts=ds(self.group_prbs,0.001,10,0.01,6,' s')
        self.spin_collection_time=ds(self.group_prbs,0.1,3600,10,2,' s')
        self.spin_vmin=ds(self.group_prbs,0,5,0,6,' V');self.spin_vmax=ds(self.group_prbs,0,5,4,6,' V')
        for label,w in [('Bits',self.spin_prbs_bits),('Seed',self.spin_prbs_seed),('Tb_var',self.spin_var_tb),('Sampling period (s)',self.spin_ts),('Session duration (s)',self.spin_collection_time),('Minimum',self.spin_vmin),('Maximum',self.spin_vmax)]:f.addRow(label,w)
        left.addWidget(self.group_prbs);self.group_collection=QGroupBox('Collection indicators');fi=QFormLayout(self.group_collection)
        self.label_collection_sample=QLabel('0 / 0');self.label_collection_u=QLabel('0.0000 V');self.label_collection_y=QLabel('0.0000 V');self.label_cycle_time=QLabel('0.0000 s')
        for label,w in [('Applied input',self.label_collection_u),('Output y',self.label_collection_y)]:fi.addRow(label,w)
        left.addWidget(self.group_collection);left.addStretch()
        self.prbs_plot_container=QWidget();self.prbs_plot_layout=QVBoxLayout(self.prbs_plot_container);prbs_main.addWidget(self.prbs_plot_container,1)

        # NCbT/Arduino tab
        self.tab_ncbt=QWidget();self.tabs.addTab(self.tab_ncbt,'NCbT');ncbt_outer=QVBoxLayout(self.tab_ncbt);self.ncbt_scroll=QScrollArea(self.tab_ncbt);self.ncbt_scroll.setWidgetResizable(True);self.ncbt_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded);self.ncbt_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded);self.ncbt_scroll_content=QWidget();mid=QHBoxLayout(self.ncbt_scroll_content);self.ncbt_scroll.setWidget(self.ncbt_scroll_content);ncbt_outer.addWidget(self.ncbt_scroll)
        col1=QVBoxLayout();mid.addLayout(col1,1);self.group_arduino=QGroupBox('NI-DAQ hardware');fa=QFormLayout(self.group_arduino)
        serial_row=QHBoxLayout();self.combo_device=QComboBox();self.button_refresh=QPushButton('Refresh');serial_row.addWidget(self.combo_device,1);serial_row.addWidget(self.button_refresh)
        fa.addRow('Device',serial_row);self.combo_ai=QComboBox();self.combo_ao=QComboBox();
        self.combo_terminal=QComboBox();self.combo_terminal.addItems(['Diff','RSE','NRSE'])
        for label,w in [('AI channels',self.combo_ai),('AO channels',self.combo_ao),('Terminal configuration',self.combo_terminal)]:fa.addRow(label,w)
        col1.addWidget(self.group_arduino);self.group_limits=QGroupBox('Control limits');fl=QFormLayout(self.group_limits);self.spin_umin=ds(self.group_limits,0,5,0,6,' V');self.spin_umax=ds(self.group_limits,0,5,4,6,' V');fl.addRow('Minimum',self.spin_umin);fl.addRow('Maximum',self.spin_umax);col1.addWidget(self.group_limits);col1.addStretch()
        col2=QVBoxLayout();mid.addLayout(col2,1);self.group_ncbt=QGroupBox('NCbT open-loop parameters');fn=QFormLayout(self.group_ncbt)
        self.spin_l=spin(self.group_ncbt,1,10000,20);self.edit_num_M=QLineEdit('[0, 0, 0, 0.0090559170]');self.edit_den_M=QLineEdit('[1, -1.8096748361, 0.8187307531]');self.edit_beta=QPlainTextEdit('[\n    ([1], [1, -1]),\n    ([0, 1], [1, -1]),\n]');self.edit_beta.setMinimumHeight(100)
        fn.addRow('l',self.spin_l);fn.addRow('num_M',self.edit_num_M);fn.addRow('den_M',self.edit_den_M);fn.addRow('beta',self.edit_beta);col2.addWidget(self.group_ncbt)
        self.group_result=QGroupBox('Estimated controller');fr=QFormLayout(self.group_result);self.edit_rho=QPlainTextEdit();self.edit_rho.setReadOnly(True);self.label_samples_used=QLabel('0');self.label_estimation_time=QLabel('0.0000 s');self.label_design_status=QLabel('Not estimated')
        fr.addRow('ρ',self.edit_rho);fr.addRow('Samples',self.label_samples_used);fr.addRow('Estimation time (s)',self.label_estimation_time);fr.addRow('Status',self.label_design_status);col2.addWidget(self.group_result)

        # Control tab
        self.tab_control=QWidget();self.tabs.addTab(self.tab_control,'Real-Time Control');ctl=QHBoxLayout(self.tab_control);ctl_left=QVBoxLayout();ctl.addLayout(ctl_left,0)
        self.group_control=QGroupBox('Control parameters');fc=QFormLayout(self.group_control);self.spin_setpoint=ds(self.group_control,-100000,100000,2,6,' V');self.spin_control_time=ds(self.group_control,0.1,3600,10,2,' s')
        fc.addRow('Setpoint',self.spin_setpoint);self.button_apply_setpoint=QPushButton('APPLY');self.button_apply_setpoint.setObjectName('button_apply_setpoint');fc.addRow('',self.button_apply_setpoint);fc.addRow('Session duration (s)',self.spin_control_time);ctl_left.addWidget(self.group_control)
        self.group_control_ind=QGroupBox('Real-time indicators');fic=QFormLayout(self.group_control_ind);self.label_control_sample=QLabel('0 / 0');self.label_current_y=QLabel('0.0000 V');self.label_current_u=QLabel('0.0000 V');self.label_raw_u=QLabel('0.0000 V');self.label_saturation=QLabel('No');self.label_overruns=QLabel('0')
        for label,w in [('Output y',self.label_current_y),('Input u',self.label_current_u)]:fic.addRow(label,w)
        ctl_left.addWidget(self.group_control_ind);ctl_left.addStretch();self.control_plot_container=QWidget();self.control_plot_layout=QVBoxLayout(self.control_plot_container);ctl.addWidget(self.control_plot_container,1)

        # Footer
        footer=QHBoxLayout();self.check_save=QCheckBox('Save data');self.edit_path=QLineEdit();self.button_browse=QPushButton('Browse');self.button_start=QPushButton('START COMPLETE CYCLE');self.button_stop=QPushButton('STOP');self.button_close=QPushButton('CLOSE')
        self.pushButton_startstop=self.button_start;self.pushButton_close=self.button_close
        footer.addWidget(self.check_save);footer.addWidget(self.edit_path,1);footer.addWidget(self.button_browse);footer.addWidget(self.button_start);footer.addWidget(self.button_stop);footer.addWidget(self.button_close);self.mainLayout.addLayout(footer)
        self.button_stop.setEnabled(False)
        self.retranslateUi(dialog);QMetaObject.connectSlotsByName(dialog)
    def retranslateUi(self,dialog):dialog.setWindowTitle('PYDAQ - Data-Driven Control')
