
"""
Script to make plots of the dune profile

EBG Aug. 2018 (Matlab); Nov 2018 (Python)
"""


import pickle
import numpy as np
import matplotlib.pyplot as plt

from LEH04 import LEH04ensembles

with open('DIM_data_2011.pkl', 'rb') as f:
    data = pickle.load(f)

#profile #
p=15;
#number of ensembles
ens=10;
#LEH04 erosion paramerer
Cs= 0.003

profile=data[p]
    
#pull all relevant data out of the dictionary
dv = profile['dv']
zb = profile['zb']
T = profile['Tp']
R_st = profile['R_st']
R_gp = profile['R_gp']
R_gp_draws = profile['R_gp_draws']

#run it through GP
[SigDuneErosionGP,zbmGP] = LEH04ensembles(dv,zb,R_gp,T,Cs)
#run it through 10 'draws' from GP
[SigDuneErosionGPD,zbmGPD] = LEH04ensembles(dv,zb,R_gp_draws,T,Cs)


#plotting
t = np.arange(0, 120)
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, R_gp_draws[:,0:11],'gray',t, R_gp,'b', t,zbmGPD[:,0:11],'gray',t,zbmGP,'k',119,profile['zb_final'],'.k')

axs[0].set_xlabel('time (hours)')
axs[0].set_ylabel('Runup elevation (blue) and Dune Toe Height (black)')

axs[1].plot(t, SigDuneErosionGPD[:,0:11],'gray', t, SigDuneErosionGP,'b',119,profile['dv_obs'],'.k')
axs[1].set_ylabel('total delV')

plt.show()

