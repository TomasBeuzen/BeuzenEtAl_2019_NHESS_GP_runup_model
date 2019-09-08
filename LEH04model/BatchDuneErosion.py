"""
This script loops through the python dictionary and 
calculates zb and dune erosion
volumes for all profiles. 

The output is a time series of profile evolution and erosion volumes.
This is compared to measured zb and dV

"It is easier to write a new code than to understand an old one"
-John von Neumann to Marston Morse, 1952

EBG Aug. 2018 (Matlab); Oct 2018 (Python)
"""

import pickle

import numpy as np

with open('DIM_data_2011.pkl', 'rb') as f:
    data = pickle.load(f)
    
#import the LEH04 model function
from LEH04 import LEH04ensembles

#LEH04 param
Cs= 0.003
   
#loop through those indicies
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
    [SigDuneErosionST,zbmST] = LEH04ensembles(dv,zb,R_st,T,Cs)
    #run it through GP
    [SigDuneErosionGP,zbmGP] = LEH04ensembles(dv,zb,R_gp,T,Cs)
    #run it through 10 'draws' from GP
    [SigDuneErosionGPD,zbmGPD] = LEH04ensembles(dv,zb,R_gp_draws,T,Cs)
    
 
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
    
#perhaps a line to save this new dictionary...  
    
    