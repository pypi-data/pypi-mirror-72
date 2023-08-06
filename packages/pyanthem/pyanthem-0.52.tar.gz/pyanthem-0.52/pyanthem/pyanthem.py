import os, random, sys, cv2, time, csv, pickle, re
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from tkinter import StringVar, DoubleVar, Tk, Label, Entry, Button, OptionMenu, Checkbutton, Message, Menu, IntVar, Scale, HORIZONTAL
from tkinter.ttk import Progressbar, Separator, Combobox
from tkinter import filedialog as fd 
import tkinter.font as font
from scipy.io import loadmat, savemat, whosmat
from scipy.io.wavfile import write as wavwrite
from scipy.optimize import nnls
from scipy.interpolate import interp1d
from scipy.signal import resample
from pygame.mixer import Sound, init, quit, get_init, set_num_channels, pre_init
from pygame.sndarray import make_sound
from pygame.time import delay
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as tkr
import matplotlib.cm as cmaps
#https://matplotlib.org/gallery/color/colormap_reference.html
import numpy as np
from numpy.matlib import repmat
from soundfile import read
from midiutil import MIDIFile
try:
	from pyanthem.pyanthem_vars import *
except:
	from pyanthem_vars import *
from git import Repo
import pkg_resources
print('pyanthem version {}'.format(pkg_resources.require("pyanthem")[0].version))

def AE_download():
	'''
	Downloads the 'Piano' audio engine from  
	'''
	AE_path = os.path.join(os.path.dirname(__file__),'anthem_AE')
	if not os.path.isdir(AE_path):
		print('Cloning the audio engine to the pyanthem package directory...')
		try:
			Repo.clone_from('https://github.com/nicthib/anthem_AE.git',AE_path)
			print(f'Audio engine downloaded to {AE_path}')
		except:
			print('ERROR: git executable not present. Please visit https://git-scm.com/downloads to install.')
	else:
		print(f'Audio engine is already present in {AE_path}. If you want to uninstall, you must manually delete the AE folder.')

def example_data_download():
	'''
	Downloads example datasets from https://github.com/nicthib/anthem_datasets
	'''
	path = os.path.join(os.path.dirname(__file__),'anthem_datasets')
	if not os.path.isdir(path):
		print('Cloning example datasets to the pyanthem package directory...')
		try:
			Repo.clone_from('https://github.com/nicthib/anthem_datasets.git',path)
			print(f'Example datasets downloaded to {path}')
		except:
			print('ERROR: git executable not present. Please visit https://git-scm.com/downloads to install.')
	else:
		print(f'Demo data is already present in {path}. If you want to uninstall, you must manually delete the folder.')

def init_entry(fn):
	'''
	Generalized version of SringVar/DoubleVar followed by set()
	'''
	if isinstance(fn, str):
		entry = StringVar()
	else:
		entry = DoubleVar()
	entry.set(fn)
	return entry

def play_for(sample_wave, ms):
	'''
	Non-blocking playsound command
	'''
	sound = make_sound(sample_wave)
	sound.play(-1)
	delay(ms)
	sound.stop()
	
def sine_wave(hz, peak, n_samples=22000):
	'''
	Plays a sine wave - used in GUI.preview_notes()
	'''
	length = 44100 / float(hz)
	omega = np.pi * 2 / length
	xvalues = np.arange(int(length)) * omega
	onecycle = peak * np.sin(xvalues)
	sound = np.resize(onecycle, (n_samples,))
	env = np.ones(len(sound),)
	attack = int(44100*.15)
	env[:attack] = np.linspace(0,1,attack)
	env[-attack:] = np.linspace(1,0,attack)
	sound=sound*env
	sound = np.hstack((sound[:,None],sound[:,None]))
	return sound.astype(np.int16)

def run(display=True):
	'''
	main command to run GUI or CLI
	'''
	root = GUI(display=display)
	if display:
		root.mainloop()
	else:
		return root

