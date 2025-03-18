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
    dt = kwds['delta_t']
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

    hp, hc = hyperbolic_waveform_generate.hphc_15PN(vmax, duration, chi1, \
                    theta1i, phi1i, chi2, theta2i, phi2i, \
                    m1, m2, et0, R, Theta, delta_t, phi0)

    hp = TimeSeries(hp, delta_t)
    hc = TimeSeries(hc, delta_t)

    # t = hp.sample_times - hp.sample_times[np.argmax(hp)+1]
    #hp = TimeSeries(hp, delta_t, epoch=min(t))
    #hc = TimeSeries(hc, delta_t, epoch=min(t))

    # Find the peak time and shift the time axis
    t_shift = hp.sample_times[np.argmax(hp)]

    hp = TimeSeries(hp.data, delta_t, epoch=-t_shift)
    hc = TimeSeries(hc.data, delta_t, epoch=-t_shift)

    return hp, hc


def hyperbolic_waveform_fd(**kwds):
    from pycbc.waveform import get_td_waveform
    from pycbc.waveform.utils import apply_fseries_time_shift
    from pycbc.waveform import td_approximants, fd_approximants
    from pycbc.waveform import utils as wfutils
    import numpy as np
    if 'approximant' in kwds:
        kwds.pop('approximant')
    #hp, hc = get_td_waveform(approximant="Hyperbolic15PNhphc", **kwds)

    kwds.update({
        "approximant": "Hyperbolic15PNhphc",
        })
    nparams = kwds.copy()

    #full_duration = duration = len(hp)*hp.delta_t

    if 'f_fref' not in nparams:
        nparams['f_ref'] = kwds['f_lower']
    # We'll try to do the right thing and figure out what the frequency
    # end is. Otherwise, we'll just assume 2048 Hz.
    # (consider removing as we hopefully have better estimates for more
    # approximants
    try:
        f_end = get_waveform_end_frequency(**kwds)
        delta_t = (0.5 / pnutils.nearest_larger_binary_number(f_end))
    except:
        delta_t = 1.0 / 2048
    nparams['delta_t'] = delta_t
    hp, hc = get_td_waveform(**nparams)
    # Resize to the right duration
    tsamples = int(1.0 / kwds['delta_f'] / delta_t)
    if tsamples < len(hp):
        raise ValueError("The frequency spacing (df = {}) is too low to "
                         "generate the {} approximant from the time "
                         "domain".format(params['delta_f'], params['approximant']))

    # apply the tapering, we will use a safety factor here to allow for
    # somewhat innacurate duration difference estimation.
    #window = (full_duration - duration) * 0.8
    #hp = wfutils.td_taper(hp, hp.start_time, hp.start_time + window)
    #hc = wfutils.td_taper(hc, hc.start_time, hc.start_time + window)
    # avoid wraparound
    hp = hp.to_frequencyseries().cyclic_time_shift(hp.start_time)
    hc = hc.to_frequencyseries().cyclic_time_shift(hc.start_time)
    return hp, hc

