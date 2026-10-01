"""Automatic PRBS collection, NCbT estimation and real-time control."""
import ast, os, time, threading, traceback
from pathlib import Path
import numpy as np
import serial
import serial.tools.list_ports
from PySide6.QtCore import QObject,QThread,QTimer,Signal,Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog,QFileDialog,QMessageBox,QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import signal as scipy_signal
from pydaq.utils.base import Base
from pydaq.utils.signals import Signal as PydaqSignal
from pydaq.data_driven_control import DataDrivenControl,DataDrivenController,validate_beta
from ..uis.ui_PyDAQ_data_driven_control_window_dialog import Ui_Dialog_Plot_Data_Driven_Window

ARDUINO_BAUD_RATE = 115200
ARDUINO_ADC_MIN = 0.0
ARDUINO_ADC_MAX = 5.0
ARDUINO_SAFE_OUTPUT = 0.0

from .ddc_matrix_inputs import install_matrix_inputs

class ExperimentWorker(QObject):
    state=Signal(str);status=Signal(str);progress=Signal(int);collection_sample=Signal(object);control_sample=Signal(object);designed=Signal(object);error=Signal(str);finished=Signal(object)
    def __init__(self,cfg):
        super().__init__();self.cfg=cfg;self.stop_event=threading.Event();self.ser=None;self.overruns=0
        self.t_col=[];self.u_col=[];self.y_col=[];self.requested=[];self.t_ctl=[];self.r_ctl=[];self.y_ctl=[];self.u_ctl=[];self.raw_ctl=[];self.pwm_ctl=[];self.valid_frames=0;self.invalid_frames=0;self.timeouts=0;self.last_raw_adc=None;self.last_frame=b''
    def request_stop(self):self.stop_event.set()
    def _set_state(self,s):self.state.emit(s)
    def _open(self):
        if self.cfg['simulate']:
            return
        self.ser = serial.Serial(
            self.cfg['port'],
            self.cfg['baud'],
            timeout=max(0.20, 5 * self.cfg['Ts']),
            write_timeout=max(0.20, 5 * self.cfg['Ts']),
        )
        time.sleep(2.0)
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        # Same warm-up command used by PYDAQ GetModel.
        self.ser.write(b"0")
        self.ser.flush()
        self.ser.reset_input_buffer()
        _ = self.ser.readline()

    def _send_only(self, voltage):
        """Send an output without waiting for an acquisition frame."""
        voltage = float(np.clip(voltage, self.cfg['u_min'], self.cfg['u_max']))
        if not self.cfg['simulate'] and self.ser is not None and self.ser.is_open:
            duty = int(np.clip(round(255 * voltage / 5.0), 0, 255))
            message = f"{self.cfg['pwm_pin']}:{duty}\n"
            self.ser.write(message.encode())
            self.ser.flush()
        return voltage

    def _exchange(self, voltage):
        """Send one PWM command and read its acknowledgement and ADC frame."""
        if self.stop_event.is_set():
            raise RuntimeError('Experiment stopped.')

        voltage = float(np.clip(voltage, self.cfg['u_min'], self.cfg['u_max']))
        duty = int(np.clip(round(255 * voltage / 5.0), 0, 255))
        message = f"{self.cfg['pwm_pin']}:{duty}\n"

        self.ser.write(message.encode())
        self.ser.flush()
        self.ser.reset_input_buffer()

        acknowledgement = self.ser.readline()
        raw_frame = self.ser.readline()

        if not raw_frame:
            self.timeouts += 1
            raise TimeoutError('Arduino did not return the analog frame.')

        fields = raw_frame.decode('utf-8', errors='ignore').strip().split(',')
        if len(fields) < 6:
            self.invalid_frames += 1
            raise ValueError(
                f"Incomplete Arduino frame: {raw_frame!r}; "
                f"acknowledgement: {acknowledgement!r}"
            )

        try:
            raw_adc = int(fields[self.cfg['ai_index']])
        except (ValueError, IndexError) as exc:
            self.invalid_frames += 1
            raise ValueError(f"Invalid Arduino ADC frame: {raw_frame!r}") from exc

        self.valid_frames += 1
        self.last_raw_adc = raw_adc
        self.last_frame = raw_frame
        measured = (
            self.cfg['adc_min']
            + raw_adc
            * (self.cfg['adc_max'] - self.cfg['adc_min'])
            / 1023.0
        )
        return voltage, float(measured), raw_adc, raw_frame
    def _wait(self,target):
        delay=target-time.perf_counter()
        if delay>0:time.sleep(delay)
        else:self.overruns+=1
    def _make_simulator(self):
        num=self.cfg['plant_num'];den=self.cfg['plant_den'];Ts=self.cfg['Ts']
        bz,az,_=scipy_signal.cont2discrete((num,den),Ts,method='zoh');return np.asarray(bz).reshape(-1),np.asarray(az).reshape(-1),np.zeros(np.asarray(bz).size),np.zeros(max(np.asarray(az).size-1,0))
    @staticmethod
    def _sim_step(u,state):
        b,a,xh,yh=state
        if xh.size>1:xh[1:]=xh[:-1]
        xh[0]=u;y=float(np.dot(b,xh))
        if yh.size:y-=float(np.dot(a[1:],yh))
        y/=a[0]
        if yh.size>1:yh[1:]=yh[:-1]
        if yh.size:yh[0]=y
        return y
    def _collect(self):
        self._set_state('COLLECTING');self.status.emit('Applying PRBS and collecting open-loop data...')
        g=PydaqSignal(self.cfg['prbs_bits'],self.cfg['prbs_seed'],self.cfg['var_tb']);span=self.cfg['v_max']-self.cfg['v_min']
        prbs=np.asarray(g.prbs_final(cycles=self.cfg['cycles'],ao_max=span),dtype=float).reshape(-1)
        if prbs.size<self.cfg['cycles']:prbs=np.tile(prbs,int(np.ceil(self.cfg['cycles']/prbs.size)))
        prbs=np.clip(prbs[:self.cfg['cycles']]+self.cfg['v_min'],self.cfg['v_min'],self.cfg['v_max'])
        sim=self._make_simulator() if self.cfg['simulate'] else None;start=time.perf_counter()
        for k,requested in enumerate(prbs):
            if self.stop_event.is_set():raise RuntimeError('Experiment stopped by the user.')
            tick = time.perf_counter()
            if sim:
                applied = float(np.clip(requested, self.cfg['u_min'], self.cfg['u_max']))
                measured = self._sim_step(applied, sim)
                raw_adc = None
            else:
                applied, measured, raw_adc, _ = self._exchange(requested)
            elapsed = time.perf_counter() - start
            self.t_col.append(elapsed);self.u_col.append(applied);self.y_col.append(measured);self.requested.append(float(requested))
            self.collection_sample.emit((k+1,self.cfg['cycles'],elapsed,applied,measured,time.perf_counter()-tick,self.overruns,raw_adc,self.valid_frames,self.invalid_frames,self.timeouts));self.progress.emit(int(100*(k+1)/self.cfg['cycles']));self._wait(start+(k+1)*self.cfg['Ts'])
        self._send_only(self.cfg['safe'])
    def _design(self):
        self._set_state('DESIGNING');self.status.emit('Aligning data and estimating the NCbT controller...');tic=time.perf_counter()
        u=np.asarray(self.u_col);y=np.asarray(self.y_col);t=np.asarray(self.t_col)
        if u.size < max(20, 2 * self.cfg['l'] + 1):
            raise ValueError('Insufficient samples for NCbT estimation.')
        if not np.all(np.isfinite(y)) or np.ptp(y) < 0.01:
            raise ValueError(
                'Measured output is constant or invalid. NCbT was not executed. '
                'Check the Arduino frame and A0 reading.'
            )
        if self.cfg['simulate']:ua,ya,ta=u,y,t
        else:ua,ya,ta=u[:-1],y[1:],t[:-1]
        ddc=DataDrivenControl(rho=None,beta=self.cfg['beta'],setpoint=self.cfg['setpoint'],period=self.cfg['Ts'])
        rho=ddc.tune_ncbt_open_loop(ua,ya,self.cfg['num_M'],self.cfg['den_M'],self.cfg['Ts'],ta,self.cfg['l'],self.cfg['beta'])
        rho=np.asarray(rho,dtype=float).reshape(-1)
        if rho.size!=len(self.cfg['beta']) or not np.all(np.isfinite(rho)):raise ValueError('NCbT returned an invalid rho vector.')
        controller=DataDrivenController(rho,self.cfg['beta']);controller.reset();elapsed=time.perf_counter()-tic
        self.designed.emit((rho,len(ua),elapsed));self.status.emit('Controller estimated successfully. Starting real-time control...');return rho,controller
    def _control(self,controller):
        self._set_state('CONTROLLING');self.progress.emit(0);cycles=int(np.floor(self.cfg['control_time']/self.cfg['Ts']))+1
        sim=self._make_simulator() if self.cfg['simulate'] else None;start=time.perf_counter();next_control=self.cfg['safe']
        for k in range(cycles):
            if self.stop_event.is_set():break
            tick=time.perf_counter()
            if sim:
                applied=float(np.clip(next_control,self.cfg['u_min'],self.cfg['u_max']))
                measured=self._sim_step(applied,sim)
            else:
                applied,measured,_,_=self._exchange(next_control)
            error=self.cfg['setpoint']-measured
            raw=float(controller.update(error));next_control=float(np.clip(raw,self.cfg['u_min'],self.cfg['u_max']));elapsed=time.perf_counter()-start
            pwm_level=int(np.clip(round(255.0*applied/5.0),0,255))
            self.t_ctl.append(elapsed);self.r_ctl.append(self.cfg['setpoint']);self.y_ctl.append(measured);self.u_ctl.append(applied);self.raw_ctl.append(raw);self.pwm_ctl.append(pwm_level)
            sat=not np.isclose(raw,applied);self.control_sample.emit((k+1,cycles,elapsed,self.cfg['setpoint'],measured,applied,raw,sat,self.overruns,pwm_level));self.progress.emit(int(100*(k+1)/cycles));self._wait(start+(k+1)*self.cfg['Ts'])
        self._send_only(self.cfg['safe'])
    @Slot()
    def run(self):
        result={'ok':False}
        try:
            self._set_state('CONNECTING');self.status.emit('Opening the experiment...');self._open();self._collect();rho,controller=self._design();self._control(controller);result={'ok':True,'rho':rho,'data':self.data()};self._set_state('FINISHED');self.status.emit('Complete cycle finished.')
        except Exception as exc:
            if self.stop_event.is_set():self._set_state('STOPPED');self.status.emit('Experiment stopped safely.')
            else:self._set_state('ERROR');traceback.print_exc();self.error.emit(f'{type(exc).__name__}: {exc}')
            result={'ok':False,'data':self.data()}
        finally:
            try:
                if self.ser and self.ser.is_open:self._send_only(self.cfg['safe']);self.ser.close()
            except Exception:pass
            self.finished.emit(result)
    def data(self):return {'collection_time':self.t_col,'collection_input':self.u_col,'collection_output':self.y_col,'requested_prbs':self.requested,'control_time':self.t_ctl,'reference':self.r_ctl,'measurement':self.y_ctl,'control_action':self.u_ctl,'raw_control':self.raw_ctl,'pwm_level':self.pwm_ctl,'valid_frames':[self.valid_frames],'invalid_frames':[self.invalid_frames],'timeouts':[self.timeouts]}

