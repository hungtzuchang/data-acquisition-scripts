# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 18:17:59 2016

@author: HungTzu
"""

import numpy as np
import math as mt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
import datetime
import warnings
from scipy.optimize import OptimizeWarning
import sys
sys.path.append('C:/Users/D60 South/Desktop/HungTzuScripts/')
from smooth import smooth
#imagedir='C:/Users/D60 South/Desktop/Gas_Image/'
#os.chdir(imagedir)
print(sys.argv)
datefromprefix=sys.argv[1]
experimentName=sys.argv[2]
imagedir='C:/Users/D60 South/Desktop/Gas_Image/'+datefromprefix+'/'+experimentName+'/'
#rootdir='C:/Users/D60 South/Desktop/1093DATA/Test/'+datefromprefix+'/'+experimentName+'/'

rootdir='C:/Users/D60 South/Desktop/1093DATA/'+datefromprefix+'/'+experimentName+'/'
print(rootdir)
os.chdir(rootdir)
file1=open("gas_config.txt",'r')
file_content=file1.readlines()
file1.close()
start_file=int(float(file_content[0]))
end_file=int(float(file_content[1]))
micron_start=float(file_content[2])
micron_end=float(file_content[3])
micron_step=float(file_content[4])
micron_zero=float(file_content[5])
pixel_start=int(float(file_content[6]))
pixel_end=int(float(file_content[7]))
pixel1_start=int(float(file_content[8]))
pixel1_end=int(float(file_content[9]))

#os.chdir('C:/Users/D60 South/Desktop/1093DATA/2017_12_06')

#if not os.path.exists(imagedir):
#	os.makedirs(imagedir)

Scan_data=np.zeros([end_file-start_file+1,1340])
Scan_data_filtered=np.zeros([end_file-start_file+1,1340])

c =  299792458000000/1e15;

center=1340/2;
sigma=30;
gfilter=np.arange(-center,center)
gfilter=np.exp(-(((gfilter-0.000)/sigma)**2)/2);
gfilter/=np.max(gfilter);

for i in range(0,end_file+1-start_file):
    a=1.0*np.fromfile('Scan'+str(i+start_file)+'.bin',dtype='int')
    Scan_data[i]=a[2:None]
    fttmp=np.fft.fftshift(np.fft.fft(Scan_data[i]))
    back=fttmp
    fttmp*=gfilter
    Scan_data_filtered[i]=np.real(np.fft.ifft(np.fft.ifftshift(fttmp)))
    #Scan_data_filtered[i]=savgol_filter(Scan_data[i],71,2)    


dODNe=np.log10(Scan_data_filtered/Scan_data)
dODNe[np.isnan(dODNe)]=0
#dODNe=dODNe-np.average(dODNe[end_file-start_file-5:end_file-start_file],axis=0)
dODNe=dODNe-dODNe[end_file-start_file-1]
micron=np.linspace(micron_start,micron_end,end_file-start_file+1,endpoint=True)-micron_zero
print('Data successfully transformed')
os.chdir(imagedir)
plt.figure()
plt.pcolormesh(dODNe,shading='gouraud',cmap='bwr')
plt.colorbar()
plt.axvline(pixel_start,  color='r')
plt.axvline(pixel_end,  color='r')
#plt.axvline(555,  color='g')
#plt.axvline(570,  color='g')
plt.axvline(pixel1_start,  color='g')
plt.axvline(pixel1_end,  color='g')
#plt.axvline(959,  color='g')
#plt.axvline(965,  color='g')
#plt.xlim([0,200])
#plt.xlim([10,310])
#plt.xlim([500,800])
plt.xlim([950,1200])
plt.clim([-0.02,0.02])
plt.savefig('Ne_trace'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.png',dpi=72)
plt.savefig('Ne_trace_last.png',dpi=100)
#plt.savefig(imagedir+'Ne_trace'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.png',dpi=72)
#plt.savefig(imagedir+'Ne_trace_last.png',dpi=100)
#plt.show()
plt.close()

integrated_signal=np.sum((dODNe.T[pixel_start:pixel_end]),axis=0).T
integrated_signal=smooth(integrated_signal,5,'flat')

#integrated_signal=savgol_filter(integrated_signal,9,2)
integrated_signal1=np.sum((dODNe.T[pixel1_start:pixel1_end]),axis=0).T
integrated_signal1=smooth(integrated_signal1,5,'flat')

#integrated_signal1=savgol_filter(integrated_signal1,9,2)
#integrated_signal2=np.sum(dODNe.T[555:565],axis=0).T
#integrated_signal2=savgol_filter(integrated_signal2,7,2)
#integrated_signal3=np.sum(dODNe.T[640:650],axis=0).T
#integrated_signal3=savgol_filter(integrated_signal3,7,2)
plt.plot(micron,integrated_signal)
plt.xlabel('micron')
plt.savefig('Ne_fit'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.png')
#plt.savefig(imagedir+'Ne_fit'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.png')
plt.close()
#sigfunc = lambda x,A0,A1,A2,A3,A4: A1+A0*np.exp(-x/A4)/(1 + np.exp(-(x-A2)/A3))
from scipy.special import erfc
sigfunc = lambda x,A1,A2,A3,A4: A3*erfc((x-A1)/A2)+A4#A2+(A1-A2)*np.exp((x-A3)/A5)/(1 + np.exp((x-A3)/A4))
#exp_decay_func = lambda x,C1,C2,C3,C4,C5: C1*C2*np.sqrt(mt.pi)*np.exp((C2*C2-16*np.log(2)*C3*(x - C4))/(16*np.log(2)*C3*C3))*(1-mt.erf((C2*C2-8*np.log(2)*C3*(x - C4))/(4*C2*np.sqrt(np.log(2))*C3))) + C5

      
A1,A2,A3,A4,A5=[-1,1,0.4,0.0,1]
B1,B2,B3,B4,B5=[-1,1,0.3,0.0,1]
C1,C2,C3,C4,C5=[0.15, 7, 50, 0, 0.0000]

error=0
error1=0
error2=0

delay_vector_fs=micron*2/c;
plt.scatter(delay_vector_fs,integrated_signal, s=80, facecolors='gray')
plt.scatter(delay_vector_fs,integrated_signal1, s=80, facecolors='black')

maxsig=np.argmax(integrated_signal)
integrated_signal[0:maxsig]=integrated_signal[maxsig]
minsig=np.argmax(integrated_signal1)
integrated_signal1[0:minsig]=integrated_signal1[minsig]

with warnings.catch_warnings():
    warnings.simplefilter("error", OptimizeWarning)
    try:
        popt,pcov=curve_fit(sigfunc,micron,integrated_signal,p0=(0,1,0.2,0))
        A1,A2,A3,A4=popt
        residual=np.sum(np.square(sigfunc(micron,*popt)-integrated_signal))/(len(integrated_signal)-len(popt))

    except OptimizeWarning:
        residual=1 
        error=1
        
    except RuntimeError:
        residual=1
        error=1
#A0=np.ones(4)
        
with warnings.catch_warnings():
    warnings.simplefilter("error", OptimizeWarning)
    try:
        popt1,pcov1=curve_fit(sigfunc,micron,integrated_signal1,p0=(0,1,-0.2,0))
        B1,B2,B3,B4=popt1
        residual1=np.sum(np.square(sigfunc(micron,*popt1)-integrated_signal1))/(len(integrated_signal1)-len(popt1))

    except OptimizeWarning:
        residual1=1 
        error1=1
        
    except RuntimeError:
        residual1=1
        error1=1
        
#with warnings.catch_warnings():
#    warnings.simplefilter("error", OptimizeWarning)
#    try:
#        popt2,pcov2=curve_fit(exp_decay_func,micron,integrated_signal1,p0=(0.15,7,50,0.0, 0))
#        C1,C2,C3,C4,C5=popt2
#        residual1=np.sum(np.square(exp_decay_func(micron,*popt2)-integrated_signal1))/(len(integrated_signal1)-len(popt2))

 #   except OptimizeWarning:
 #       residual2=1 
 #       error2=1
        
 #   except RuntimeError:
 #       residual2=1
 #       error2=1
        
        
#delay_vector_fs=micron*2/c;
#plt.plot(delay_vector_fs,integrated_signal, s=80, facecolors='gray')
#plt.plot(delay_vector_fs,integrated_signal1, s=80, facecolors='black')

#plt.plot(delay_vector_fs,sigfunc(micron,A1,A2,A3,A4,A5))
#plt.plot(delay_vector_fs,sigfunc(micron,B1,B2,B3,B4,A5))
#plt.show()
#print(error,error1)
#plt.scatter(micron,integrated_signal3, s=80, facecolors='red')
if error==0:
    plt.plot(delay_vector_fs,sigfunc(micron,A1,A2,A3,A4),'r-')

if error1==0:    
    plt.plot(delay_vector_fs,sigfunc(micron,B1,B2,B3,B4),'g-')

plt.xlabel('fs')
#plt.ylim([-0.2,1.2])
plt.savefig('Ne_fit'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.png')
plt.savefig('Ne_fit_last.png',dpi=100)
#plt.savefig(imagedir+'Ne_fit'+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")+'.png')
#plt.savefig(imagedir+'Ne_fit_last.png',dpi=100)
plt.close()

offset_fs=(A1)*2/c;
offset_fsB=(B1)*2/c;
#os.chdir(rootdir+datefromprefix)
file1=open('delay_log.txt','a')
file1.write(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S\t")+'{:.4f}'.format(A3)+'\t'+'{:.4f}'.format(offset_fs)+'\t'+'{:.4f}'.format(1/A4)+'\t'+'{:.2e}'.format(residual)+'\t'+'{:.4f}'.format(A1)+'\t'+'{:.4f}'.format(A2)+'\t'+'{:.4f}'.format(B3)+'\t'+'{:.4f}'.format(offset_fsB)+'\t'+'{:.4f}'.format(B4)+'\t'+'{:.2e}'.format(residual1)+'\t'+'{:.4f}'.format(B1)+'\t'+'{:.4f}'.format(B2)+'\t'+'\n')
file1.close()

np.savetxt('delay_micron.txt',np.array([A1, offset_fs, residual, B1, offset_fsB, residual1, 1/A4]),fmt='%.7f')