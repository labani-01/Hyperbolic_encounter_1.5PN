"""
setup.py file for line of sight acceleration parameter pycbc waveform plugin package
"""

from setuptools import Extension, setup, Command
from setuptools import find_packages

VERSION = '0.0.dev0'






setup (
    name = 'pycbc-Hyperbolic15PNhphc',
    version = VERSION,
    description = 'New waveform to generate hyperbolic encounter plugin PyCBC',
    long_description = open('descr.rst').read(),
    author = 'The PyCBC team',
    author_email = 'labannyo2000@gmail.org',
    url = 'http://www.pycbc.org/',
    download_url = 'https://github.com/labani-01/Hyperbolic_encounter_1.5PN',
    keywords = ['pycbc', 'signal processing', 'gravitational waves'],
    install_requires = ['pycbc'],
    py_modules = ['hyperbolic_waveform_generate','Hyperbolic15PNhphc'],
    entry_points = {"pycbc.waveform.td":"Hyperbolic15PNhphc = Hyperbolic15PNhphc:hyperbolic_waveform_td", 
                    "pycbc.waveform.fd": "Hyperbolic15PNhphc = Hyperbolic15PNhphc:hyperbolic_waveform_fd"},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)

