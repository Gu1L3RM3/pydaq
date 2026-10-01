import ast,time,threading,traceback
from pathlib import Path
import numpy as np
from PySide6.QtCore import QObject,QThread,QTimer,Signal,Slot
from PySide6.QtWidgets import QDialog,QFileDialog,QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy import signal as ss
from pydaq.utils.base import NIDAQ_AVAILABLE,nidaqmx,TerminalConfiguration
from pydaq.utils.signals import Signal as PydaqSignal
from pydaq.data_driven_control import DataDrivenControl,DataDrivenController,validate_beta
from ..uis.ui_PyDAQ_data_driven_control_nidaq_window_dialog import Ui_Dialog_Plot_Data_Driven_NIDAQ_Window
SAFE=0.0
from .ddc_matrix_inputs import install_matrix_inputs

class Worker(QObject):
 state=Signal(str);status=Signal(str);progress=Signal(int);sample=Signal(object);ctl=Signal(object);designed=Signal(object);error=Signal(str);finished=Signal(object)
 def __init__(self,c):super().__init__();self.c=c;self.stop=threading.Event();self.data={k:[] for k in ['tc','uc','yc','tt','rr','yt','ut']};self.over=0
 def halt(self):self.stop.set()
 def sim(self):
  b,a,_=ss.cont2discrete((self.c['pn'],self.c['pd']),self.c['Ts']);return [np.asarray(b).ravel(),np.asarray(a).ravel(),np.zeros(np.asarray(b).size),np.zeros(max(np.asarray(a).size-1,0))]
 def simstep(self,u,s):
  b,a,x,y=s;x[1:]=x[:-1];x[0]=u;o=(np.dot(b,x)-np.dot(a[1:],y))/a[0] if y.size else np.dot(b,x)/a[0];
  if y.size:y[1:]=y[:-1];y[0]=o
  return float(o)
 def wait(self,t):
  d=t-time.perf_counter();time.sleep(d) if d>0 else setattr(self,'over',self.over+1)
 @Slot()
 def run(self):
  ao=ai=None;rho=None
  try:
   c=self.c;simstate=self.sim() if c['simulate'] else None
   if not c['simulate']:
    ao=nidaqmx.Task();ai=nidaqmx.Task();ao.ao_channels.add_ao_voltage_chan(c['ao'],min_val=c['umin'],max_val=c['umax']);ai.ai_channels.add_ai_voltage_chan(c['ai'],terminal_config={'Diff':TerminalConfiguration.DIFFERENTIAL,'RSE':TerminalConfiguration.RSE,'NRSE':TerminalConfiguration.NRSE}[c['terminal']]);ao.write(SAFE)
   self.state.emit('COLLECTING');g=PydaqSignal(c['bits'],c['seed'],c['tb']);p=np.asarray(g.prbs_final(cycles=c['cycles'],ao_max=c['vmax']-c['vmin'])).ravel();p=np.resize(p,c['cycles'])+c['vmin'];start=time.perf_counter()
   for k,u in enumerate(p):
    if self.stop.is_set():raise RuntimeError('Stopped')
    u=float(np.clip(u,c['umin'],c['umax']));
    if c['simulate']:y=self.simstep(u,simstate)
    else:ao.write(u);y=float(ai.read())
    t=time.perf_counter()-start;self.data['tc'].append(t);self.data['uc'].append(u);self.data['yc'].append(y);self.sample.emit((k+1,c['cycles'],t,u,y));self.progress.emit(int(100*(k+1)/c['cycles']));self.wait(start+(k+1)*c['Ts'])
   if ao:ao.write(SAFE)
   y=np.asarray(self.data['yc']);
   if np.ptp(y)<.01:raise ValueError('Measured output is constant. NCbT was not executed.')
   self.state.emit('DESIGNING');d=DataDrivenControl(beta=c['beta'],setpoint=c['sp'],period=c['Ts']);rho=np.asarray(d.tune_ncbt_open_loop(self.data['uc'],self.data['yc'],c['numM'],c['denM'],c['Ts'],self.data['tc'],c['l'],c['beta']));ctrl=DataDrivenController(rho,c['beta']);self.designed.emit(rho)
   self.state.emit('CONTROLLING');self.progress.emit(0);n=int(c['ct']/c['Ts'])+1;u=SAFE;start=time.perf_counter()
   for k in range(n):
    if self.stop.is_set():break
    if c['simulate']:y=self.simstep(u,simstate)
    else:ao.write(u);y=float(ai.read())
    raw=ctrl.update(c['sp']-y);u=float(np.clip(raw,c['umin'],c['umax']));t=time.perf_counter()-start;self.data['tt'].append(t);self.data['rr'].append(c['sp']);self.data['yt'].append(y);self.data['ut'].append(u);self.ctl.emit((k+1,n,t,c['sp'],y,u,self.over));self.progress.emit(int(100*(k+1)/n));self.wait(start+(k+1)*c['Ts'])
   self.state.emit('FINISHED');self.finished.emit({'rho':rho,'data':self.data})
  except Exception as e:traceback.print_exc();self.error.emit(f'{type(e).__name__}: {e}');self.finished.emit({'rho':rho,'data':self.data})
  finally:
   try:
    if ao:ao.write(SAFE);ao.close()
    if ai:ai.close()
   except:pass
