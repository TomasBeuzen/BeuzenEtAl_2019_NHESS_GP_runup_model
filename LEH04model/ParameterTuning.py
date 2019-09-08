#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to tune dune erosion constant.
Code incorporates most of 'BatchDuneErosion.py', but adds soem extra steps 
to loop through multiple Cs Values

EBG Aug. 2018 (Matlab); Nov 2018 (Python)
"""


import pickle

import numpy as np
import matplotlib.pyplot as plt
#from scipy import stats
#mode is commented out right now

with open('DIM_data_2011.pkl', 'rb') as f:
    data = pickle.load(f)
    
#import the LEH04 model function
from LEH04 import LEH04ensembles

#LEH04 param array
Cs = np.logspace(-5,-1,50);
#Best value is:
#Cs= 0.0016 

#number of ensembles
ens=100

#preallocate
errorGP = np.zeros((len(data),len(Cs)))
errorST = np.zeros((len(data),len(Cs)))
errorGPmean = np.zeros((len(data),len(Cs)))
errorGPmode = np.zeros((len(data),len(Cs)))
errorGPmedian = np.zeros((len(data),len(Cs)))

MaxGP = np.zeros((len(data),len(Cs),ens));
MinGP = np.zeros((len(data),len(Cs),ens));
MeanGP = np.zeros((len(data),len(Cs),ens));
#ModeGP = np.zeros((len(data),len(Cs),ens));
MedianGP = np.zeros((len(data),len(Cs),ens));

#loop through all the Cs indicies
for j in range(len(Cs)):
    
    #loop through the profile indicies
    for k in data:
        profile=data[k]
        
        #pull all relevant data out of the dictionary
        dv = profile['dv']
        zb = profile['zb']
        T = profile['Tp']
        R_st = profile['R_st']
        R_gp = profile['R_gp']
        R_gp_draws = profile['R_gp_draws']
        
        #run it through the St model
        [SigDuneErosionST,zbmST] = LEH04ensembles(dv,zb,R_st,T,Cs[j])
        #run it through GP
        [SigDuneErosionGP,zbmGP] = LEH04ensembles(dv,zb,R_gp,T,Cs[j])
        #run it through 10 'draws' from GP
        [SigDuneErosionGPD,zbmGPD] = LEH04ensembles(dv,zb,R_gp_draws,T,Cs[j])
        
        #record the max and min from GP draws
        for n in range(ens):
            MaxGP[k,j,n] = np.amax(SigDuneErosionGPD[-1,0:n+1])
            MinGP[k,j,n] = np.amin(SigDuneErosionGPD[-1,0:n+1])
            MeanGP[k,j,n] = np.mean(SigDuneErosionGPD[-1,0:n+1])
            #ModeGP[k,j,n] = stats.mode(SigDuneErosionGPD[-1,0:n+1])
            MedianGP[k,j,n] = np.median(SigDuneErosionGPD[-1,0:n+1])
     
        #record error— Absolute error
        errorST[k,j] = np.absolute(profile['dv_obs']-SigDuneErosionST[-1]);     
        errorGP[k,j] = np.absolute(profile['dv_obs']-SigDuneErosionGP[-1]);
    
        #GP ensemble mean is done for max number of ensembles.
        errorGPmean[k,j] = np.absolute(profile['dv_obs'] - MeanGP[k,j,ens-1]);
        #errorGPmode[k,j] = np.absolute(profile['dv_obs'] - ModeGP[k,j,ens]);
        errorGPmedian[k,j]= np.absolute(profile['dv_obs'] - MedianGP[k,j,ens-1]);
    
        #put time series back in the dictionary (new keys)
        profile['SigDuneErosionST'] = SigDuneErosionST
        profile['zbmST'] = zbmST
        profile['SigDuneErosionGP'] = SigDuneErosionGP
        profile['zbmGP'] = zbmGP
        profile['SigDuneErosionGPD'] = SigDuneErosionGPD
        profile['zbmGPD'] = zbmGPD
        
        #make a new key for total erosion and final zb
        profile['dVst'] = SigDuneErosionST[-1]
        profile['zbst'] = zbmST[-1]
        profile['dVGP'] = SigDuneErosionGP[-1]
        profile['zbGP'] = zbmGP[-1]
        profile['dVGPD'] = SigDuneErosionGPD[-1,:]
        profile['zbGPD'] = zbmGPD[-1,:]
        
        #put the dictionary back in the bigger dictionary. 
        #This 'overprints' the old dictionary b/c it adds new entries.
        #no info is deleted.
        data[k]=profile
        
#COMPUTE SOME INFO
#capture stats
PercentWithin = np.zeros((len(Cs),ens))
obs = np.zeros((len(data)))
for h in data:
    obs[h] = data[h]['dv_obs']
    
    
for f in range(len(Cs)):
    for g in range(ens):
        within = np.where((MaxGP[:,f,g]>=obs) & (MinGP[:,f,g]<=obs))
        PercentWithin[f,g] = 100*(len(within[0])/(len(data)));



#plotting
fig, axs = plt.subplots(2, 1)
axs[0].semilogx(Cs,np.mean(errorST, axis=0),'r',Cs,np.mean(errorGP, axis=0),'k',Cs,np.mean(errorGPmean, axis=0),'k.',Cs,np.mean(errorGPmedian, axis=0),'b.')

axs[0].set_ylabel('MAE (all profiles)')
axs[0].set_ylim(0, 10)  

axs[1].plot()
axs[1].semilogx(Cs,PercentWithin)
axs[1].set_xlabel('Cs')
axs[1].set_ylabel('percent within ensemble')

plt.show()

#legend('ST','GP', 'E. Mean', 'E. Median')

#for finding the min error
#a=np.mean(errorGPmean, axis=0)
#aa=np.mean(errorGP, axis=0)

