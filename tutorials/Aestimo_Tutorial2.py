# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 09:40:24 2024

@author: wmaineult
"""

import aestimo as solver
import config as ac
ac.messagesoff = True # turn off logging in order to keep notebook from being flooded with messages.
import database as adatabase
import numpy as np
import matplotlib.pyplot as plt
import copy
from pprint import pprint


#%% Initialise the structure
class Structure(object): pass
s0 = Structure() # this will be our datastructure

# TEMPERATURE
s0.T = 15.0 #Kelvin

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

# REGIONS
# Region input is a two-dimensional list input.
#         | Thickness (nm) | Material | Alloy fraction | Doping(cm^-3) | n or p type |
s0.material =[
            [ 20.0, 'AlGaAs', 0.3, 0.0, 'n'],
            [ 11.0, 'GaAs', 0, 2e16, 'n'],
            [ 20.0, 'AlGaAs', 0.3, 0.0, 'n'],
            ]

structure0 = s0


#%% simple qw calculation

model = solver.StructureFrom(structure0,adatabase) # structure could also be a dictionary.
    
#calculate QW states
result = solver.Poisson_Schrodinger(model)

#solver.save_and_plot(result,model) # Write the simulation results in files
plot = solver.QWplot(result,figno=None) # Plot QW diagram
solver.logger.info("Simulation is finished.")


#%% Double QW

s1 = copy.copy(s0) #simpler than redefining everything and changes to s0 should propagate to s1
s1.material = [
            [ 20.0, 'AlGaAs', 0.3, 0.0, 'n'],
            [ 11.0, 'GaAs', 0, 2e16, 'n'],
            [ 2.0, 'AlGaAs', 0.3, 0.0, 'n'], #barrier layer
            [ 11.0, 'GaAs', 0, 2e16, 'n'],            
            [ 20.0, 'AlGaAs', 0.3, 0.0, 'n'],
            ]
barrier_layer = 2 # defines which layer will be adjusted later
s1.subnumber_e = 6 # There will be double the number of energy states now.

# Initialise structure class
model1 = solver.StructureFrom(s1,adatabase) # structure could also be a dictionary.

#calculate QW states
result1 = solver.Poisson_Schrodinger(model1)

#solver.save_and_plot(result,model)
fig1 = solver.QWplot(result1,figno=None)
solver.logger.info("Simulation is finished.")

# print 'state, Energy'
# # print '     ,meV'

# for num,E in zip(range(result1.subnumber_e),result1.E_state):
#     print('%5d %7g' %(num,E))


#%% Vary the barrier width
q = 1.602176e-19 #C
meV2J=1e-3*q #meV to Joules
# Shooting method parameters for Schrödinger Equation solution
ac.delta_E = 0.005*meV2J #Energy step (Joules) for initial search. Initial delta_E is 1 meV. 
#ac.d_E = 1e-5*meV2J #Energy step (Joules) within Newton-Raphson method when improving the precision of the energy of a found level.
#ac.E_start = 0.0    #Energy to start shooting method from (if E_start = 0.0 uses minimum of energy of bandstructure)
#ac.Estate_convergence_test = 1e-9*meV2J

def set_barrier(d):
    """Sets barriers between the two QWs to d (nm)."""
    model1.material[barrier_layer][0] = d
    model1.create_structure_arrays() # update the instance's internals

results = []
barriers = np.arange(1,11)
for barrier in barriers:
    set_barrier(barrier)
    resulti = solver.Poisson_Schrodinger(model1)
    results.append(resulti.E_state)

results = np.array(results)

ax1 = plt.subplot(111)
for level in results.transpose(): ax1.plot(barriers,level)
ax1.invert_xaxis()
ax1.set_xlabel("barrier thickness (nm)")
ax1.set_ylabel("Energy (meV)")
plt.show()

#%% vary the qw energy

ac.delta_E = 0.2*meV2J #Energy step (Joules) for initial search. Initial delta_E is 1 meV. 

s2 = copy.copy(s0) #simpler than redefining everything and changes to s0 should propagate to s1
s2.material = [
            [ 20.0, 'AlGaAs', 0.3, 0.0, 'n'],
            [ 11.0, 'GaAs', 0, 2e16, 'n'],
            [ 2.0, 'AlGaAs', 0.3, 0.0, 'n'], #barrier layer
            [ 9.0, 'GaAs', 0, 2e16, 'n'],            
            [ 20.0, 'AlGaAs', 0.3, 0.0, 'n'],
            ]
well2_layer = 3 # defines which layer will be adjusted later
s2.subnumber_e = 6 # There will be double the number of energy states now.

# Initialise structure class
model2 = solver.StructureFrom(s2,adatabase) # structure could also be a dictionary.

def set_well(d):
    """Sets barriers between the two QWs to d (nm)."""
    model2.material[well2_layer][0] = d
    model2.create_structure_arrays() # update the instance's internals
    
# turn off logging
solver.logger.setLevel("WARNING")
    
#calculate QW states
results2 = []
well_thicknesses = np.linspace(8.0,14.0,200)
for barrier in well_thicknesses:
    set_well(barrier)
    resulti = solver.Poisson_Schrodinger(model2)
    results2.append(resulti.E_state)

results2 = np.array(results2)

ax2 = plt.subplot(111)
for level in results2.transpose(): ax2.plot(well_thicknesses,level)
ax2.set_xlabel("2nd well thickness (nm)")
ax2.set_ylabel("Energy (meV)")