class Data_Driven_Control_Window_Dialog(QDialog,Ui_Dialog_Plot_Data_Driven_Window,Base):
    send_values=Signal(str,float)
    def __init__(self,*args):
        super().__init__();self.setupUi(self);install_matrix_inputs(self,[('edit_num_M','vector'),('edit_den_M','vector'),('edit_beta','beta')]);self.worker=None;self.thread=None;self.last_result=None;self._incoming={};self._make_plots();self._connect();self.refresh_ports();self._recalculate()
        self.timer=QTimer(self);self.timer.timeout.connect(self._draw);self.timer.start(100)
    def _make_plots(self):
        self.fig_prbs=Figure(figsize=(7,5),facecolor='#404040');self.canvas_prbs=FigureCanvas(self.fig_prbs);self.prbs_plot_layout.addWidget(self.canvas_prbs);self.ax_prbs=self.fig_prbs.add_subplot(111)
        self.fig_ctl=Figure(figsize=(7,5),facecolor='#404040');self.canvas_ctl=FigureCanvas(self.fig_ctl);self.control_plot_layout.addWidget(self.canvas_ctl);self.ax_y=self.fig_ctl.add_subplot(211);self.ax_u=self.fig_ctl.add_subplot(212);self.ax_pwm=self.ax_u.twinx();self.fig_ctl.tight_layout()
        self._style_axes([self.ax_prbs,self.ax_y,self.ax_u,self.ax_pwm])
        self.plot_data={'tc':[],'uc':[],'yc':[],'tt':[],'rr':[],'yt':[],'ut':[],'pwm':[]}
    @staticmethod
    def _style_axes(axes):
        for ax in axes:ax.set_facecolor('#404040');ax.tick_params(colors='white');[s.set_color('white') for s in ax.spines.values()];ax.xaxis.label.set_color('white');ax.yaxis.label.set_color('white');ax.title.set_color('white')
    def _connect(self):
        self.button_refresh.clicked.connect(self.refresh_ports);self.button_start.clicked.connect(self.start_complete_cycle);self.button_stop.clicked.connect(self.stop_cycle);self.button_close.clicked.connect(self.close);self.button_browse.clicked.connect(self.browse)
        for w in [self.spin_ts,self.spin_collection_time,self.spin_vmin,self.spin_vmax]:w.valueChanged.connect(self._recalculate)
    @Slot()
    def refresh_ports(self):
        current=self.combo_serial.currentData();self.combo_serial.clear()
        for p in serial.tools.list_ports.comports():self.combo_serial.addItem(f'{p.device} - {p.description}',p.device)
        if current:
            i=self.combo_serial.findData(current)
            if i>=0:self.combo_serial.setCurrentIndex(i)
    def _recalculate(self):
        # Cycles and PRBS amplitude are derived internally from Ts, duration,
        # minimum voltage and maximum voltage. No duplicate UI fields are needed.
        return
    @staticmethod
    def _parse(text,name):
        try:value=ast.literal_eval(text)
        except Exception as exc:raise ValueError(f'Invalid {name}. Use Python list syntax.') from exc
        return np.asarray(value,dtype=float).reshape(-1)
    def _cfg(self):
        beta=ast.literal_eval(self.edit_beta.toPlainText());validate_beta(beta);simulate=bool(self._incoming.get('simulate',False));port=self.combo_serial.currentData()
        if not simulate and not port:raise ValueError('Select an Arduino serial port.')
        if self.spin_vmin.value()>=self.spin_vmax.value():raise ValueError('Minimum PRBS voltage must be below maximum.')
        if self.spin_umin.value()>=self.spin_umax.value():raise ValueError('Minimum control output must be below maximum.')
        if not self.spin_umin.value() <= ARDUINO_SAFE_OUTPUT <= self.spin_umax.value():
            raise ValueError('Control limits must include the fixed safe output of 0 V.')
        cfg={'simulate':simulate,'port':port,'baud':ARDUINO_BAUD_RATE,'ai_index':int(self.combo_ai.currentText()[1:]),'pwm_pin':int(self.combo_pwm.currentText()[1:]),'adc_min':ARDUINO_ADC_MIN,'adc_max':ARDUINO_ADC_MAX,'safe':ARDUINO_SAFE_OUTPUT,'u_min':self.spin_umin.value(),'u_max':self.spin_umax.value(),'Ts':self.spin_ts.value(),'collection_time':self.spin_collection_time.value(),'cycles':int(np.floor(self.spin_collection_time.value()/self.spin_ts.value()))+1,'prbs_bits':self.spin_prbs_bits.value(),'prbs_seed':self.spin_prbs_seed.value(),'var_tb':int(self.spin_var_tb.value()),'v_min':self.spin_vmin.value(),'v_max':self.spin_vmax.value(),'l':self.spin_l.value(),'num_M':self._parse(self.edit_num_M.text(),'num_M'),'den_M':self._parse(self.edit_den_M.text(),'den_M'),'beta':beta,'setpoint':self.spin_setpoint.value(),'control_time':self.spin_control_time.value(),'plant_num':self._parse(self._incoming.get('numerator','[1]'),'plant numerator'),'plant_den':self._parse(self._incoming.get('denominator','[1,1]'),'plant denominator')}
        return cfg
    @Slot()
    def start_complete_cycle(self):
        if self.thread and self.thread.isRunning():return
        try:cfg=self._cfg()
        except Exception as exc:QMessageBox.warning(self,'Invalid configuration',str(exc));return
        for k in self.plot_data:self.plot_data[k]=[]
        self.worker=ExperimentWorker(cfg);self.thread=QThread(self);self.worker.moveToThread(self.thread);self.thread.started.connect(self.worker.run);self.worker.state.connect(self._state);self.worker.status.connect(self.label_status.setText);self.worker.progress.connect(self.progressBar.setValue);self.worker.collection_sample.connect(self._col_sample);self.worker.control_sample.connect(self._ctl_sample);self.worker.designed.connect(self._designed);self.worker.error.connect(self._worker_error);self.worker.finished.connect(self._finished);self.worker.finished.connect(self.thread.quit);self.worker.finished.connect(self.worker.deleteLater);self.thread.finished.connect(self.thread.deleteLater)
        self.button_start.setEnabled(False);self.button_stop.setEnabled(True);self.thread.start()
    @Slot()
    def stop_cycle(self):
        if self.worker:self.worker.request_stop()
        self.button_stop.setEnabled(False);self.label_status.setText('Stopping safely...')
    @Slot(str)
    def _state(self,state):
        self.label_state.setText(state)
        if state=='COLLECTING':self.tabs.setCurrentWidget(self.tab_prbs)
        elif state=='DESIGNING':self.tabs.setCurrentWidget(self.tab_ncbt)
        elif state=='CONTROLLING':self.tabs.setCurrentWidget(self.tab_control)
    @Slot(object)
    def _col_sample(self,item):
        k,n,t,u,y,cycle,over,raw_adc,valid,invalid,timeouts=item;self.label_collection_sample.setText(f'{k} / {n}');self.label_collection_u.setText(f'{u:.4f} V');self.label_collection_y.setText(f'{y:.4f} V' + (f' | ADC {raw_adc}' if raw_adc is not None else ''));self.label_cycle_time.setText(f'{cycle:.5f} s | valid {valid}, invalid {invalid}, timeout {timeouts}');self.plot_data['tc'].append(t);self.plot_data['uc'].append(u);self.plot_data['yc'].append(y)
    @Slot(object)
    def _ctl_sample(self,item):
        k,n,t,r,y,u,raw,sat,over,pwm_level=item;self.label_control_sample.setText(f'{k} / {n}');self.label_current_y.setText(f'{y:.4f} V');self.label_current_u.setText(f'{u:.4f} V');self.label_raw_u.setText(f'{raw:.4f} V');self.label_saturation.setText('Yes' if sat else 'No');self.label_overruns.setText(str(over));self.plot_data['tt'].append(t);self.plot_data['rr'].append(r);self.plot_data['yt'].append(y);self.plot_data['ut'].append(u);self.plot_data['pwm'].append(pwm_level)
    @Slot(object)
    def _designed(self,item):
        rho,n,elapsed=item;self.edit_rho.setPlainText(np.array2string(rho,precision=10,separator=', '));self.label_samples_used.setText(str(n));self.label_estimation_time.setText(f'{elapsed:.5f} s');self.label_design_status.setText('Valid');self.rho=rho
    @Slot(str)
    def _worker_error(self,message):
        self.label_status.setText(message)
        QMessageBox.critical(self,'Data-Driven Control',message)

    @Slot(object)
    def _finished(self,result):
        self.last_result=result;self.button_start.setEnabled(True);self.button_stop.setEnabled(False);self.worker=None;self.thread=None
        if self.check_save.isChecked() and self.edit_path.text().strip():self.save_data(self.edit_path.text().strip())
    def _draw(self):
        self.ax_prbs.clear();self._style_axes([self.ax_prbs]);self.ax_prbs.plot(self.plot_data['tc'],self.plot_data['uc'],label='Input u',color='#33aaff');self.ax_prbs.plot(self.plot_data['tc'],self.plot_data['yc'],label='Output y',color='#ff5555');self.ax_prbs.set_xlabel('Time (s)');self.ax_prbs.set_ylabel('Voltage (V)');self.ax_prbs.legend();self.canvas_prbs.draw_idle()
        self.ax_y.clear();self.ax_u.clear();self.ax_pwm.clear();self._style_axes([self.ax_y,self.ax_u,self.ax_pwm]);self.ax_y.plot(self.plot_data['tt'],self.plot_data['rr'],label='Reference',color='#66ff66');self.ax_y.plot(self.plot_data['tt'],self.plot_data['yt'],label='Measurement',color='#ff5555');self.ax_y.legend();self.ax_y.set_ylabel('Voltage (V)');control_lines=self.ax_u.plot(self.plot_data['tt'],self.plot_data['ut'],label='Control u',color='#33aaff',linewidth=1.5);pwm_lines=self.ax_pwm.step(self.plot_data['tt'],self.plot_data['pwm'],where='post',label='PWM',color='#ffb347',linewidth=0.8,alpha=0.85);legend=self.ax_u.legend(control_lines+pwm_lines,[line.get_label() for line in control_lines+pwm_lines],loc='upper center',bbox_to_anchor=(0.5,1.02),ncol=2,framealpha=0.9);legend.set_zorder(1000);self.ax_u.set_xlabel('Time (s)');self.ax_u.set_ylabel('Control u (V)');self.ax_pwm.yaxis.set_label_position('right');self.ax_pwm.yaxis.tick_right();self.ax_pwm.set_ylabel('PWM',color='#ffb347',labelpad=12);self.ax_pwm.set_ylim(-5,260);self.ax_pwm.set_yticks([0,64,128,192,255]);self.ax_pwm.tick_params(axis='y',colors='#ffb347',pad=4);self.canvas_ctl.draw_idle()
    @Slot()
    def browse(self):
        p=QFileDialog.getExistingDirectory(self,'Choose output directory',self.edit_path.text() or str(Path.home()/'Desktop'))
        if p:self.edit_path.setText(p)
    def save_data(self,path):
        Path(path).mkdir(parents=True,exist_ok=True)
        if not self.last_result:return
        d=self.last_result.get('data',{})
        for name,values in d.items():np.savetxt(Path(path)/f'{name}.dat',np.asarray(values),delimiter=',')
        if self.last_result.get('rho') is not None:np.savetxt(Path(path)/'rho.dat',np.asarray(self.last_result['rho']),delimiter=',')
        (Path(path)/'beta.txt').write_text(self.edit_beta.toPlainText(),encoding='utf-8')
    # Compatibility with the previous outer widget.
    def check_board(self,board,hardware_id,ao,ai,terminal,simulate):
        self._incoming['simulate']=bool(simulate)
        if hardware_id:
            i=self.combo_serial.findData(hardware_id)
            if i>=0:self.combo_serial.setCurrentIndex(i)
        if ao:self.combo_pwm.setCurrentText(str(ao[0]));
        if ai:self.combo_ai.setCurrentText(str(ai[0]));
    def set_parameters(self,rho,beta,numerator,denominator,setpoint,unit,equationvu,equationuv,period,path,save,u_data_path=None,y_data_path=None,r_data_path=None,t_data_path=None,num_M=None,den_M=None,l=20,**kwargs):
        self._incoming.update({'numerator':numerator,'denominator':denominator,'unit':unit});self.spin_ts.setValue(float(period));self.spin_setpoint.setValue(float(setpoint));self.check_save.setChecked(bool(save));self.edit_path.setText(path or '')
        if beta is not None:self.edit_beta.setPlainText(repr(beta))
        if num_M is not None:self.edit_num_M.setText(repr(np.asarray(num_M).tolist()))
        if den_M is not None:self.edit_den_M.setText(repr(np.asarray(den_M).tolist()))
        self.spin_l.setValue(int(l));self._recalculate()
    def closeEvent(self,event):
        if self.thread and self.thread.isRunning():
            ans=QMessageBox.question(self,'Stop experiment','Stop the active experiment and close?',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if ans==QMessageBox.No:event.ignore();return
            self.stop_cycle();self.thread.wait(3000)
        event.accept()
