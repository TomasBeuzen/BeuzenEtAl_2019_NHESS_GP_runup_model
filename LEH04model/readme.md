##Dune erosion Model:

There are four routines here for using GP runup esitmates in the Larson, Erikson, Hanson (2004) model of dune erosion (http://doi.org/10.1016/j.coastaleng.2004.07.003):

**LEH04.py** — this is the ‘core’ routine, with a single function that implements the LEH04 model

**BatchDuneErosion.py** — this script loops through the data dictionary and calls LEH04.py to erode the dune at each profile, and for each runup model (Stockdon, GP, GP ensembles)

**DuneProfilePlots.py** —this script plots the timeseries of a single user-defined profile. Specifically the mean and ensemble Runup, mean and ensemble zb, and mean and ensemble dV. User specifies the number of ensembles to plot, and the Cs value for the LEH04 model

**Parameter Tuning.py** — this script is like BatchDuneErosion.py, but with an extra loop for variations in Cs. It has a plotting routine at the end to show how changes in Cs result in changes in mean error for each model, and ‘capture rate’ for the ensembles. 
 
