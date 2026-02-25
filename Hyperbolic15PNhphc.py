import hyperbolic_waveform_generate
import numpy as np
from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
pi = np.pi
from pycbc.waveform import get_td_waveform
from pycbc.waveform import td_approximants, fd_approximants
import pycbc.conversions
from pycbc.types import TimeSeries
import pycbc.coordinates as cord

def hyperbolic_waveform_td(**kwds):
    m1 = kwds['mass1']
    m2 = kwds['mass2']
    R = kwds['distance']
    Theta = kwds['inclination']
    spin1_a, spin1_polar, spin1_azimuthal = cord.cartesian_to_spherical(kwds['spin1x'], kwds['spin1y'], kwds['spin1z'])
    spin2_a, spin2_polar, spin2_azimuthal = cord.cartesian_to_spherical(kwds['spin2x'], kwds['spin2y'], kwds['spin2z'])
    kwds.update({
        'spin1_a': spin1_a,
        'spin1_polar': spin1_polar,
        'spin1_azimuthal': spin1_azimuthal,
        'spin2_a': spin2_a,
        'spin2_polar': spin2_polar,
        'spin2_azimuthal': spin2_azimuthal
    })
    chi1 = kwds['spin1_a']
    chi2 = kwds['spin2_a']
    phi1i = kwds['spin1_azimuthal']
    phi2i = kwds['spin2_azimuthal']
    theta1i = kwds['spin1_polar']
    theta2i = kwds['spin2_polar']
    delta_t = kwds['delta_t']
    phi0 = kwds['coa_phase']
    vmax =  kwds.get('alpha', kwds.get('vmax'))
    duration = kwds.get('alpha1', kwds.get('duration'))
    et0 = kwds.get('alpha2', kwds.get('eccentricity'))

    hp, hc = hyperbolic_waveform_generate.hphc_15PN(
    m1=m1,
    m2=m2,
    chi1=chi1,
    theta1i=theta1i,
    phi1i=phi1i,
    chi2=chi2,
    theta2i=theta2i,
    phi2i=phi2i,
    et0=et0,
    phi0=phi0,
    Theta=Theta,
    R=R,
    delta_t=delta_t,
    vmax=vmax,
    duration=duration
    )

    hp = TimeSeries(hp, delta_t)
    hc = TimeSeries(hc, delta_t)
    # Find the peak time and shift both hp and hc (in time) with the same amount
    t_shift_hp = hp.sample_times[np.argmax(hp)]
    t_shift_hc = hc.sample_times[np.argmax(hc)]

    hp = TimeSeries(hp.data, delta_t, epoch=-t_shift_hp)
    hc = TimeSeries(hc.data, delta_t, epoch=-t_shift_hc)

    hp_tapered = hp.taper_timeseries('TAPER_STARTEND')
    hc_tapered = hc.taper_timeseries('TAPER_STARTEND')

    return hp_tapered, hc_tapered

def hyperbolic_waveform_fd(**kwds):
    if 'approximant' in kwds:
        kwds.pop('approximant')

    kwds.update({
        "approximant": "Hyperbolic15PNhphc",
    })
    nparams = kwds.copy()

    if 'f_fref' not in nparams:
        nparams['f_ref'] = kwds['f_lower']

    # Determine an appropriate delta_t based on waveform end frequency
    try:
        f_end = get_waveform_end_frequency(**kwds)
        # Choose power-of-two sampling rate (important for FFT speed)
        sample_rate = pnutils.nearest_larger_binary_number(f_end)
        delta_t = 0.5 / sample_rate
    except:
        # fallback to a safe default
        delta_t = 1.0 / 2048

    nparams['delta_t'] = delta_t

    # Generate the TD waveform
    hp, hc = get_td_waveform(**nparams)

    # Resize to the right duration in frequency domain
    tsamples = int(1.0 / kwds['delta_f'] / delta_t)
    if tsamples < len(hp):
        raise ValueError(
            "The frequency spacing (df = {}) is too low to "
            "generate the {} approximant from the time domain".format(
                kwds['delta_f'], kwds['approximant']
            )
        )

    # Convert to frequency series and shift
    hp = hp.to_frequencyseries().cyclic_time_shift(hp.start_time)
    hc = hc.to_frequencyseries().cyclic_time_shift(hc.start_time)

    return hp, hc

