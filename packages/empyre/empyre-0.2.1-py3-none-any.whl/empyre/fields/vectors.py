# -*- coding: utf-8 -*-
# Copyright 2016 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#


import logging
from numbers import Number

import numpy as np

from .field import Field


__all__ = ['create_vector_homog', 'create_vector_vortex', 'create_vector_skyrmion', 'create_vector_singularity']

_log = logging.getLogger(__name__)


def create_vector_homog(dim, phi=0, theta=None, scale=1.0):
    """Field subclass implementing a homogeneous vector field with 3 components in 2 or 3 dimensions.

    Attributes
    ----------
    dim : tuple
        The dimensions of the grid.
    phi : float
        The azimuthal angle. The default is 0, i.e., the vectors point in x direction.
    theta : float, optional
        The polar angle. If None (default), only two components will be created (corresponds to pi/2 in 3D, i.e., the
        vectors are in the xy plane).
    scale: tuple of float
        Scaling along the dimensions of the underlying data.

    """
    _log.debug('Calling __init__')
    assert len(dim) in (2, 3), 'Disc can only be build in 2 or 3 dimensions!'
    assert isinstance(phi, Number), 'phi has to be an angle in radians!'
    assert isinstance(theta, Number) or theta is None, 'theta has to be an angle in radians or None!'
    if len(dim) == 2 and theta is None:  # 2D and 3rd component not explicitely wanted:
        y_comp = np.ones(dim) * np.sin(phi)
        x_comp = np.ones(dim) * np.cos(phi)
        data = np.stack([x_comp, y_comp], axis=-1)
    else:  # 3D, always have a third component:
        if theta is None:
            theta = np.pi/2  # xy-plane if not specified otherwise!
        z_comp = np.ones(dim) * np.cos(theta)
        y_comp = np.ones(dim) * np.sin(theta) * np.sin(phi)
        x_comp = np.ones(dim) * np.sin(theta) * np.cos(phi)
        data = np.stack([x_comp, y_comp, z_comp], axis=-1)
    return Field(data=data, scale=scale, vector=True)


def create_vector_vortex(dim, center=None, phi_0=np.pi/2, oop_r=None, oop_sign=1, core_r=0, axis=0, scale=1.0):
    """Field subclass implementing a vortex vector field with 3 components in 2 or 3 dimensions.

    Attributes
    ----------
    dim : tuple
        The dimensions of the grid.
    center : tuple (N=2 or N=3), optional
        The vortex center, given in 2D `(v, u)` or 3D `(z, y, x)`, where the perpendicular axis is discarded
        (determined by the `axis` parameter). Is set to the center of the field of view if not specified.
        The vortex center should be between two pixels to avoid singularities.
    axis :  int, optional
        The orientation of the vortex axis. The default is 0 and corresponds to the z-axis. Is ignored if dim is
        only 2D.
    phi_0 : float, optional
        Angular offset that allows all arrows to be rotated simultaneously. The default value is `pi/2` and corresponds
        to an anti-clockwise rotation, while a value of `-pi/2` corresponds to a clockwise rotation. `0` and `pi` lead
        to arrows that all point in/outward.
    oop_r : float, optional
        Radius of a potential out-of-plane ("oop") component in the vortex center. If `None`, the vortex is purely
        in-plane, which is the default. Set this to a number (in pixels) that determines the the radius in which the
        oop-component is tilted into the plane. A `0` leads to an immediate/sharp tilt (not visible without setting a
        core radius, see `core_r`), while setting this to the radius of your vortex disc, will let it tilt smoothly
        until reaching the edge.
    oop_sign : {1, -1}, optional
        Only used if `oop_r` is not None (i.e. there is an out-of-plane component). Can be `1` (default) or `-1` and
        determines if the core (if it exists) is aligned parallel (`+1`) or antiparallel (`-1`) to the chosen symmetry
        axis.
    core_r : float, optional
        Radius of a potential vortex core that's homogeneously oriented out-of-plane. Is not used when `oop_r` is not
        set and defaults to `0`, which means the vortex core is infinitely sharp.
    scale: tuple of float
        Scaling along the dimensions of the underlying data.

    Returns
    -------
    field : `~.Field` object
        The resulting vector field.

    """
    _log.debug('Calling create_vector_vortex')
    assert len(dim) in (2, 3), 'Vortex can only be build in 2 or 3 dimensions!'
    # Find indices of the vortex plane axes:
    idx_uv = [0, 1, 2]
    if len(dim) == 3:  # 3D:
        idx_uv.remove(axis)
    else:  # 2D:
        idx_uv.remove(2)
    # 2D dimensions:
    dim_uv = tuple([dim[i] for i in idx_uv])
    # Find default values:
    if center is None:
        center = tuple([dim[i] / 2 for i in idx_uv])
    elif len(center) == 3:  # if a 3D-center is given, just take the relevant coordinates:
        center = list(center)
        del center[axis]
        center = tuple(center)
    # Create vortex plane (2D):
    coords_uv = np.indices(dim_uv) + 0.5  # 0.5 to get to pixel/voxel center!
    coords_uv = coords_uv - np.asarray(center, dtype=float)[:, None, None]  # Shift by center!
    phi = np.arctan2(coords_uv[0], coords_uv[1]) - phi_0
    rr = np.hypot(coords_uv[0], coords_uv[1])
    rr_clip = np.clip(rr - core_r, a_min=0, a_max=None)  # negative inside core_r (clipped to 0), positive outside!
    # Check if a core should be constructed (oop_r != 0):
    if oop_r is None:
        w_comp = np.zeros(dim_uv)
    else:
        assert oop_r >= 0, 'oop_r has to be a positive number!'
        assert oop_sign in (1, -1), 'Sign of the out-of-plane component has to be either +1 or -1!'
        w_comp = 1 - 2/np.pi * np.arcsin(np.tanh(np.pi*rr_clip/(oop_r+1E-30)))  # orthogonal: 1 inside, to 0 outside!
        w_comp *= oop_sign * w_comp
    v_comp = np.ones(dim_uv) * np.sin(phi) * np.sqrt(1 - np.abs(w_comp))
    u_comp = np.ones(dim_uv) * np.cos(phi) * np.sqrt(1 - np.abs(w_comp))
    if len(dim) == 3:  # Expand to 3D:
        w_comp = np.expand_dims(w_comp, axis=axis)
        v_comp = np.expand_dims(v_comp, axis=axis)
        u_comp = np.expand_dims(u_comp, axis=axis)
        reps = [1, 1, 1]  # repetitions for tiling
        reps[axis] = dim[axis]  # repeat along chosen axis
        w_comp = np.tile(w_comp, reps)
        v_comp = np.tile(v_comp, reps)
        u_comp = np.tile(u_comp, reps)
    if axis == 0:  # z-axis
        z_comp = w_comp
        y_comp = -v_comp
        x_comp = -u_comp
    elif axis == 1:  # y-axis
        z_comp = v_comp
        y_comp = w_comp
        x_comp = u_comp
    elif axis == 2:  # x-axis
        z_comp = -v_comp
        y_comp = -u_comp
        x_comp = w_comp
    else:
        raise ValueError(f'{axis} is not a valid argument for axis (has to be 0, 1 or 2)')
    data = np.stack([x_comp, y_comp, z_comp], axis=-1)
    return Field(data=data, scale=scale, vector=True)


