# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO plugin for simple text format."""


import logging
from numbers import Number

import numpy as np

from ...fields.field import Field
from ...utils.misc import interp_to_regular_grid
from ...vis import colors


_log = logging.getLogger(__name__)

file_extensions = ('.vtk',)  # Recognised file extensions


def reader(filename, scale=None, vector=None, **kwargs):
    """More infos at:

    overview: https://docs.enthought.com/mayavi/mayavi/data.html
    writing: https://vtk.org/Wiki/VTK/Writing_VTK_files_using_python
    format: https://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf

    """
    _log.debug('Calling reader')
    try:
        from tvtk.api import tvtk
    except ImportError:
        _log.error('This extension recquires the tvtk package!')
        return
    if vector is None:
        vector = True
    # Setting up reader:
    reader = tvtk.DataSetReader(file_name=filename, read_all_scalars=True, read_all_vectors=vector)
    reader.update()
    # Getting output:
    output = reader.output
    assert output is not None, 'File reader could not find data or file "{}"!'.format(filename)
    # Reading points and vectors:
    if isinstance(output, tvtk.ImageData):  # tvtk.StructuredPoints is a subclass of tvtk.ImageData!
        # Connectivity: implicit; described by: 3D data array and spacing along each axis!
        _log.info('geometry: ImageData')
        # Load relevant information from output (reverse to get typical Python order z,y,x):
        dim = output.dimensions[::-1]
        origin = output.origin[::-1]
        spacing = output.spacing[::-1]
        _log.info(f'dim: {dim}, origin: {origin}, spacing: {spacing}')
        assert len(dim) == 3, 'Data has to be three-dimensional!'
        if scale is None:
            scale = tuple(spacing)
        if vector:  # Extract vector compontents and create magnitude array:
            vector_array = np.asarray(output.point_data.vectors, dtype=np.float)
            x_mag, y_mag, z_mag = vector_array.T
            data = np.stack((x_mag.reshape(dim), y_mag.reshape(dim), z_mag.reshape(dim)), axis=-1)
        else:  # Extract scalar data and create magnitude array:
            scalar_array = np.asarray(output.point_data.scalars, dtype=np.float)
            data = scalar_array.reshape(dim)
    elif isinstance(output, tvtk.RectilinearGrid):
        # Connectivity: implicit; described by: 3D data array and 1D array of spacing for each axis!
        _log.info('geometry: RectilinearGrid')
        raise NotImplementedError('RectilinearGrid is currently not supported!')
    elif isinstance(output, tvtk.StructuredGrid):
        # Connectivity: implicit; described by: 3D data array and 3D position arrays for each axis!
        _log.info('geometry: StructuredGrid')
        raise NotImplementedError('StructuredGrid is currently not supported!')
    elif isinstance(output, tvtk.PolyData):
        # Connectivity: explicit; described by: x, y, z positions of vertices and arrays of surface cells!
        _log.info('geometry: PolyData')
        raise NotImplementedError('PolyData is currently not supported!')
    elif isinstance(output, tvtk.UnstructuredGrid):
        # Connectivity: explicit; described by: x, y, z positions of vertices and arrays of volume cells!
        _log.info('geometry: UnstructuredGrid')
        # Load relevant information from output:
        point_array = np.asarray(output.points, dtype=np.float)
        if vector:
            data_array = np.asarray(output.point_data.vectors, dtype=np.float)
        else:
            data_array = np.asarray(output.point_data.scalars, dtype=np.float)
        if scale is None:
            raise ValueError('For the interpolation of unstructured grids, the `scale` parameter is required!')
        elif isinstance(scale, Number):  # Scale is the same for each dimension x, y, z!
            scale = (scale,) * 3
        elif isinstance(scale, tuple):
            assert len(scale) == 3, f'Each dimension (z, y, x) needs a scale, but {scale} was given!'
        data = interp_to_regular_grid(point_array, data_array, scale, **kwargs)
    else:
        raise TypeError('Data type of {} not understood!'.format(output))
    return Field(data, scale, vector=True)


def writer(filename, field, **kwargs):
    _log.debug('Call writer')
    assert len(field.dim) == 3, 'Currently only 3D fields can be saved to vtk!'
    try:
        from tvtk.api import tvtk, write_data
    except ImportError:
        _log.error('This extension recquires the tvtk package!')
        return
    # Create dataset:
    origin = (0, 0, 0)
    spacing = (field.scale[2], field.scale[1], field.scale[0])
    dimensions = (field.dim[2], field.dim[1], field.dim[0])
    sp = tvtk.StructuredPoints(origin=origin, spacing=spacing, dimensions=dimensions)
    # Fill with data from field:
    if field.vector:  # Handle vector fields:
        # Put vector components in corresponding array:
        vectors = field.data.reshape(-1, 3)
        sp.point_data.vectors = vectors
        sp.point_data.vectors.name = 'vectors'
        # Calculate colors:
        x_mag, y_mag, z_mag = field.comp
        magvec = np.asarray((x_mag.data.ravel(), y_mag.data.ravel(), z_mag.data.ravel()))
        cmap = kwargs.pop('cmap', None)
        if cmap is None:
            cmap = colors.cmaps.cyclic_cubehelix
        rgb = cmap.rgb_from_vector(magvec)
        point_colors = tvtk.UnsignedIntArray()
        point_colors.number_of_components = 3
        point_colors.name = 'colors'
        point_colors.from_array(rgb)
        sp.point_data.scalars = point_colors
        sp.point_data.scalars.name = 'colors'
    else:  # Handle scalar fields:
        scalars = field.data.ravel()
        sp.point_data.scalars = scalars
        sp.point_data.scalars.name = 'scalars'
    # Write the data to file:
    write_data(sp, filename)
