# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO plugin for simple text format."""


import logging
import re

import numpy as np

from ...fields.field import Field
from ...utils.misc import interp_to_regular_grid


_log = logging.getLogger(__name__)

file_extensions = ('.tec',)  # Recognised file extensions


def reader(filename, scale=None, vector=None, **kwargs):
    assert isinstance(scale, tuple), 'The scale must be a tuple, each entry corresponding to one grid dimensions!'
    _log.debug('Call reader')
    if vector is None:
        vector = True
    assert vector is True, 'Only vector fields can be loaded from tec-files!'
    with open(filename, 'r') as mag_file:
        lines = mag_file.readlines()  # Read in lines!
        match = re.search(R'N=(\d+)', lines[2])  # Extract number of points from third line!
        if match:
            n_points = int(match.group(1))
        else:
            raise IOError('File does not seem to match .tec format!')
    n_head, n_foot = 3, len(lines) - (3 + n_points)
    # Read in data:
    data_raw = np.genfromtxt(filename, skip_header=n_head, skip_footer=n_foot)
    if scale is None:
        raise ValueError('For the interpolation of unstructured grids, the `scale` parameter is required!')
    data = interp_to_regular_grid(data_raw[:, :3], data_raw[:, 3:], scale, **kwargs)
    return Field(data, scale, vector=vector)


def writer(filename, field, **kwargs):
    _log.debug('Call writer')
    raise NotImplementedError('A writer for this extension is not yet implemented!')
