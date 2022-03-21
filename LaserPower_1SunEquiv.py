# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 17:47:59 2022

@author: Dane
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define constants for the calculation:

wavelength = 532 # nm, wavelength
d = 600*1e-7 # cm, film thickness

#%% Load data sets
Abs_Coeff_Data = np.loadtxt('PDSAbsorptionData.txt', skiprows = 1)
Wavelength_Abs_Coeff = Abs_Coeff_Data[:,0]
Abs_Coeff = Abs_Coeff_Data[:,1]

AM1p5_Data = np.loadtxt('astmg173.txt', skiprows = 2)
Wavelength_AM1p5 = AM1p5_Data[:,0]
AM1p5 = AM1p5_Data[:,2]

#%% Interpolate the data
Wavelength_interp = np.linspace(min(Wavelength_Abs_Coeff), max(Wavelength_Abs_Coeff), 1000)

f = interp1d(Wavelength_Abs_Coeff, Abs_Coeff)
Abs_Coeff_interp = f(Wavelength_interp)

f2 = interp1d(Wavelength_AM1p5, AM1p5)
AM1p5_interp = f2(Wavelength_interp)


#%% Plot data to check that it looks right
# plt.figure()
# plt.plot(Wavelength_Abs_Coeff, Abs_Coeff)
# plt.plot(Wavelength_interp, Abs_Coeff_interp)

# plt.figure()
# plt.plot(Wavelength_AM1p5, AM1p5)
# plt.plot(Wavelength_interp, AM1p5_interp)

#%% Define some useful functions
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return Abs_Coeff_interp[idx]

# calculate the optical density at the laser excitation wavelength for a specified thickness
OD_value = find_nearest(Wavelength_interp, wavelength)*d


# define the function to calculate the power density for a certain wavelength to reach the same absorbed photon flux as AM1.5
def Power_Density():
    Bandwidth = Wavelength_interp[1]-Wavelength_interp[0]
    Sun_flux = AM1p5_interp*Wavelength_interp*(1-np.exp(-Abs_Coeff_interp*d))*Bandwidth
    Laser_flux = wavelength*(1-np.exp(-OD_value))
    Laser_power = np.sum(Sun_flux)/Laser_flux
    return Laser_power

print(f'{Power_Density()*1e3/1e4:.4}', 'mW/cm2')