from pycbc.waveform import get_td_waveform, get_fd_waveform, get_fd_waveform_from_td
from pycbc.types import TimeSeries
import numpy as np
from matplotlib import pyplot as plt

#################
#different masses
#################

for m1 in [10, 20, 100]:
    hp, hc = get_td_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = m1, mass2 = 15, f_lower=15,
                         delta_t=1.0/4096, Phi0=0, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=20, inclination=0.78, eccentricity=1.11)
    plt.plot(hp.sample_times, hp, label=m1)

#plt.xlim(-4, 4)
plt.ylabel('Strain')
plt.xlabel('Time (s)')
plt.legend()
plt.show()


####################
#different distances
####################

for d in [10, 20, 50, 80, 100]:
    hp, hc = get_td_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = 20, mass2 = 15, f_lower=15,
                         delta_t=1.0/4096, Phi0=0, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=d, inclination=0.78, eccentricity=1.11)
    plt.plot(hp.sample_times, hp, label=d)

#plt.xlim(-4, 4)
plt.ylabel('Strain')
plt.xlabel('Time (s)')
plt.legend()
plt.show()


#########################
#different eccentricities
#########################

for e in [1.01, 1.11, 1.58, 1.80]:
    hp, hc = get_td_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = 20, mass2 = 15, f_lower=15,
                         delta_t=1.0/4096, Phi0=0, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=20, inclination=0.78, eccentricity=e)
    plt.plot(hp.sample_times, hp, label=e)

#plt.xlim(-4, 4)
plt.ylabel('Strain')
plt.xlabel('Time (s)')
plt.legend()
plt.show()


##################################
#different orbital azimuthal angle
##################################
for phi in [0, 1.0, 2.0, 3.0]:
    hp, hc = get_td_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = 20, mass2 = 15, f_lower=15,
                         delta_t=1.0/4096, Phi0=phi, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=20, inclination=0.78, eccentricity=1.11)
    plt.plot(hp.sample_times, hp, label=phi)

#plt.xlim(-4, 4)
plt.ylabel('hp')
plt.xlabel('Times(sec)')
plt.legend()
plt.show()






