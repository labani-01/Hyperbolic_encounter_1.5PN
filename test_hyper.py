from pycbc.waveform import get_td_waveform, get_fd_waveform, get_fd_waveform_from_td
from pycbc.types import TimeSeries
import numpy as np
from matplotlib import pyplot as plt

#######################################
#generate time_domain hyperbolic signal
#######################################
hp_td, hc_td = get_td_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = 20, mass2 = 15, f_lower=15,
                         delta_t=1.0/4096, Phi0=0, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=20, inclination=0.78, eccentricity=1.11)
print(hp_td, hc_td)
plt.plot(hp_td.sample_times, hp_td)
plt.show()


############################################
#generate frequecny domain hyperbolic signal
############################################
hp_fd, hc_fd = get_fd_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = 20, mass2 = 15, f_lower=15, delta_f=1/16,
                         delta_t=1.0/4096, Phi0=0, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=20, inclination=0.78, eccentricity=1.11)
print(hp_fd, hc_fd)
plt.plot(hp_fd.sample_frequencies, hp_fd)
plt.show()


#############################################################
#whiten the timeseries and convert it in the frequency domain
#############################################################
hp_td_whiten = hp_td.whiten(2, 4)
plt.plot(hp_td_whiten.sample_times, hp_td_whiten)
plt.show()
hp_fd_whiten = hp_td_whiten.to_frequencyseries()
plt.plot(hp_fd_whiten.sample_frequencies, hp_fd_whiten)
plt.show()

hc_td_whiten = hc_td.whiten(2, 4)
plt.plot(hc_td_whiten.sample_times, hc_td_whiten)
plt.show()
hc_fd_whiten = hc_td_whiten.to_frequencyseries()
plt.plot(hc_fd_whiten.sample_frequencies, hc_fd_whiten)
plt.show()

####################
#Detector's response
####################
from pycbc.detector import Detector
from pycbc.waveform import get_td_waveform

# Time, orientation and location of the source in the sky
ra = 3.7
dec = 1.0
pol = 0.2
inc = 0
time = 1187198976

#Generate a waveform
hp, hc = get_td_waveform(approximant="Hyperbolic15PNhphc",
                         mass1 = 20, mass2 = 15, f_lower=15,
                         delta_t=1.0/4096, Phi0=0, xi0=0.0005, vmax=0.2, duration=8,
                         spin1_a=1, spin1_polar=0.5, spin1_azimuthal=0.35, spin2_a=1, spin2_polar=0.8, spin2_azimuthal=1, distance=20, inclination=0.78, eccentricity=1.11)
for ifo in ["L1", "H1", "V1"]:
    d = Detector(ifo)
    fp, fc = d.antenna_pattern(ra, dec, pol, time)
    ht = fp * hp + fc * hc
    plt.plot(ht.sample_times, ht, label=ifo)
    plt.legend()
    plt.show()



###############################################
#Detector's response on frequency domain signal
###############################################

from pycbc.detector import Detector
from pycbc.waveform import get_td_waveform

# Time, orientation and location of the source in the sky
ra = 3.7
dec = 1.0
pol = 0.2
inc = 0
time = 1187198976

#Considering the whiten frequency series
for ifo in ["L1", "H1", "V1"]:
    d = Detector(ifo)
    fp, fc = d.antenna_pattern(ra, dec, pol, time)
    hf = fp * hp_fd_whiten + fc * hc_fd_whiten
    plt.plot(hf.sample_frequencies, hf, label=ifo)
    plt.legend()
    plt.show()
    
    