class GUI(Tk):
	def __init__(self,display=True):
		'''
		Initializes the GUI instance. display=True runs the Tk.__init__(self)
		command, while display=False skips that and visual initialization, keeping
		the GUI 'hidden'
		'''
		self.package_path = os.path.dirname(__file__)
		self.AE_path = os.path.join(os.path.dirname(__file__),'anthem_AE')
		self.AE_run = os.path.isdir(self.AE_path)
		self.display = display
		if self.display:
			Tk.__init__(self)
			self.default_font=font.nametofont("TkDefaultFont")
			self.initGUI()
	
	def quit(self):
		'''
		quits the GUI instance. currently, jupyter instances are kinda buggy
		'''
		try:
			get_ipython().__class__.__name__
			self.destroy()
		except NameError:
			sys.exit()

	def check_data_and_save_path(self):
		'''
		Checks to make sure data and a save path are defined.
		'''
		if not hasattr(self,'data'):
			if self.display:
				self.status['text'] = 'Error: no dataset has been loaded.'
			else:
				print('Error: no dataset has been loaded.')
			return False
		if self.cfg['save_path'] is None:
			print('Error: cfg["save_path"] is empty - please provide one!')
			return False
		return True

	def self_to_cfg(self):
		'''
		This function is neccesary to allow command-line access of the GUI functions. 
		StringVar() and IntVar() allow for dynamic, quick field updating and access, 
		but cannot be used outside of a mainloop. for this reason, I convert all 
		StringVars and IntVars to a new dict called 'self.cfg', that can be accessed 
		oustide the GUI.
		'''
		self.cfg = {k: getattr(self,k).get() if self_fns[k] is 'entry' else getattr(self,k) for k in self_fns}

	def load_data(self,filein=None):
		'''
		loads dataset from filein. At the time, only supports .mat files.
		'''
		self.data = loadmat(filein)
		if (k in self.data for k in ('W','H','fr')):
			self.data['W_shape'] = self.data['W'].shape
			self.data['W'] = self.data['W'].reshape(self.data['W'].shape[0]*self.data['W'].shape[1],self.data['W'].shape[2])
			self.data['fr'] = float(self.data['fr'])
		if not self.display:
			return self

	def load_GUI(self):
		'''
		GUI-addons for load_data. Prompts user with filedialog, assigns defaults and sets GUI fields. 
		'''
		inputfile = os.path.normpath(fd.askopenfilename(title='Select .mat file for import',filetypes=[('.mat files','*.mat')]))
		if len(inputfile) < 2:
			return
		self.load_data(inputfile)
		self.data['H_pp'] = self.data['H']
		self.data['H_fp'] = self.data['H']
		self.data['W_pp'] = self.data['W']
		self.fr.set(self.data['fr'])
		self.file_in.set(os.path.splitext(os.path.split(inputfile)[1])[0])

		# Set defaults
		self.file_out.set(self.file_in.get())
		self.save_path.set(os.path.split(inputfile)[0])
		Hstr = 'H'
		self.brightness.set(f'{float(f"{np.max(self.data[Hstr]):.3g}"):g}')
		self.threshold.set(f'{float(f"{np.mean(self.data[Hstr]):.3g}"):g}')
		self.Wshow_arr = list(range(len(self.data['H'])))
		self.status['text'] = 'Status: File load successful!'
		self.self_to_cfg()
		self.refresh_GUI()
	
	def dump_config(self):
		'''
		Saves config file. This is run every time a user calls write_audio() or write_video()
		'''
		if not hasattr(self,'data'):
			return
		file_out = os.path.join(self.cfg['save_path'],self.cfg['file_out'])+'_cfg.p'
		pickle.dump(self.cfg,open(file_out, "wb"))
	
	def load_config(self,filein=None):
		'''
		Loads .p file containing dict of parameters needed to create outputs. If display=True, sets GUI fields.
		'''
		if filein is None:
			filein = os.path.normpath(fd.askopenfilename(title='Select pickle file for import',filetypes=[('pickle file','*.p'),('pickle file','*.pkl'),('pickle file','*.pickle')]))
		if len(filein) < 2:
			return
		with open(filein, "rb") as f:
			self.cfg = pickle.load(f)
			if self.display:
				for key,value in self.cfg.items():
					if self_fns[key] is 'entry':
						getattr(self,key).set(value)
					else:
						setattr(self,key,value)
				self.refresh_GUI()
			else:
				return self

	def refresh_GUI(self):
		'''
		
		'''
		if not hasattr(self,'data'):
			self.status['text'] = 'Status: Cannot do this - no dataset has been loaded.'
			return
		self.process_H_W()
		self.init_plots()

		# Update slider (Need to move the command)
		if self.frameslider.get() > len(self.data['H_pp'].T): # This (usually) occurs when the user crops the dataset
			self.frameslider.set(1)
		self.frameslider['to'] = int(len(self.data['H_pp'].T)-1)

		Hstd = self.data['H_pp'].std()*3 # 3 Could be in an option json/yaml file
		if self.offsetH.get():
			tmpH = self.data['H_pp'].T - repmat([w*Hstd for w in list(range(len(self.Wshow_arr)))],len(self.data['H_pp'].T),1)
		else:
			tmpH = self.data['H_pp'].T

		self.H_plot = self.Hax1.plot(tmpH,linewidth=.5)
		for i,j in enumerate(self.Hax1.lines):
			j.set_color(self.cmap[i])
		if not self.offsetH.get():
			thresh_line = self.Hax1.plot(np.ones((len(self.data['H_pp'].T,)))*self.cfg['threshold'],linestyle='dashed',color='0',linewidth=1)
			zero_line = self.Hax1.plot(np.zeros((len(self.data['H_pp'].T,))),linestyle='dashed',color='.5',linewidth=1)
			self.legend = self.Hax1.legend((thresh_line[0],), ('Threshold',))
			#self.legend = self.Hax1.legend((thresh_line[0],zero_line[0]), ('Threshold','Baseline'))

		if self.cfg['audio_format'] == 'Stream':
			self.H_p_plot = self.Hax2.imshow(self.data['H_pp'],interpolation='none',cmap=plt.get_cmap('gray'))
			self.H_p_plot.set_clim(0, np.max(self.data['H_pp']))
		else:
			self.H_p_plot = self.Hax2.imshow(self.data['H_fp'],interpolation='none',cmap=plt.get_cmap('gray'))

		self.Hax2.xaxis.set_major_formatter(tkr.FuncFormatter(lambda x, pos: '{:.2g}'.format(x/self.cfg['fr'])))
		self.Hax2.set(xlabel='time (sec)',ylabel='Component #')

		self.Hax1.set_xlim(0, len(self.data['H_pp'].T))
		self.Hax1.set_ylim(np.min(tmpH), np.max(tmpH))
		if self.offsetH.get():
			self.Hax1.set(ylabel='Component #')
		else:
			self.Hax1.set(ylabel='Magnitude')

		self.Hax1.spines['right'].set_visible(False)
		self.Hax1.spines['top'].set_visible(False)
		self.Hax1.spines['bottom'].set_visible(False)
		self.Hax1.tick_params(axis='x',which='both',bottom=False, top=False, labelbottom=False, right=False)

		if len(self.Wshow_arr) > 10:
			yticks = np.arange(4,len(self.data['H_pp']),5)
			yticklabels = np.arange(4,len(self.data['H_pp']),5)
		else:
			yticks = np.arange(0,len(self.data['H_pp']),1)
			yticklabels = np.arange(0,len(self.data['H_pp']),1)

		if self.offsetH.get():
			self.Hax1.set(yticks=-yticks*Hstd,yticklabels=yticklabels)
		self.Hax2.set(yticks=yticks,yticklabels=yticklabels)
		self.imWH = self.Wax1.imshow((self.data['W_pp']@np.diag(self.data['H_pp'][:,self.frameslider.get()])@self.cmap[:,:-1]*(255/self.cfg['brightness'])).reshape(self.data['W_shape'][0],self.data['W_shape'][1],3).clip(min=0,max=255).astype('uint8'))
		self.imW = self.Wax2.imshow((self.data['W_pp']@self.cmap[:,:-1]*255/np.max(self.data['W_pp'])).reshape(self.data['W_shape'][0],self.data['W_shape'][1],3).clip(min=0,max=255).astype('uint8'))
		
		self.H_p_plot.axes.set_aspect('auto')
		self.imW.axes.set_aspect('equal')
		self.imWH.axes.set_aspect('equal')
		self.canvas_H.draw()
		self.canvas_W.draw()
		self.refresh_slider([])

	def process_H_W(self):
		'''
		
		'''
		if self.cfg['Wshow'] == 'all':
			self.Wshow_arr = list(range(len(self.data['H'])))
		elif re.match('^\[[0-9,: ]*\]$',self.cfg['Wshow']) is not None:
			w = eval('np.r_'+self.cfg['Wshow'])
			if np.max(w) <= len(self.data['H']):
				self.Wshow_arr = np.asarray(list(range(len(self.data['H']))))[w]
		else:
			self.status['text'] = 'Status: For \'components to show\', please input indices with commas and colons enclosed by square brackets, or \'all\' for all components.'

		if self.display:
			self.self_to_cfg()

		self.data['H_pp'] = self.data['H'][self.Wshow_arr,int(len(self.data['H'].T)*self.cfg['st_p']/100):int(len(self.data['H'].T)*self.cfg['en_p']/100)]
		self.data['H_pp'] = self.data['H_pp']+self.cfg['baseline']
		self.data['W_pp'] = self.data['W'][:,self.Wshow_arr]
		
		self.make_keys()

		# Making note matrix
		true_fr = self.cfg['fr']*self.cfg['speed']/100
		ns = int(len(self.data['H_pp'].T)*1000/true_fr)
		H = resample(self.data['H_pp'], ns, axis=1)
		Hb = H > self.cfg['threshold']
		Hb = Hb * 1
		Hb[:,0] = 0
		Hb[:,-1] = 0
		Hmax = np.max(H)
		self.data['H_fp'] = np.zeros(np.shape(self.data['H_pp']))
		self.nd = {}
		self.nd['st'],self.nd['en'],self.nd['note'],self.nd['mag'] = [],[],[],[]
		for i in range(len(H)):
			TC = np.diff(Hb[i,:])
			st = np.argwhere(TC == 1)
			en = np.argwhere(TC == -1)
			self.nd['st'].extend([x/1000 for x in st])
			self.nd['en'].extend([x/1000 for x in en])
			for j in range(len(st)):
				tmpmag = np.max(H[i,st[j][0]:en[j][0]])
				self.data['H_fp'][i,int(st[j][0]*true_fr/1000):int(en[j][0]*true_fr/1000)] = tmpmag
				self.nd['mag'].append(int(tmpmag * 127 / Hmax))
				self.nd['note'].append(self.keys[i])

		# Colormap
		if hasattr(cmaps,self.cfg['cmapchoice']):
			cmap = getattr(cmaps,self.cfg['cmapchoice'])
			self.cmap = cmap(np.linspace(0,1,len(self.data['H_pp'])))
		else:
			self.status['text'] = f'Status: cmap {self.cfg["cmapchoice"]} not found. Please check the matplotlib documentation for a list of standard colormaps.'

	def make_keys(self):
		'''
		
		'''
		scaledata = []
		nnotes = len(self.data['H_pp'])
		with open(os.path.join(self.package_path,'scaledata.csv')) as csvfile:
			file = csv.reader(csvfile)
			for row in file:
				scaledata.append([int(x) for x in row if x != 'NaN'])
		noteIDX = scaledata[scale_type_opts.index(self.cfg['scale_type'])]
		noteIDX = [k+key_opts.index(self.cfg['key']) for k in noteIDX]
		keys = []
		for i in range(int(np.ceil(nnotes/len(noteIDX)))):
			keys.extend([k+i*12 for k in noteIDX])
		keys = keys[:nnotes] # Crop to nnotes to avoid confusion
		self.keys = [k+int(self.cfg['oct_add'])*12 for k in keys]

	def refresh_slider(self,event):
		'''
		
		'''
		if not hasattr(self,'data'):
			self.status['text'] = 'Status: Cannot do this - no dataset has been loaded.'
			return
		if hasattr(self,'imWH'):
			self.imWH.remove()
		self.imWH = self.Wax1.imshow((self.data['W_pp']@np.diag(self.data['H_pp'][:,self.frameslider.get()])@self.cmap[:,:-1]*(255/self.cfg['brightness'])).reshape(self.data['W_shape'][0],self.data['W_shape'][1],3).clip(min=0,max=255).astype('uint8'))
		if not hasattr(self,'H_vline'):
			self.H_vline, = self.Hax1.plot([],'k',linewidth=.5)
		self.H_vline.set_xdata([self.frameslider.get(), self.frameslider.get()])
		self.H_vline.set_ydata(self.Hax1.get_ylim())
		self.canvas_W.draw()
		self.canvas_H.draw()

	def preview_notes(self):
		'''
		
		'''
		if not hasattr(self,'data'):
			self.status['text'] = 'Status: Cannot do this - no dataset has been loaded.'
			return
		if get_init() is None: # Checks if pygame has initialized audio engine. Only needs to be run once per instance
			pre_init(44100, -16, 2, 1024)
			init()
			set_num_channels(128) # We will never need more than 128...
		for i in range(len(self.keys)):
			# Load/play notes
			if self.cfg['audio_format']!='Piano':
				sound = sine_wave(16.352*2**(self.keys[i]/12), 10000)
			else:
				fn = os.path.join(self.AE_path,str(self.keys[i])+'_5_2.ogg');
				sound = Sound(file=fn)
			self.imW.remove()
			Wtmp = self.data['W_pp'][:,i]
			cmaptmp = self.cmap[i,:-1]
			self.imW = self.Wax2.imshow((Wtmp[:,None]@cmaptmp[None,:]*255/np.max(self.data['W_pp'])).reshape(self.data['W_shape'][0],self.data['W_shape'][1],3).clip(min=0,max=255).astype('uint8'))
			self.canvas_W.draw()
			self.update()
			if self.cfg['audio_format']=='Stream':
				play_for(sound, 500)
			else:
				sound.play()
				time.sleep(.5)
		self.refresh_GUI()

	def write_audio(self):
		'''
		
		'''
		if self.check_data_and_save_path():
			if not self.display:
				self.process_H_W()
			self.make_keys() # Just in case
			if self.display:
				self.dump_config()
			if self.cfg['audio_format'] == 'MIDI':
				fn = os.path.join(self.cfg['save_path'],self.cfg['file_out'])+'.mid'
				MIDI = MIDIFile(1)  # One track
				MIDI.addTempo(0,0,60) # addTempo(track, time, tempo)
				for j in range(len(self.nd['note'])):
					# addNote(track, channel, pitch, time + i, duration, volume)
					MIDI.addNote(0, 0, self.nd['note'][j], self.nd['st'][j], (self.nd['en'][j]-self.nd['st'][j]), self.nd['mag'][j])
				with open(fn, 'wb') as mid:
					MIDI.writeFile(mid)
			elif self.cfg['audio_format'] == 'Piano':
				self.synth()
			elif self.cfg['audio_format'] == 'Stream':
				self.neuralstream()
			if not self.display:
				return
	
	def synth(self):
		'''
		
		'''
		fs = 44100
		r = .5 # release for note
		#r_mat = np.linspace(1, 0, num=int(fs*r))
		#r_mat = np.vstack((r_mat,r_mat)).T
		currnote = -1
		ext = 11
		note = [[0] * 8 for i in range(3)]
		raws = np.zeros((int(fs*(np.max(self.nd['st'])+ext)),2))
		nnotes = len(self.nd['st'])
		for i in range(len(self.nd['st'])):
			if currnote != self.nd['note'][i]:
				currnote = self.nd['note'][i]
				for mag in range(8): # Load up new notes
					for length in range(3):
						fn = str(currnote+1)+'_'+str(mag)+'_'+str(length+1)+'.ogg';
						note[length][mag],notused = read(os.path.join(self.package_path,'AE',fn))
			L = self.nd['en'][i]-self.nd['st'][i]
			L = min(L,10-r)
			if L > 1:
				raw = note[2][int(np.ceil(self.nd['mag'][i]/16-1))]#[0:int(L*fs)] # Truncate to note length plus release
			elif 1 > L > .25:
				raw = note[1][int(np.ceil(self.nd['mag'][i]/16-1))]#[0:int(L*fs)] # Truncate to note length plus release
			elif L < .25:
				raw = note[0][int(np.ceil(self.nd['mag'][i]/16-1))]#[0:int(L*fs)] # Truncate to note length plus release
			#raw[-int(fs*r):] *= r_mat
			inds = range(int(self.nd['st'][i][0]*fs),int(self.nd['st'][i][0]*fs)+len(raw))
			raws[inds,:] += raw
			if self.display:
				self.status['text'] = f'Status: writing audio file, {i+1} out of {nnotes} notes written'
				self.update()
		raws = raws[:-fs*(ext-1),:] # Crop wav
		raws = np.int16(raws/np.max(np.abs(raws)) * 32767)
		wavwrite(os.path.join(self.cfg['save_path'],self.cfg['file_out'])+'.wav',fs,raws)
		if self.display:
			self.status['text'] = f'Status: audio file written to {self.cfg["save_path"]}'

	def neuralstream(self):
		'''
		
		'''
		C0 = 16.352
		fs = 44100
		freqs = [C0*2**(i/12) for i in range(128)]
		true_fr = (self.cfg['fr']*self.cfg['speed'])/100
		ns = int(fs*len(self.data['H_fp'].T)/true_fr)
		t1 = np.linspace(0,len(self.data['H_fp'].T)/self.cfg['fr'],len(self.data['H_fp'].T))
		t2 = np.linspace(0,len(self.data['H_fp'].T)/self.cfg['fr'],ns)
		H = np.zeros((len(t2),))
		nchan = len(self.data['H_fp'])
		for n in range(nchan):
			Htmp = self.data['H_fp'][n,:]
			Htmp[Htmp<0] = 0
			Htmp = interp1d(t1,Htmp)(t2)
			H += np.sin(2*np.pi*freqs[self.keys[n]]*t2)*Htmp
			Hstr = 'H_fp'
			if self.display:
				self.status['text'] = f'Status: Writing audio: {n+1} out of {nchan} channels...'
				self.update()
		wav = np.hstack((H[:,None],H[:,None]))
		wav = np.int16(wav/np.max(np.abs(wav)) * 32767)
		wavwrite(os.path.join(self.cfg['save_path'],self.cfg['file_out'])+'.wav',fs,wav)
		if self.display:
			self.status['text'] = f'Status: audio file written to {self.cfg["save_path"]}'
		else:
			print(f'Audio file written to {self.cfg["save_path"]}')

	def write_video(self):
		'''
		Writes video file using self.data['H_pp'] using opencv
		'''
		if self.check_data_and_save_path():		
			if not self.display:
				self.process_H_W()
			if self.display:
				self.dump_config()
			fourcc = cv2.VideoWriter_fourcc(*'mp4v')
			out = cv2.VideoWriter(os.path.join(self.cfg['save_path'],self.cfg['file_out'])+'.mp4', fourcc, self.cfg['fr']*self.cfg['speed']/100, tuple(self.data['W_shape'][::-1][1:]),True)
			nframes = len(self.data['H_pp'].T)
			for i in range(nframes):
				frame = (self.data['W_pp']@np.diag(self.data['H_pp'][:,i])@self.cmap[:,:-1]*(255/self.cfg['brightness'])).reshape(self.data['W_shape'][0],self.data['W_shape'][1],3).clip(min=0,max=255).astype('uint8')
				out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
				if self.display:
					self.status['text'] = f'Status: writing video file, {i+1} out of {nframes} frames written'
					self.update()
			out.release()
			if self.display:
				self.status['text'] = f'Status: video file written to {self.cfg["save_path"]}'
			else:
				print(f'Video file written to {self.cfg["save_path"]}')
				return self
	
	def merge(self):
		'''
		Merges video and audio with ffmpeg
		'''
		if self.check_data_and_save_path():
			fn = os.path.join(self.cfg['save_path'],self.cfg['file_out'])
			cmd = 'ffmpeg -hide_banner -loglevel warning -y -i {} -i {} -c:v copy -c:a aac {}'.format(fn+'.mp4',fn+'.wav',fn+'_AV.mp4')
			os.system(cmd)
			if self.display:
				self.status['text'] = f'Status: Video file w/ audio written to {self.cfg["save_path"]}'
			else:
				print(f'A/V file written to {self.cfg["save_path"]}')
				return self
	
	def write_AV(self):
		'''
		
		'''
		if self.check_data_and_save_path():
			self.write_video()
			self.write_audio()
			self.merge()
			if not self.display:
				return self

	def cleanup(self):
		'''
		Tries to remove any files that are video or audio only.	
		'''
		fn = os.path.join(self.cfg['save_path'],self.cfg['file_out'])
		try:
			os.remove(fn+'.mp4')
			os.remove(fn+'.wav')
		except: pass
		if self.display:
			self.status['text'] = f'A/V only videos removed'
		else:
			print(f'A/V only videos removed')
			return self

	def edit_save_path(self):
		self.save_path.set(fd.askdirectory(title='Select a directory to save output files',initialdir=self.cfg['save_path']))

	def initGUI(self):
		'''
		
		'''
		self.winfo_toplevel().title("pyanthem GUI")
		self.protocol("WM_DELETE_WINDOW", self.quit)

		# StringVars
		self.file_in=init_entry('')
		self.file_out=init_entry('')
		self.save_path=init_entry('')
		self.speed=init_entry(100)
		self.fr=init_entry(0)
		self.st_p=init_entry(0)
		self.en_p=init_entry(100)
		self.baseline=init_entry(0)
		self.brightness=init_entry(0)
		self.threshold=init_entry(0)
		self.oct_add=init_entry('2')
		self.scale_type=init_entry('Maj. 7th (4/oct)')
		self.key=init_entry('C')
		self.audio_format=init_entry('Stream')
		self.Wshow=init_entry('all')
		self.status=init_entry('Status: Welcome to pyanthem!')
		self.cmapchoice=init_entry('jet')
		
		# Labels
		Label(text='').grid(row=0,column=0) # Just to give a border around Seperators
		Label(text='File Parameters',font='Helvetica 14 bold').grid(row=0,column=1,columnspan=2,sticky='WE')
		Label(text='Movie Parameters',font='Helvetica 14 bold').grid(row=0,column=3,columnspan=2,sticky='WE')
		Label(text='Audio Parameters',font='Helvetica 14 bold').grid(row=0,column=5,columnspan=2,sticky='WE')
		Label(text='Input Filename').grid(row=1, column=1,columnspan=2,sticky='W')
		Label(text='Output Filename').grid(row=3, column=1,columnspan=2,sticky='W')
		Label(text='Save Path').grid(row=5, column=1,columnspan=1,sticky='W')
		Label(text='Playback speed (%)').grid(row=1, column=3, sticky='E')
		Label(text='Start (%)').grid(row=2, column=3, sticky='E')
		Label(text='End (%)').grid(row=3, column=3, sticky='E')
		Label(text='Baseline').grid(row=4, column=3, sticky='E')
		Label(text='Max brightness').grid(row=5, column=3, sticky='E')
		Label(text='Colormap').grid(row=6, column=3, sticky='E')
		Label(text='Threshold').grid(row=1, column=5, sticky='E')
		Label(text='Octave').grid(row=2, column=5, sticky='E')
		Label(text='Scale Type').grid(row=3, column=5, sticky='E')
		Label(text='Key').grid(row=4, column=5, sticky='E')
		Label(text='Audio format').grid(row=5, column=5, sticky='E')

		# Messages
		self.status = Message(text='Status: Welcome to pyanthem!',aspect=1000)
		self.status.grid(row=8, column=1,columnspan=4,sticky='W')
		self.status.grid_propagate(0)

		# Entries
		Entry(textvariable=self.file_in).grid(row=2, column=1,columnspan=2,sticky='W')
		Entry(textvariable=self.file_out).grid(row=4, column=1,columnspan=2,sticky='W')
		Entry(textvariable=self.save_path,width=17).grid(row=6, column=1,columnspan=2,sticky='EW')
		Entry(textvariable=self.speed,width=7).grid(row=1, column=4, sticky='W')
		Entry(textvariable=self.st_p,width=7).grid(row=2, column=4, sticky='W')
		Entry(textvariable=self.en_p,width=7).grid(row=3, column=4, sticky='W')
		Entry(textvariable=self.baseline,width=7).grid(row=4, column=4, sticky='W')
		Entry(textvariable=self.brightness,width=7).grid(row=5, column=4, sticky='W')
		Entry(textvariable=self.threshold,width=7).grid(row=1, column=6, sticky='W')

		# Buttons
		Button(text='Edit',command=self.edit_save_path,width=5).grid(row=5, column=2)
		Button(text='Preview Notes',width=15,command=self.preview_notes).grid(row=6, column=5,columnspan=2)
		Button(text='Update',width=15,command=self.refresh_GUI).grid(row=8, column=5,columnspan=2)

		# Option/combobox values
		
		if self.AE_run:
			audio_format_opts = ['Stream','Piano','MIDI']
		else:
			audio_format_opts = ['Stream','MIDI']
			self.status['text'] = 'Status: AE engine not downloaded. Please do so using AE_download() to enable "Piano" format'

		# Option Menus
		oct_add_menu = OptionMenu(self,self.oct_add,*oct_add_opts)
		oct_add_menu.config(width=7)
		oct_add_menu.grid(row=2, column=6, sticky='W')
		scale_type_menu=OptionMenu(self,self.scale_type,*scale_type_opts)
		scale_type_menu.config(width=7)
		scale_type_menu.config(font=(self.default_font,(8)))
		scale_type_menu.grid(row=3, column=6, sticky='EW')
		key_menu=OptionMenu(self,self.key,*key_opts)
		key_menu.config(width=7)
		key_menu.grid(row=4, column=6, sticky='W')
		audio_format_menu=OptionMenu(self,self.audio_format,*audio_format_opts)
		audio_format_menu.config(width=7)
		audio_format_menu.grid(row=5, column=6, sticky='W')
		
		# Combo box
		self.cmapchooser = Combobox(self,textvariable=self.cmapchoice,width=7)
		self.cmapchooser['values'] = cmaps_opts
		#self.cmapchooser['state'] = 'readonly'
		self.cmapchooser.grid(row=6, column=4, sticky='WE')
		self.cmapchooser.current()
		self.cmap = []
		# Menu bar
		menubar=Menu(self)
		filemenu=Menu(menubar, tearoff=0)
		filemenu.add_command(label="Load from .mat", command=self.load_GUI)
		filemenu.add_command(label="Load .cfg", command=self.load_config)
		filemenu.add_command(label="Quit",command=self.quit)

		savemenu=Menu(menubar, tearoff=0)
		savemenu.add_command(label="Audio", command=self.write_audio)
		savemenu.add_command(label="Video", command=self.write_video)
		savemenu.add_command(label="Merge A/V", command=self.merge)
		savemenu.add_command(label="Write A/V then merge", command=self.write_AV)
		savemenu.add_command(label="Cleanup", command=self.cleanup)

		menubar.add_cascade(label="File", menu=filemenu)
		menubar.add_cascade(label="Save", menu=savemenu)
		self.config(menu=menubar)

		# Seperators
		s_v=[[0,0,9],[2,0,8],[4,0,8],[6,0,9]]
		s_h=[[1,0,6],[1,1,6],[1,8,6],[1,9,6],[1,3,2],[1,5,2]]
		for sv in s_v:
			Separator(self, orient='vertical').grid(column=sv[0], row=sv[1], rowspan=sv[2], sticky='nse')
		for sh in s_h:
			Separator(self, orient='horizontal').grid(column=sh[0], row=sh[1], columnspan=sh[2], sticky='nwe')

		# Offset
		self.offsetH=IntVar()
		self.offsetH.set(1)
		
		# frameslider
		self.frameslider=Scale(self, from_=0, to=1, orient=HORIZONTAL)
		self.frameslider['command']=self.refresh_slider

	def init_plots(self):
		'''
		
		'''
		# H
		self.figH = plt.Figure(figsize=(6,6), dpi=100, tight_layout=True)
		self.Hax1 = self.figH.add_subplot(211)
		self.Hax2 = self.figH.add_subplot(212)
		self.Hax1.set_title('Raw Temporal Data (H)')
		self.Hax2.set_title('Converted Temporal Data (H\')')
		self.canvas_H = FigureCanvasTkAgg(self.figH, master=self)
		self.canvas_H.get_tk_widget().grid(row=0,column=7,rowspan=29,columnspan=10)
		bg = self.status.winfo_rgb(self.status['bg'])
		self.figH.set_facecolor([(x>>8)/255 for x in bg])
		self.canvas_H.draw()

		# Checkbox
		Checkbutton(self, text="Offset H",command=self.refresh_GUI,variable=self.offsetH).grid(row=0,rowspan=1,column=16)

		# W
		self.figW = plt.Figure(figsize=(6,3), dpi=100, constrained_layout=True)
		self.Wax1 = self.figW.add_subplot(121)
		self.Wax2 = self.figW.add_subplot(122)
		self.Wax1.set_title('Output(H x W)')
		self.Wax2.set_title('Spatial Components (W)')
		self.Wax1.axis('off')
		self.Wax2.axis('off')
		self.canvas_W = FigureCanvasTkAgg(self.figW, master=self)
		self.canvas_W.get_tk_widget().grid(row=10,column=1,rowspan=19,columnspan=6)
		self.figW.set_facecolor([(x>>8)/255 for x in bg])
		self.canvas_W.draw()
		
		# Frameslider
		self.frameslider.grid(row=29, column=2, columnspan=1)

		# Wshow
		Label(text='Components to show:').grid(row=29, column=3, columnspan=3, sticky='E')
		Entry(textvariable=self.Wshow,width=15,justify='center').grid(row=29, column=5, columnspan=2,sticky='E')

	def process_raw(self,file_in=None,n_clusters=None,frame_rate=None,save=False):
		'''
		
		'''
		from sklearn.cluster import KMeans
		if file_in is None:
			root = Tk()
			root.withdraw()
			file_in = os.path.normpath(fd.askopenfilename(title='Select .mat file for import',filetypes=[('.mat files','*.mat')]))
			root.update()
		if len(file_in) == 0:
			return
		dh,var = loadmat(file_in),whosmat(file_in)
		data = dh[var[0][0]]
		sh = data.shape
		if len(sh) != 3:
			print('ERROR: input dataset is not 3D.')
			return
		data = data.reshape(sh[0]*sh[1],sh[2])
		# Ignore rows with any nans
		nanidx = np.any(np.isnan(data), axis=1)
		data_nn = data[~nanidx] # nn=non-nan
		# k-means
		print('Performing k-means...',end='')
		if n_clusters is None:
			n_clusters = int(len(data)**.25) # Default k is the 4th root of the number of samples per frame (for 256x256, this would be 16)
			print(f'No num_clusters given. Defaulting to {n_clusters}...',end='')
		idx_nn = KMeans(n_clusters=n_clusters, random_state=0).fit(data_nn).labels_
		idx = np.zeros((len(data),))
		idx[nanidx==False] = idx_nn
		# TCs
		H = np.zeros((n_clusters,len(data.T)))
		for i in range(n_clusters):
			H[i,:] = np.nanmean(data[idx==i,:],axis=0)
		print('done.')
		# NNLS
		nnidx=np.where(~nanidx)[0]
		W = np.zeros((len(data),n_clusters))
		print('Performing NNLS...',end='')
		for i in range(len(nnidx)):
			W[nnidx[i],:]=nnls(H.T,data_nn[i,:])[0]
		# Sort top to bottom
		xc,yc = [], []
		(X,Y) = np.meshgrid(range(sh[0]),range(sh[1]))
		for i in range(len(W.T)):
			Wtmp = W[:,i].reshape(sh[0],sh[1])
			xc.append((X*Wtmp).sum() / Wtmp.sum().astype("float"))
			yc.append((Y*Wtmp).sum() / Wtmp.sum().astype("float"))
		I = np.argsort(yc)
		W = W[:,I]
		H = H[I,:]
		print('done.')
		
		# Assign variables and save
		self.data = {}
		self.data['H'] = H
		self.data['W'] = W.reshape(sh[0],sh[1],n_clusters)
		self.data['W_shape'] = self.data['W'].shape
		if frame_rate == []:
			self.data['fr'] = 10
			print('No fr given. Defaulting to 10')
		else:
			self.data['fr'] = frame_rate
		if save:
			fn = file_in.replace('.mat','_decomp.mat')
			savemat(fn,self.data)
			print(f'Decomposed data file saved to {fn}')
		
		# Reshape W here, since any use of self from here would require a flattened W
		self.data['W'] = self.data['W'].reshape(self.data['W'].shape[0]*self.data['W'].shape[1],self.data['W'].shape[2])
		return self

if __name__ == "__main__":
	run()

# self\.([a-z_]{1,14})\.get\(\)
# self\.cfg\[$1\]