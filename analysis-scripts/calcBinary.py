# stream binary PIXIS data
# Written by Hung-Tzu Chang, 2018/1/17

import numpy as np
#import matplotlib.pyplot as plt
#import pandas as pd
import sys
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.stats import norm

path_log=sys.argv[1]
prefix=sys.argv[2]
NumCycles=int(sys.argv[3])
NumSteps=int(sys.argv[4])
NumGas=int(sys.argv[5])
NumDark=sys.argv[6]
NumBG=sys.argv[7]

pumpon_array=np.loadtxt(path_log+'/'+prefix+'_pumpon.txt',dtype='int')
pumpoff_array=np.loadtxt(path_log+'/'+prefix+'_pumpoff.txt',dtype='int')


if(NumGas!=0):
	gas_array=np.loadtxt(path_log+'/'+prefix+'_gas.txt',dtype='int')
# Setup FT parameters
	gfilter=np.zeros(1340);
	center=1340/2;
	sigma=30;
	gfilter=norm.pdf(np.arange(-center,center),0.001,sigma)
	gfilter/=np.max(gfilter);
# Calculate Gas Transient
	gas_transient=np.zeros([NumCycles*NumGas,1340],dtype=int)
	for i in range(0,NumCycles*NumGas):
		gas_transient[i]=np.fromfile('Scan'+str(gas_array[i])+'.bin',dtype='int32')[2:None]
		
	np.save(prefix+'_gas_raw',gas_transient.reshape([NumCycles,NumGas,1340]))
	dOD_gas=np.zeros([NumCycles*NumGas,1340])
	for i in range(0,gas_transient.shape[0]):
		fttmp=np.fft.fftshift(np.fft.fft(np.asfarray(gas_transient[i,:])))*gfilter
		dOD_gas[i,:]=np.log10(np.real(np.fft.ifft(np.fft.ifftshift(fttmp))))-np.log10(np.asfarray(gas_transient[i,:]))

	dOD_gas=dOD_gas.reshape([NumCycles,NumGas,1340])
	for i in range(0,NumCycles):
		dOD_gas[i]-=dOD_gas[i,-1,:]

	dOD_gas[np.isnan(dOD_gas)]=0
	np.save(prefix+'-gas_dOD',dOD_gas)
	del gas_transient
	del dOD_gas

# Start background smoothing
dark=np.fromfile('Scan'+NumDark+'.bin',dtype='int')
dark=dark[2:None].reshape(dark[0],dark[1])
dark=np.average(dark,axis=0)

background=np.fromfile('Scan'+NumBG+'.bin',dtype='int')
background=background[2:None].reshape(background[0],background[1])
background=np.average(background,axis=0)

filtered = lowess(dark, np.arange(0,1340), is_sorted=True, frac=0.1, it=0)
dark = filtered[:,1]
filtered = lowess(background, np.arange(0,1340), is_sorted=True, frac=0.1, it=0)
background = filtered[:,1]

np.save(prefix+'_dark',dark)
np.save(prefix+'_bg',background)

pumpon=np.zeros([NumCycles*NumSteps,1340],dtype=int)
#pumpoff=np.zeros([NumCycles*NumSteps,1340],dtype=int)
for i in range(0,NumCycles*NumSteps):
	pumpon[i]=np.fromfile('Scan'+str(pumpon_array[i])+'.bin',dtype='int')[2:None]
#	pumpoff[i]=np.fromfile('Scan'+str(pumpoff_array[i])+'.bin',dtype='int')[2:None]

np.save(prefix+'_pumpon',pumpon.reshape([NumCycles,NumSteps,1340]))
#np.save(prefix+'_pumpoff',pumpoff.reshape([NumCycles,NumSteps,1340]))
del pumpon
pumpoff=np.zeros([NumCycles*NumSteps,1340],dtype=int)
for i in range(0,NumCycles*NumSteps):
#	pumpon[i]=np.fromfile('Scan'+str(pumpon_array[i])+'.bin',dtype='int')[2:None]
	pumpoff[i]=np.fromfile('Scan'+str(pumpoff_array[i])+'.bin',dtype='int')[2:None]

#np.save(prefix+'_pumpon',pumpon.reshape([NumCycles,NumSteps,1340]))
np.save(prefix+'_pumpoff',pumpoff.reshape([NumCycles,NumSteps,1340]))
'''
pumpon=np.asfarray(pumpon)-np.tile(background,[NumCycles*NumSteps,1])
pumpoff=np.asfarray(pumpoff)-np.tile(dark,[NumCycles*NumSteps,1])

# Calculate dOD
dOD=np.log10(pumpoff/pumpon)
dOD[np.isnan(dOD)]=0
dOD=dOD.reshape([NumCycles,NumSteps,1340])
np.save(prefix+'-dOD',dOD)

# Calculate dOD_FT
pumpon_FT=np.zeros([NumCycles*NumSteps,1340])
pumpoff_FT=np.zeros([NumCycles*NumSteps,1340])
for i in range(0,pumpon.shape[0]):
	ftpumpon=np.multiply(np.fft.fftshift(np.fft.fft(pumpon[i])),gfilter)
	ftpumpoff=np.multiply(np.fft.fftshift(np.fft.fft(pumpoff[i])),gfilter)
	pumpon_FT[i]=np.real(np.fft.ifft(np.fft.ifftshift(ftpumpon)))
	pumpoff_FT[i]=np.real(np.fft.ifft(np.fft.ifftshift(ftpumpoff)))
	
dOD_FT=np.log10(pumpoff_FT/pumpon_FT)
dOD_FT[np.isnan(dOD_FT)]=0
dOD_FT=dOD_FT.reshape([NumCycles,NumSteps,1340])
np.save(prefix+'-dOD_FT',dOD-dOD_FT)
del dOD
del dOD_FT
del pumpoff
del pumpoff_FT

# Calculate dOD_FT_RIGOR
dOD_FT_RIGOR=np.log10(pumpon_FT/pumpon)
dOD_FT_RIGOR=dOD_FT_RIGOR.reshape([NumCycles,NumSteps,1340])
for i in range(0,NumCycles):
	dOD_FT_RIGOR[i]-=np.average(np.squeeze(dOD_FT_RIGOR[i,0:10,:]),axis=0)
	
dOD_FT_RIGOR[np.isnan(dOD_FT_RIGOR)]=0
np.save(prefix+'-dOD_FT_RIGOR',dOD_FT_RIGOR)
'''