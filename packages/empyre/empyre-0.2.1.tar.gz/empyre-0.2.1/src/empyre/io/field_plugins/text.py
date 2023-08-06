# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO plugin for simple text format."""


import logging
import ast

import numpy as np

from ...fields.field import Field


_log = logging.getLogger(__name__)

file_extensions = ('.txt',)  # Recognised file extensions


def reader(filename, scale=None, vector=None, **kwargs):
    _log.debug('Call reader')
    if vector is None:
        vector = False
    assert vector is False, 'Only scalar 2D fields can currently be read with this file reader!'
    with open(filename, 'r') as load_file:  # Read data:
        empyre_format = load_file.readline().startswith('EMPYRE-FORMAT')
        if empyre_format:  # File has EMPyRe structure:
            scale = ast.literal_eval(load_file.readline()[8:-4])  # [8:-4] takes just the scale string!
            data = np.loadtxt(filename, delimiter='\t', skiprows=2)  # skips header!
        else:  # Try default with provided kwargs:
            scale = 1.0 if scale is None else scale  # Set default if not provided!
            data = np.loadtxt(filename, **kwargs)
    return Field(data, scale=scale, vector=False)


def writer(filename, field, with_header=True, **kwargs):
    _log.debug('Call writer')
    assert not field.vector, 'Vector fields can currently not be saved to text!'
    assert len(field.dim) == 2, 'Only 2D fields can currenty be saved to text!'
    if with_header:  # write header:
        with open(filename, 'w') as save_file:
            save_file.write('EMPYRE-FORMAT\n')
            save_file.write(f'scale = {field.scale} nm\n')
        save_kwargs = {'fmt': '%7.6e', 'delimiter': '\t'}
    else:
        save_kwargs = kwargs
    with open(filename, 'ba') as save_file:  # the 'a' is for append!
        np.savetxt(save_file, field.data, **save_kwargs)
