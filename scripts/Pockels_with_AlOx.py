# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:40:24 2024

@author: wmaineult
"""

import aestimo as solver
import config as ac
ac.messagesoff = True # turn off logging in order to keep notebook from being flooded with messages.
from database import adatabase
import numpy as np
import matplotlib.pyplot as plt
from copy import copy
from pprint import pprint
import pandas as pd


#%% Initialise the structure
class Structure(object): pass
s0 = Structure() # this will be our datastructure

# TEMPERATURE
s0.T = 300.0 #Kelvin

# COMPUTATIONAL SCHEME
# 0: Schrodinger
# 1: Schrodinger + nonparabolicity
# 2: Schrodinger-Poisson
# 3: Schrodinger-Poisson with nonparabolicity
# 4: Schrodinger-Exchange interaction
# 5: Schrodinger-Poisson + Exchange interaction
# 6: Schrodinger-Poisson + Exchange interaction with nonparabolicity
s0.computation_scheme = 0

# Non-parabolic effective mass function
# 0: no energy dependence
# 1: Nelson's effective 2-band model
# 2: k.p model from Vurgaftman's 2001 paper
s0.meff_method = 0

# Non-parabolic Dispersion Calculations for Fermi-Dirac
s0.fermi_np_scheme = True #needed only for aestimo_numpy2.py

# QUANTUM
# Total subband number to be calculated for electrons
s0.subnumber_e = 3

# APPLIED ELECTRIC FIELD
s0.Fapplied = 0.00 # (V/m)

# GRID
# For 1D, z-axis is choosen
s0.gridfactor = 0.1 #nm
s0.maxgridpoints = 200000 #for controlling the size
# s0.use_cython=False
# REGIONS
# Region input is a two-dimensional list input.
#         | Thickness (nm) | Material | Alloy fraction | Doping(cm^-3) | n or p type |
# s0.material = [
#             [ 5, 'AlOx', 1, 0.0, 'n'],
#             [ 2,  'InGaAs', 0.3, 5e18, 'n'],
#             [ 0.5,  'GaAs', 0, 5e18, 'n'],
#             [ 2, 'GaAsP', 0.7, 0.0, 'n'], #barrier layer
#             [ 5, 'AlOx', 1, 0, 'n'],       
#             ]


s0.material = [
            [ 5, 'AlOx', 1, 0.0, 'n'],
            [ 2,  'InGaAs', 0.3, 5e18, 'n'],
            [ 0.5,  'GaAs', 0, 5e18, 'n'],
            [ 2, 'AlAsP', 0.7, 0.0, 'n'], #barrier layer
            [ 5, 'AlOx', 1, 0, 'n'],       
            ]

s0.valley = 'Gamma'




#%% Caculation in the GammaBand -> going to AlAs

model = solver.StructureFrom(s0,adatabase) # structure could also be a dictionary.
    
#calculate QW states
result = solver.Poisson_Schrodinger(model)

#solver.save_and_plot(result,model) # Write the simulation results in files
fig1 = solver.QWplot(result,figno=None) # Plot QW diagram
solver.logger.info("Simulation is finished.")


#%% Calcualtion in the X band

s1 = copy(s0) #simpler than redefining everything and changes to s0 should propagate to s1

s1.valley = 'X'

# Initialise structure class
model1 = solver.StructureFrom(s1,adatabase) # structure could also be a dictionary.

#calculate QW states
result1 = solver.Poisson_Schrodinger(model1)

#solver.save_and_plot(result,model)
# fig2 = solver.QWplot(result1,figno=None)
fig3 = solver.QWplot_compare(results = [result, result1],
                             labels = pd.Index(['Gamma', 'X'], name='Valley'), 
                             plot_only = [0,1,2,3,4,5])
fig3.axes[0].set_ylim([800,1000])
solver.logger.info("Simulation is finished.")

# print 'state, Energy'
# # print '     ,meV'

# for num,E in zip(range(result1.subnumber_e),result1.E_state):
#     print('%5d %7g' %(num,E))

#%% Caculation in the GammaBand -> going to GaAs
s2 = copy(s0)
s2.material = [
            [ 10, 'AlAs', 0, 2e18, 'n'],
            [ 3, 'GaAs', 0, 4e18, 'n'],   
            [ 2.5, 'AlAs', 1, 0.0, 'n'],
            [ 3, 'GaAs', 0, 4e18, 'n'],
            [ 2.5, 'AlAs', 1, 0.0, 'n'], #barrier layer
            [ 3, 'GaAs', 0, 4e18, 'n'],       
            [ 2.5, 'AlAs', 1, 0.0, 'n'], #barrier layer
            [ 10, 'AlGaAs', 0.20, 5e18, 'n'],
            ]

s2.valley = 'Gamma'

model2 = solver.StructureFrom(s2,adatabase) # structure could also be a dictionary.
    
#calculate QW states
result2 = solver.Poisson_Schrodinger(model2)

#solver.save_and_plot(result,model) # Write the simulation results in files
# fig1 = solver.QWplot(result,figno=None) # Plot QW diagram
solver.logger.info("Simulation is finished.")


#%% Calcualtion in the X band

s3 = copy(s2) #simpler than redefining everything and changes to s0 should propagate to s1

s3.valley = 'X'

# Initialise structure class
model3 = solver.StructureFrom(s3,adatabase) # structure could also be a dictionary.

#calculate QW states
result3 = solver.Poisson_Schrodinger(model3)

#solver.save_and_plot(result,model)
# fig2 = solver.QWplot(result1,figno=None)
fig3 = solver.QWplot_compare(results = [result2, result3],
                             labels = pd.Index(['Gamma', 'X'], name='Valley'), 
                             plot_only = [0,1,2,3,4,5])
fig3.axes[0].set_ylim([800,1000])
solver.logger.info("Simulation is finished.")