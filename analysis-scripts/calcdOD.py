#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 14:39:59 2017

@author: htchang
"""

import numpy as np
import sys
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy.stats import norm

prefix=sys.argv[1]
#print(prefix)

NumCycles=int(sys.argv[2])
NumSteps=int(sys.argv[3])

dark=np.average(np.loadtxt(prefix+'.dark'),axis=0)
background=np.average(np.loadtxt(prefix+'.bg'),axis=0)
pumpon=np.fromfile(prefix+'_pumpon_raw.bin',dtype='int32')
pumpoff=np.fromfile(prefix+'_pumpoff_raw.bin',dtype='int32')

if(sys.argv[4]=='-static'):
    pumpon=np.fromfile(prefix+'_pumpon_raw.bin',dtype='float32')
    pumpoff=np.fromfile(prefix+'_pumpoff_raw.bin',dtype='float32')
    

filtered = lowess(dark, np.arange(0,1340), is_sorted=True, frac=0.1, it=0)
dark = filtered[:,1]
filtered = lowess(background, np.arange(0,1340), is_sorted=True, frac=0.1, it=0)
background = filtered[:,1]

pumpon_proc=pumpon-background.repeat(NumCycles*NumSteps)
pumpoff_proc=pumpoff-dark.repeat(NumCycles*NumSteps)

dOD=np.log10(pumpoff_proc/pumpon_proc)
dOD[np.isnan(dOD)]=0

dOD=dOD.reshape(NumCycles,NumSteps,1340)
#print(dOD.shape)
if(sys.argv[4]!='-static'):
    np.save(prefix+'-dOD',dOD);

if(sys.argv[4]=='-FT'):
    #print(sys.argv[4])
    dOD_FT=np.zeros([NumCycles,NumSteps,1340])
    gfilter=np.zeros(1340);
    center=1340/2;
    sigma=30;
    gfilter=norm.pdf(np.arange(-center,center),0.001,sigma)
    gfilter/=np.max(gfilter);
    pumpon_proc=pumpon_proc.reshape(NumCycles,NumSteps,1340)
    pumpoff_proc=pumpoff_proc.reshape(NumCycles,NumSteps,1340)
    for i in range(0,NumCycles):
        for j in range(0,NumSteps):
            ftpumpon=np.multiply(np.fft.fftshift(np.fft.fft(pumpon_proc[i][j])),gfilter)
            ftpumpoff=np.multiply(np.fft.fftshift(np.fft.fft(pumpon_proc[i][j])),gfilter)
            pumponifft=np.real(np.fft.ifft(np.fft.ifftshift(ftpumpon)))
            pumpoffifft=np.real(np.fft.ifft(np.fft.ifftshift(ftpumpoff)))
            dOD_FT[i][j]=np.log10(pumpoffifft/pumponifft)
            
            
    dOD_FT=dOD-dOD_FT
    np.save(prefix+'-dOD_FT',dOD_FT)
    
if(sys.argv[4]=='-static'):
    dOD=np.squeeze(dOD)
    #print(dOD.shape)
    dOD_static=np.average(dOD,axis=0)
    #print(dOD_static.shape)
    energy=np.loadtxt(sys.argv[5])
    #print(energy.shape)
    #print(np.vstack((energy.T, dOD_static)).shape)
    np.savetxt(prefix+'_static.txt',np.vstack((energy.T, dOD_static)).T,fmt='%.6f')
    
    
    