def create_vector_skyrmion(dim, center=None, phi_0=0, core_sign=1, skyrm_d=None, wall_d=None, axis=0, scale=1.0):
    """Create a 3-dimensional magnetic Bloch or Neel type skyrmion distribution.

    Parameters
    ----------
    dim : tuple
        The dimensions of the grid.
    center : tuple (N=2 or N=3), optional
        The source center, given in 2D `(v, u)` or 3D `(z, y, x)`, where the perpendicular axis
        is discarded. Is set to the center of the field of view if not specified.
        The center has to be between two pixels.
    phi_0 : float, optional
        Angular offset switching between Neel type (0 [default] or pi) or Bloch type (+/- pi/2)
        skyrmions.
    core_sign : {1, -1}, optional
        Can be `1` (default) or `-1` and determines if the skyrmion core is aligned parallel (`+1`) or antiparallel
        (`-1`) to the chosen symmetry axis.
    skyrm_d : float, optional
        Diameter of the skyrmion. Defaults to half of the smaller dimension perpendicular to the
        skyrmion axis if not specified.
    wall_d : float, optional
        Diameter of the domain wall of the skyrmion. Defaults to `skyrm_d / 4` if not specified.
    axis :  int, optional
        The orientation of the vortex axis. The default is 0 and corresponds to the z-axis. Is ignored if dim is
        only 2D.
    scale: tuple of float
        Scaling along the dimensions of the underlying data.

    Returns
    -------
    field : `~.Field` object
        The resulting vector field.

    Notes
    -----
        To avoid singularities, the source center should lie between the pixel centers (which
        reside at coordinates with _.5 at the end), i.e. integer values should be used as center
        coordinates (e.g. coordinate 1 lies between the first and the second pixel).

        Skyrmion wall width is dependant on exchange stiffness  A [J/m] and anisotropy K [J/m³]
        The out-of-plane magnetization at the domain wall is described in a paper by Romming et al
        (see DOI: 10.1103/PhysRevLett.114.177203s)

    """

    def _theta(r):
        theta_1 = + np.arcsin(np.tanh((r + skyrm_d/2)/(wall_d/2)))
        theta_2 = - np.arcsin(np.tanh((r - skyrm_d/2)/(wall_d/2)))
        theta = theta_1 + theta_2
        theta /= np.abs(theta).max() / np.pi
        return theta

    _log.debug('Calling create_vector_skyrmion')
    assert len(dim) in (2, 3), 'Skyrmion can only be build in 2 or 3 dimensions!'
    assert core_sign in (1, -1), 'Sign of the out-of-plane component has to be either +1 or -1!'
    # Find indices of the skyrmion plane axes:
    idx_uv = [0, 1, 2]
    if len(dim) == 3:  # 3D:
        idx_uv.remove(axis)
    else:  # 2D:
        idx_uv.remove(2)
    # 2D dimensions:
    dim_uv = tuple([dim[i] for i in idx_uv])
    # Find default values:
    if skyrm_d is None:
        skyrm_d = np.min(dim_uv) / 2
    if wall_d is None:
        wall_d = skyrm_d / 4
    if center is None:
        center = tuple([dim[i] / 2 for i in idx_uv])
    elif len(center) == 3:  # if a 3D-center is given, just take the relevant coordinates:
        center = list(center)
        del center[axis]
        center = tuple(center)
    # Create skyrmion plane (2D):
    coords_uv = np.indices(dim_uv) + 0.5  # 0.5 to get to pixel/voxel center!
    coords_uv = coords_uv - np.asarray(center, dtype=float)[:, None, None]  # Shift by center!
    rr = np.hypot(coords_uv[0], coords_uv[1])
    phi = np.arctan2(coords_uv[0], coords_uv[1]) - phi_0
    theta = _theta(rr)
    w_comp = core_sign * np.cos(theta)
    v_comp = np.sin(theta) * np.sin(phi)
    u_comp = np.sin(theta) * np.cos(phi)
    # Expansion to 3D if necessary and component shuffling:
    if len(dim) == 3:  # Expand to 3D:
        w_comp = np.expand_dims(w_comp, axis=axis)
        v_comp = np.expand_dims(v_comp, axis=axis)
        u_comp = np.expand_dims(u_comp, axis=axis)
        reps = [1, 1, 1]  # repetitions for tiling
        reps[axis] = dim[axis]  # repeat along chosen axis
        w_comp = np.tile(w_comp, reps)
        v_comp = np.tile(v_comp, reps)
        u_comp = np.tile(u_comp, reps)
    if axis == 0:  # z-axis
        z_comp = w_comp
        y_comp = -v_comp
        x_comp = -u_comp
    elif axis == 1:  # y-axis
        z_comp = v_comp
        y_comp = w_comp
        x_comp = u_comp
    elif axis == 2:  # x-axis
        z_comp = -v_comp
        y_comp = -u_comp
        x_comp = w_comp
    else:
        raise ValueError(f'{axis} is not a valid argument for axis (has to be 0, 1 or 2)')
    data = np.stack([x_comp, y_comp, z_comp], axis=-1)
    return Field(data=data, scale=scale, vector=True)


