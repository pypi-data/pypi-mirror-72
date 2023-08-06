# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO plugin for the numpy format."""


import logging

import numpy as np

from ...fields.field import Field


_log = logging.getLogger(__name__)

file_extensions = ('.npy', '.npz')  # Recognised file extensions


def reader(filename, scale=None, vector=None, **kwargs):
    _log.debug('Call reader')
    if vector is None:
        vector = False
    if scale is None:
        scale = 1.0
    return Field(np.load(filename, **kwargs), scale, vector)


def writer(filename, field, **kwargs):
    _log.debug('Call writer')
    np.save(filename, field.data, **kwargs)
