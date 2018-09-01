# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 13:01:53 2017

@author: HungTzu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sys

logfile=pd.read_csv(sys.argv[1],sep='\t')
#print(list(logfile))
#prefix='Si134nm-Ne168torrKr66orr-15ms-5ms-15muJ_'
prefix=sys.argv[2]
gas_label='Gas_Reference_1'
gas_numbers=np.empty(0,dtype=int)
pumpon_numbers=np.empty(0,dtype=int)
pumpoff_numbers=np.empty(0,dtype=int)
scanstart=int(sys.argv[3])
scanend=int(sys.argv[4])
NumCycles=int(sys.argv[5])
NumSteps=int((scanend-scanstart+1)/NumCycles)
TimeOffset=float(sys.argv[6])
#log_used=logfile.loc[logfile['ScanNumber'].isin(np.arange(2628,66948))]
for i in range(0,NumCycles):
    log_used=logfile.loc[logfile['ScanNumber'].isin(np.arange(scanstart+NumSteps*i,scanstart+NumSteps*(i+1)))]
    gas_entries=log_used.loc[log_used['Notes']==gas_label]
    Sipumpon=log_used.loc[(log_used['Notes']!=gas_label) & (log_used['PumpOnOff_800']==1)]
    Sipumpoff=log_used.loc[(log_used['Notes']!=gas_label) & (log_used['PumpOnOff_800']==0)]
    gas_numbers=np.r_[gas_numbers,gas_entries['ScanNumber']]
    Sipumponsort=Sipumpon.sort_values('StageDelay',ascending=True)
    pumpon_numbers=np.r_[pumpon_numbers,Sipumponsort['ScanNumber']]
    Sipumpoffsort=Sipumpoff.sort_values('StageDelay',ascending=True)
    pumpoff_numbers=np.r_[pumpoff_numbers,Sipumpoffsort['ScanNumber']]
    
timeaxis=np.array(Sipumpoffsort['StageDelay'])    
'''
plt.plot(gas_numbers,'o')
plt.show()
plt.close()
'''
np.savetxt(prefix+'_gas.txt',gas_numbers,fmt='%d')
np.savetxt(prefix+'_pumpon.txt',pumpon_numbers,fmt='%d')
np.savetxt(prefix+'_pumpoff.txt',pumpoff_numbers,fmt='%d')
timeaxis-=TimeOffset
timeaxis*=20./3
np.save(prefix+'_taxis.npy',timeaxis)