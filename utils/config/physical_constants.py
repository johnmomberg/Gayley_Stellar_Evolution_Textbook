import numpy as np 
import math 




# Define physical constants (in CGS units)
G = 6.67e-8                 # Gravitional constant 
c = 2.998e10                # Speed of light (cm/sec)
sigma_sb = 5.6703744e-5     # Stefan-Boltzmann constant 
h = 6.6261e-27              # Planck constant (erg*sec) 
k = 1.38e-16                # Boltzmann constant 

# # Unit conversions  
# secs_per_year = 3.154e7     # Seconds in a year 
# cm_per_km = 1e5             # Centimeters in a kilometer 
# cm_per_Mpc = 3.086e24       # Centimeters in a Megaparsec 
RotPerDay_per_RadPerSec = 24*3600 / (2*np.pi) 
RadPerSec_per_RotPerDay = 1/RotPerDay_per_RadPerSec 
cm_per_AU = 1.496e+13 # Centimeters in an Astronomical Unit 

# # Cosmology 
# H_0=70*cm_per_km/cm_per_Mpc # Hubble constant, H_0 = 70 km/sec/Mpc, converted to cm/sec/cm to keep units consistent 
# Omega_m0 = 0.3              # Matter (dark matter + baryons) fraction 

# Sun 
M_sun = 1.989e33            # Mass of the sun (grams)
R_sun = 6.96e10             # Radius of the sun (cm)
L_sun = 3.826e33            # Luminosity of the sun 

# Particles 
m_e = 9.109e-28             # Mass of electron (grams)
m_p = 1.6726e-24            # Mass of proton (grams)




