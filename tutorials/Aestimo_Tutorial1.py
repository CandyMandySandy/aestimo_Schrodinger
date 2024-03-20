# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:26:24 2024

@author: wmaineult
"""



import aestimo as solver

#%% Config file
import config as ac

q = 1.602176e-19 #C
meV2J=1e-3*q #meV to Joules

# Input File(s)
# -------------
ac.inputfilename = "sample-qw-barrierdope"
#ac.inputfilename = "sample-qw-qwdope"
#ac.inputfilename = "sample-moddop"
#ac.inputfilename = "sample-qw-HarrisonCh3_3"
#ac.inputfilename = "sample-qw-barrierdope-p"
#ac.inputfilename = "sample-double-qw"

# Calculation
# -----------
# Aestimo / Aestimo_numpy
ac.use_cython = True #provides a speed up for aestimo and aestimo_numpy
# Shooting method parameters for Schrödinger Equation solution
ac.delta_E = 0.5*meV2J #Energy step (Joules) for initial search. Initial delta_E is 1 meV. 
ac.d_E = 1e-5*meV2J #Energy step (Joules) within Newton-Raphson method when improving the precision of the energy of a found level.
ac.E_start = 0.0    #Energy to start shooting method from (if E_start = 0.0 uses minimum of energy of bandstructure)
ac.Estate_convergence_test = 1e-9*meV2J
# FermiDirac
ac.FD_d_E = 1e-9 #Initial and minimum Energy step (meV) for derivative calculation for Newton-Raphson method to find E_F
ac.FD_convergence_test = 1e-6 #meV
ac.np_d_E = 1.0 # Energy step (meV) for dispersion calculations
# Poisson Loop
ac.damping = 0.5    #averaging factor between iterations to smooth convergence.
ac.max_iterations=80 #maximum number of iterations.
ac.convergence_test=1e-6 #convergence is reached when the ground state energy (meV) is stable to within this number between iterations.

# Aestimo_numpy_h
ac.strain = True # for aestimo_numpy_h
ac.piezo=True
#Set material type used in the structure 
ac.Wurtzite=True
ac.Zincblind=False

# Output Files
# ------------
ac.output_directory = "outputs"
ac.parameters = True
ac.electricfield_out = True
ac.potential_out = True
ac.sigma_out = True
ac.probability_out = True
ac.states_out = True

# Result Viewer
# -------------
ac.resultviewer = True
ac.wavefunction_scalefactor = 200 # scales wavefunctions when plotting QW diagrams
# Messages
# --------
ac.messagesoff = False
ac.logfile = 'aestimo.log'

ac.use_cython = False
ac.messagesoff = True

#%% Database part 
import database as adatabase
from pprint import pprint

pprint(adatabase.materialproperty['GaAs'])

#%% Structure 

class Structure(object): pass
s = Structure() # this will be our datastructure

# TEMPERATURE
s.T = 60.0 #Kelvin

# COMPUTATIONAL SCHEME
# 0: Schrodinger
# 1: Schrodinger + nonparabolicity
# 2: Schrodinger-Poisson
# 3: Schrodinger-Poisson with nonparabolicity
# 4: Schrodinger-Exchange interaction
# 5: Schrodinger-Poisson + Exchange interaction
# 6: Schrodinger-Poisson + Exchange interaction with nonparabolicity
s.computation_scheme = 3

# Non-parabolic effective mass function
# 0: no energy dependence
# 1: Nelson's effective 2-band model
# 2: k.p model from Vurgaftman's 2001 paper
s.meff_method = 2

# Non-parabolic Dispersion Calculations for Fermi-Dirac
s.fermi_np_scheme = True #needed only for aestimo_numpy2.py

# QUANTUM
# Total subband number to be calculated for electrons
s.subnumber_e = 3
# Total subband number to be calculated for electrons (needed only for aestimo_numpy_h)
s.subnumber_h = 1 

# APPLIED ELECTRIC FIELD
s.Fapplied = 0.00/50e-9 # (V/m)

# --------------------------------
# REGIONAL SETTINGS FOR SIMULATION
# --------------------------------

# GRID
# For 1D, z-axis is choosen
s.gridfactor = 0.1 #nm
s.maxgridpoints = 200000 #for controlling the size

# REGIONS
# Region input is a two-dimensional list input.
# An example:
#         | Thickness (nm) | Material | Alloy fraction | Doping(cm^-3) | n or p type |
# Layer 0 |      250.0     |   Si     |      0         |     1e16      |     n       |
# Layer 1 |      250.0     |   Si     |      0         |     1e16      |     p       |
#
s.material =[[ 10.0, 'AlGaAs', 0.3, 0.0, 'n'],
            [ 5.0, 'AlGaAs', 0.3, 5e17, 'n'],
            [ 5.0, 'AlGaAs', 0.3, 0.0, 'n'],
            [ 11.0, 'GaAs', 0, 0, 'n'],
            [ 5.0, 'AlGaAs', 0.3, 0.0, 'n'],
            [ 5.0, 'AlGaAs', 0.3, 5e17, 'n'],
            [ 10.0, 'AlGaAs', 0.3, 0.0, 'n']]

structure = s
model = solver.StructureFrom(structure,adatabase) # structure could also be a dictionary.
    
#calculate QW states
result = solver.Poisson_Schrodinger(model)

# Write the simulation results in files
# %matplotlib inline
solver.save_and_plot(result,model)
solver.logger.info("Simulation is finished.")