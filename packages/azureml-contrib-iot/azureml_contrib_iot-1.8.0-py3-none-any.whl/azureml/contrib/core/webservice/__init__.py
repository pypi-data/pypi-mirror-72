# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This package contains classes used to manage Compute Targets objects within Azure Machine Learning."""

from azureml._base_sdk_common import __version__ as VERSION
from .iot import IotWebservice, IotModuleSettings, IotBaseModuleSettings

__version__ = VERSION

__all__ = [
    'IotWebservice',
    'IotModuleSettings',
    'IotBaseModuleSettings'
]
