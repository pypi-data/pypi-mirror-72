"""Top-level package for tfields."""

__author__ = """Daniel Böckenhoff"""
__email__ = 'dboe@ipp.mpg.de'
__version__ = '0.2.0'

from . import plotting
from . import log  # NOQA
from . import path  # NOQA

plotting.use('matplotlib')
