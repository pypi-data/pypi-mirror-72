# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO plugin for LLG format."""


import logging

import numpy as np

from ...fields.field import Field


_log = logging.getLogger(__name__)

file_extensions = ('.llg',)  # Recognised file extensions


def reader(filename, scale=None, vector=None, **kwargs):
    _log.debug('Call reader')
    if vector is None:
        vector = True
    assert vector is True, 'Only vector fields can be read from the llg file format!'
    SCALE = 1.0E-9 / 1.0E-2  # From cm to nm
    data_columns = np.genfromtxt(filename, skip_header=2)
    dim = tuple(np.genfromtxt(filename, dtype=int, skip_header=1, skip_footer=len(data_columns[:, 0])))
    if scale is None:  # Otherwise overwrite!
        stride_x = 1  # x varies fastest
        stride_y = dim[2]  # one y step for dim[2] x steps
        stride_z = dim[1] * dim[2]  # one z step for one x-y layer (dim[1]*dim[2])
        scale_x = (data_columns[stride_x, 0] - data_columns[0, 0]) / SCALE  # first column varies in x
        scale_y = (data_columns[stride_y, 1] - data_columns[0, 1]) / SCALE  # second column varies in y
        scale_z = (data_columns[stride_z, 2] - data_columns[0, 2]) / SCALE  # third column varies in z
        scale = (scale_z, scale_y, scale_x)
    x_mag, y_mag, z_mag = data_columns[:, 3:6].T
    data = np.stack((x_mag.reshape(dim), y_mag.reshape(dim), z_mag.reshape(dim)), axis=-1)
    return Field(data, scale, vector=True)


def writer(filename, field, **kwargs):
    _log.debug('Call writer')
    assert field.vector and len(field.dim) == 3, 'Only 3D vector fields can be saved to the llg file format!'
    SCALE = 1.0E-9 / 1.0E-2  # from nm to cm
    # Create 3D meshgrid and reshape it and the field into a list where x varies first:
    zzz, yyy, xxx = (np.indices(field.dim) + 0.5) * np.reshape(field.scale, (3, 1, 1, 1)) * SCALE  # broadcast shape!
    z_coord, y_coord, x_coord = np.ravel(zzz), np.ravel(yyy), np.ravel(xxx)  # Turn into vectors!
    x_comp, y_comp, z_comp = field.comp  # Extract scalar field components!
    x_vec, y_vec, z_vec = np.ravel(x_comp.data), np.ravel(y_comp.data), np.ravel(z_comp.data)  # Turn into vectors!
    data = np.array([x_coord, y_coord, z_coord, x_vec, y_vec, z_vec]).T
    # Save data to file:
    with open(filename, 'w') as mag_file:
        mag_file.write('LLGFileCreator: EMPyRe vector Field\n')
        mag_file.write('    {:d}    {:d}    {:d}\n'.format(*field.dim))
        mag_file.writelines('\n'.join('   '.join('{:7.6e}'.format(cell) for cell in row) for row in data))