class Data_Driven_Control_NIDAQ_Window_Dialog(QDialog,Ui_Dialog_Plot_Data_Driven_NIDAQ_Window):
 def __init__(self,parent=None):
  super().__init__(parent);self.setupUi(self);install_matrix_inputs(self,[('edit_num_M','vector'),('edit_den_M','vector'),('edit_beta','beta')]);self.worker=self.thread=None;self.result=None;self.cfg0={};self.dp={k:[] for k in ['tc','uc','yc','tt','rr','yt','ut']};self.makeplots();self.button_refresh.clicked.connect(self.refresh);self.combo_device.currentIndexChanged.connect(self.channels);self.button_start.clicked.connect(self.start);self.button_stop.clicked.connect(self.stop);self.button_close.clicked.connect(self.close);self.button_browse.clicked.connect(self.browse);self.refresh();self.timer=QTimer(self);self.timer.timeout.connect(self.draw);self.timer.start(150)
 def makeplots(self):
  self.f1=Figure(facecolor='#404040');self.c1=FigureCanvas(self.f1);self.prbs_plot_layout.addWidget(self.c1);self.a1=self.f1.add_subplot(111);self.f2=Figure(facecolor='#404040');self.c2=FigureCanvas(self.f2);self.control_plot_layout.addWidget(self.c2);self.a2=self.f2.add_subplot(211);self.a3=self.f2.add_subplot(212)
 def refresh(self):
  self.combo_device.clear();
  if NIDAQ_AVAILABLE:
   for d in nidaqmx.system.System.local().devices:self.combo_device.addItem(f'{d.product_type} ({d.name})',d.name)
  self.channels()
 def channels(self):
  self.combo_ai.clear();self.combo_ao.clear();n=self.combo_device.currentData()
  if NIDAQ_AVAILABLE and n:
   d=nidaqmx.system.device.Device(n);self.combo_ai.addItems(d.ai_physical_chans.channel_names);self.combo_ao.addItems(d.ao_physical_chans.channel_names)
 def set_parameters(self,device,ai,ao,terminal,Ts,sp,beta,numM,denM,l,simulate,pn,pd,path='',save=False):self.cfg0=dict(device=device,ai=ai,ao=ao,terminal=terminal,Ts=Ts,sp=sp,beta=beta,numM=numM,denM=denM,l=l,simulate=simulate,pn=pn,pd=pd);self.edit_path.setText(path);self.check_save.setChecked(save);self.spin_ts.setValue(Ts);self.spin_setpoint.setValue(sp);self.combo_terminal.setCurrentText(terminal);self.edit_beta.setPlainText(repr(beta));self.edit_num_M.setText(repr(list(numM)));self.edit_den_M.setText(repr(list(denM)))
 def cfg(self):
  c=self.cfg0.copy();c.update(device=self.combo_device.currentData(),ai=self.combo_ai.currentText(),ao=self.combo_ao.currentText(),terminal=self.combo_terminal.currentText(),Ts=self.spin_ts.value(),sp=self.spin_setpoint.value(),beta=ast.literal_eval(self.edit_beta.toPlainText()),numM=ast.literal_eval(self.edit_num_M.text()),denM=ast.literal_eval(self.edit_den_M.text()),l=self.spin_l.value(),bits=self.spin_prbs_bits.value(),seed=self.spin_prbs_seed.value(),tb=self.spin_var_tb.value(),cycles=int(self.spin_collection_time.value()/self.spin_ts.value())+1,vmin=self.spin_vmin.value(),vmax=self.spin_vmax.value(),umin=self.spin_umin.value(),umax=self.spin_umax.value(),ct=self.spin_control_time.value(),pn=np.asarray(ast.literal_eval(c.get('pn','[1]')),float),pd=np.asarray(ast.literal_eval(c.get('pd','[1,1]')),float));validate_beta(c['beta']);return c
 def start(self):
  try:c=self.cfg()
  except Exception as e:QMessageBox.warning(self,'Configuration',str(e));return
  self.worker=Worker(c);self.thread=QThread(self);self.worker.moveToThread(self.thread);self.thread.started.connect(self.worker.run);self.worker.state.connect(self.state);self.worker.status.connect(self.label_status.setText);self.worker.progress.connect(self.progressBar.setValue);self.worker.sample.connect(self.sample);self.worker.ctl.connect(self.control);self.worker.designed.connect(lambda r:self.edit_rho.setPlainText(np.array2string(r)));self.worker.error.connect(self.worker_error);self.worker.finished.connect(self.done);self.worker.finished.connect(self.thread.quit);self.button_start.setEnabled(False);self.button_stop.setEnabled(True);self.thread.start()
 @Slot(str)
 def worker_error(self,e):QMessageBox.critical(self,'NI-DAQ',e)
 def state(self,s):self.label_state.setText(s);self.tabs.setCurrentWidget(self.tab_prbs if s=='COLLECTING' else self.tab_ncbt if s=='DESIGNING' else self.tab_control)
 def sample(self,v):k,n,t,u,y=v;self.dp['tc'].append(t);self.dp['uc'].append(u);self.dp['yc'].append(y)
 def control(self,v):k,n,t,r,y,u,o=v;self.dp['tt'].append(t);self.dp['rr'].append(r);self.dp['yt'].append(y);self.dp['ut'].append(u);self.label_current.setText(f'{y:.4f} V');self.label_action.setText(f'{u:.4f} V');self.label_overruns.setText(str(o))
 def stop(self):
  if self.worker:self.worker.halt()
 def done(self,r):self.result=r;self.button_start.setEnabled(True);self.button_stop.setEnabled(False)
 def browse(self):
  p=QFileDialog.getExistingDirectory(self,'Output directory');self.edit_path.setText(p) if p else None
 def draw(self):
  for a in [self.a1,self.a2,self.a3]:a.clear();a.set_facecolor('#404040');a.tick_params(colors='white')
  self.a1.plot(self.dp['tc'],self.dp['uc'],label='u');self.a1.plot(self.dp['tc'],self.dp['yc'],label='y');self.a1.legend();self.a2.plot(self.dp['tt'],self.dp['rr'],label='r');self.a2.plot(self.dp['tt'],self.dp['yt'],label='y');self.a2.legend();self.a3.plot(self.dp['tt'],self.dp['ut'],label='u');self.a3.legend();self.c1.draw_idle();self.c2.draw_idle()