def create_vector_singularity(dim, center=None, scale=1.0):
    """Create a 3-dimensional magnetic distribution of a homogeneous magnetized object.

    Parameters
    ----------
    dim : tuple
        The dimensions of the grid.
    center : tuple (N=2 or N=3), optional
        The source center, given in 2D `(v, u)` or 3D `(z, y, x)`, where the perpendicular axis
        is discarded. Is set to the center of the field of view if not specified.
        The source center has to be between two pixels.
    scale: tuple of float
        Scaling along the dimensions of the underlying data.

    Returns
    -------
    field : `~.Field` object
        The resulting vector field.

    Notes
    -----
        To avoid singularities, the source center should lie between the pixel centers (which
        reside at coordinates with _.5 at the end), i.e. integer values should be used as center
        coordinates (e.g. coordinate 1 lies between the first and the second pixel).

        Per default, all arrows point outwards, negate the resulting `Field` object with a minus after creation to let
        them point inwards.

    """
    _log.debug('Calling create_vector_singularity')
    # Find default values:
    if center is None:
        center = tuple([d / 2 for d in dim])
    assert len(dim) == len(center), f"Length of dim ({len(dim)}) and center ({len(center)}) don't match!"
    # Setup coordinates, shape is (c, z, y, x), if 3D, or (c, y, x), if 2D (c: components):
    coords = np.indices(dim) + 0.5  # 0.5 to get to pixel/voxel center!
    bc_shape = (len(dim,),) + (1,)*len(dim)  # Shape for broadcasting, (3,1,1,1) for 3D, (2,1,1) for 2D!
    coords = coords - np.reshape(center, bc_shape)  # Shift by center (append 1s for broadcasting)!
    rr = np.sqrt(np.sum([coords[i]**2 for i in range(len(dim))], axis=0))
    coords /= rr + 1E-30  # Normalise amplitude (keep direction), rr (z,y,x) is broadcasted to data (c,z,y,x)!
    # coords has components listed in wrong order (z, y, x) in the first dimension, we need (x, y, z) in the last:
    coords = np.flip(coords, axis=0)
    # Finally, the data has the coordinate axis at the end, not at the front:
    data = np.moveaxis(coords, 0, -1)  # (c,z,y,x) -> (z,y,x,c)
    return Field(data=data, scale=scale, vector=True)
