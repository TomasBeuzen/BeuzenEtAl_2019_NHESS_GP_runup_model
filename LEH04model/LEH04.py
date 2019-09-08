import numpy as np

def LEH04ensembles( dv, zb, R, T, Cs):
        
    '''
    for a given set of points x, z, delV,
    and a given Runup and period timeseries
    erode the dune based on the Larson et al 2004 model
    
    "It is easier to write a new code than to understand an old one"
    -John von Neumann to Marston Morse, 1952
    '''
    
    t = 60*60 #hourly timesteps
        
    #for each GP draws/realizations in R timeseries
    if R.ndim == 1:
        #make a 1D array to 2D array, to help with iteration
        R=np.array([R])
        R=np.transpose(R)
        draws = np.arange(0,1)
    else:
        draws = np.arange(0,(len(R[0])))
        
    #counter for cumulative dune erosion, which is length of forcing
    SigDuneErosion=0*R
    #counter for dune foot elevation, which is length of forcing
    zbm=0*R
    
    #number of timesteps  in R timeseries
    time = np.arange(0,(len(R)))
    
    for ii in draws:
        for i in time:
            #print(i)
            
            #find the dune toe elevation
            if i == 0: 
                #use the initial value from the curve, which is the pre storm
                zbp = zb[0]
            else:
                #use the model value from previous time step
                zbp = zbm[i-1,ii]
                
            #if the runup is higher than the dune toe, then erode the dune
            if R[i,ii] > zbp:
                #LEH model
                DuneErosion = 4*Cs*((R[i,ii]-zbp)**2)*(t/T[i])
            else:
                DuneErosion=0
                
            #if there was erosion    
            if DuneErosion > 0:
                #for the dune erosion calculated, find the new zb.
                #1. find cumulative dune erosion
                if i == 0 :
                    SigDuneErosion[i,ii] = DuneErosion
                else:
                    SigDuneErosion[i,ii] = DuneErosion + SigDuneErosion[i-1,ii]

                #2. Use to find the new zb, using interp
                zbm[i,ii] = np.interp(SigDuneErosion[i,ii],dv,zb)
            
                #if the new dune toe (zb) started out lower than the runup (R(i))
                #at this timestep, but now the new dune toe is higher than runup
                #( zb(i)>R(i) ), then there was over-erosion. This loop corrects
                #this problem by setting the new dune toe exactly to the runup
                #elevation; zb(i) -> R(i)
                if zbp < R[i,ii] and zbm[i,ii] > R[i,ii]:
                    zbm[i,ii] = R[i,ii]
                    #and then only erode the amount of sand to get to that
                    #readjusted height and overprint the DuneErosion number
                    SigDuneErosion[i,ii] = np.interp(zbm[i,ii],zb,dv)

            else:
                 #if there is no dune erosion, fill the new dune base and the new
                 # cumulative erosion with the previosu time step's value
                zbm[i,ii] = zbp
                if i==0:
                    SigDuneErosion[i,ii] = 0
                else:
                    SigDuneErosion[i,ii] = SigDuneErosion[i-1,ii]
                
    return [SigDuneErosion,zbm]
    
    
