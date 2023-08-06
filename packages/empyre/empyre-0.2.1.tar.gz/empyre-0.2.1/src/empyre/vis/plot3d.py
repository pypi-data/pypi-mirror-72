# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""This module provides functions for 3D plots based on the `mayavi` library."""


import logging

import numpy as np

from . import colors


__all__ = ['contour3d', 'mask3d', 'quiver3d']

_log = logging.getLogger(__name__)


# TODO: Docstrings and signature!

def contour3d(field, title='Field Distribution', contours=10, opacity=0.25, size=None, new_fig=True, **kwargs):
    """Plot a field as a 3D-contour plot.

    Parameters
    ----------
    title: string, optional
        The title for the plot.
    contours: int, optional
        Number of contours which should be plotted.
    opacity: float, optional
        Defines the opacity of the contours. Default is 0.25.

    Returns
    -------
    plot : :class:`mayavi.modules.vectors.Vectors`
        The plot object.

    """
    _log.debug('Calling contour3d')
    try:
        from mayavi import mlab
    except ImportError:
        _log.error('This extension recquires the mayavi package!')
        return
    if size is None:
        size = (750, 700)
    if new_fig:
        mlab.figure(size=size, bgcolor=(0.5, 0.5, 0.5), fgcolor=(0., 0., 0.))
    zzz, yyy, xxx = np.indices(field.dim) + np.reshape(field.scale, (3, 1, 1, 1)) / 2  # shifted by half of scale!
    zzz, yyy, xxx = zzz.T, yyy.T, xxx.T  # Transpose because of VTK order!
    field_amp = field.amp.data.T  # Transpose because of VTK order!
    if not isinstance(contours, (list, tuple, np.ndarray)):  # Calculate the contours:
        contours = list(np.linspace(field_amp.min(), field_amp.max(), contours))
    extent = np.ravel(list(zip((0, 0, 0), field_amp.shape)))
    cont = mlab.contour3d(xxx, yyy, zzz, field_amp, contours=contours, opacity=opacity, **kwargs)
    mlab.outline(cont, extent=extent)
    mlab.axes(cont, extent=extent)
    mlab.title(title, height=0.95, size=0.35)
    mlab.orientation_axes()
    cont.scene.isometric_view()
    return cont


def mask3d(field, title='Mask', threshold=0, grid=True, labels=True,
           orientation=True, size=None, new_fig=True, **kwargs):
    """Plot the mask as a 3D-contour plot.

    Parameters
    ----------
    title: string, optional
        The title for the plot.
    threshold : float, optional
        A pixel only gets masked, if it lies above this threshold . The default is 0.

    Returns
    -------
    plot : :class:`mayavi.modules.vectors.Vectors`
        The plot object.

    """
    _log.debug('Calling mask3d')
    try:
        from mayavi import mlab
    except ImportError:
        _log.error('This extension recquires the mayavi package!')
        return
    if size is None:
        size = (750, 700)
    if new_fig:
        mlab.figure(size=size, bgcolor=(0.5, 0.5, 0.5), fgcolor=(0., 0., 0.))
    zzz, yyy, xxx = np.indices(field.dim) + np.reshape(field.scale, (3, 1, 1, 1)) / 2  # shifted by half of scale!
    zzz, yyy, xxx = zzz.T, yyy.T, xxx.T  # Transpose because of VTK order!
    mask = field.mask.data.T.astype(int)  # Transpose because of VTK order!
    extent = np.ravel(list(zip((0, 0, 0), mask.shape)))
    cont = mlab.contour3d(xxx, yyy, zzz, mask, contours=[1], **kwargs)
    if grid:
        mlab.outline(cont, extent=extent)
    if labels:
        mlab.axes(cont, extent=extent)
        mlab.title(title, height=0.95, size=0.35)
    if orientation:
        oa = mlab.orientation_axes()
        oa.marker.set_viewport(0, 0, 0.4, 0.4)
        mlab.draw()
    engine = mlab.get_engine()
    scene = engine.scenes[0]
    scene.scene.isometric_view()
    return cont


