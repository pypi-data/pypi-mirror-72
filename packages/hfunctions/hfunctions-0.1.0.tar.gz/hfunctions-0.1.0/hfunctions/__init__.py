from hfunctions._hfunctions import create_sample_df
from hfunctions._hfunctions import random_actual_prediction

from pkg_resources import get_distribution


def _get_version_from_setuptools():
    return get_distribution("hfunctions").version


__author__ = """Ahmed Salhin"""
__email__ = 'ahmed@salhin.org'
__version__ = _get_version_from_setuptools()
__all__ = ['__version__', "create_sample_df", "random_actual_prediction"]