def quiver3d(field, title='Vector Field', limit=None, cmap=None, mode='2darrow',
             coloring='angle', ar_dens=1, opacity=1.0, grid=True, labels=True,
             orientation=True, size=(700, 750), new_fig=True, view='isometric',
             position=None, bgcolor=(0.5, 0.5, 0.5)):
    """Plot the vector field as 3D-vectors in a quiverplot.

    Parameters
    ----------
    title : string, optional
        The title for the plot.
    limit : float, optional
        Plotlimit for the vector field arrow length used to scale the colormap.
    cmap : string, optional
        String describing the colormap which is used for color encoding (uses `~.colors.cmaps.cyclic_cubehelix` if
        left on the `None` default) or amplitude encoding (uses 'jet' if left on the `None` default).
    ar_dens: int, optional
        Number defining the arrow density which is plotted. A higher ar_dens number skips more
        arrows (a number of 2 plots every second arrow). Default is 1.
    mode: string, optional
        Mode, determining the glyphs used in the 3D plot. Default is '2darrow', which
        corresponds to 2D arrows. For smaller amounts of arrows, 'arrow' (3D) is prettier.
    coloring : {'angle', 'amplitude'}, optional
        Color coding mode of the arrows. Use 'angle' (default) or 'amplitude'.
    opacity: float, optional
        Defines the opacity of the arrows. Default is 1.0 (completely opaque).

    Returns
    -------
    plot : :class:`mayavi.modules.vectors.Vectors`
        The plot object.

    """
    _log.debug('Calling quiver_plot3D')
    try:
        from mayavi import mlab
    except ImportError:
        _log.error('This extension recquires the mayavi package!')
        return
    if limit is None:
        limit = np.max(np.nan_to_num(field.amp))
    ad = ar_dens
    # Create points and vector components as lists:
    zzz, yyy, xxx = (np.indices(field.dim) + 1 / 2)
    zzz = zzz[::ad, ::ad, ::ad].ravel()
    yyy = yyy[::ad, ::ad, ::ad].ravel()
    xxx = xxx[::ad, ::ad, ::ad].ravel()
    x_mag = field.data[::ad, ::ad, ::ad, 0].ravel()
    y_mag = field.data[::ad, ::ad, ::ad, 1].ravel()
    z_mag = field.data[::ad, ::ad, ::ad, 2].ravel()
    # Plot them as vectors:
    if new_fig:
        mlab.figure(size=size, bgcolor=(0.5, 0.5, 0.5), fgcolor=(0., 0., 0.))
    if coloring == 'angle':  # Encodes the full angle via colorwheel and saturation:
        _log.debug('Encoding full 3D angles')
        vecs = mlab.quiver3d(xxx, yyy, zzz, x_mag, y_mag, z_mag, mode=mode, opacity=opacity,
                             scalars=np.arange(len(xxx)), line_width=2)
        vector = np.asarray((x_mag.ravel(), y_mag.ravel(), z_mag.ravel()))
        if cmap is None:
            cmap = colors.cmaps.cyclic_cubehelix
        rgb = cmap.rgb_from_vector(vector)
        rgba = np.hstack((rgb, 255 * np.ones((len(xxx), 1), dtype=np.uint8)))
        vecs.glyph.color_mode = 'color_by_scalar'
        vecs.module_manager.scalar_lut_manager.lut.table = rgba
        mlab.draw()
    elif coloring == 'amplitude':  # Encodes the amplitude of the arrows with the jet colormap:
        _log.debug('Encoding amplitude')
        if cmap is None:
            cmap = 'jet'
        vecs = mlab.quiver3d(xxx, yyy, zzz, x_mag, y_mag, z_mag,
                             mode=mode, colormap=cmap, opacity=opacity, line_width=2)
        mlab.colorbar(label_fmt='%.2f')
        mlab.colorbar(orientation='vertical')
    else:
        raise AttributeError('Coloring mode not supported!')
    vecs.glyph.glyph_source.glyph_position = 'center'
    vecs.module_manager.vector_lut_manager.data_range = np.array([0, limit])
    extent = np.ravel(list(zip((0, 0, 0), (field.dim[2], field.dim[1], field.dim[0]))))
    if grid:
        mlab.outline(vecs, extent=extent)
    if labels:
        mlab.axes(vecs, extent=extent)
        mlab.title(title, height=0.95, size=0.35)
    if orientation:
        oa = mlab.orientation_axes()
        oa.marker.set_viewport(0, 0, 0.4, 0.4)
        mlab.draw()
    engine = mlab.get_engine()
    scene = engine.scenes[0]
    if view == 'isometric':
        scene.scene.isometric_view()
    elif view == 'x_plus_view':
        scene.scene.x_plus_view()
    elif view == 'y_plus_view':
        scene.scene.y_plus_view()
    if position:
        scene.scene.camera.position = position
    return vecs
