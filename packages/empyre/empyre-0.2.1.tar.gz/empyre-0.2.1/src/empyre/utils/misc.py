# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""This module provides the miscellaneous helper functions."""


import logging
import itertools
from time import time

import numpy as np
from tqdm import tqdm
from scipy.spatial import cKDTree, qhull
from scipy.interpolate import LinearNDInterpolator


__all__ = ['levi_civita', 'interp_to_regular_grid']
_log = logging.getLogger(__name__)


def levi_civita(i, j, k):
    _log.debug('Calling levi_civita')
    return (j-i) * (k-i) * (k-j) / (np.abs(j-i) * np.abs(k-i) * np.abs(k-j))


def interp_to_regular_grid(points, values, scale, scale_factor=1, step=1, convex=True, distance_upper_bound=None):
    """Interpolate values on points to regular grid.

    Parameters
    ----------
    points : np.ndarray, (N, 3)
        Array of points, describing the location of the values that should be interpolated. Three columns x, y, z!
    values : np.ndarray, (N, c)
        Array of values that should be interpolated to the new grid. `c` is the number of components (`1` for scalar
        fields, `3` for normal 3D vector fields).
    scale : tuple of 3 ints
        Scale along each of the 3 spatial dimensions. Usually given in nm.
    scale_factor : float, optional
        Additional scaling factor that should be used if the original points are not described on a nm-scale. Use this
        to convert from nm of `scale` to the unit of the points. By default 1.
    step : int, optional
        If this is bigger than 1 (the default), only every `step` point is taken into account. Can speed up calculation,
        but you'll lose accuracy of your interpolation.
    convex : bool, optional
        By default True. If this is set to False, additional measures are taken to find holes in the point cloud.
        WARNING: this is an experimental feature that should be used with caution!
    distance_upper_bound: float, optional
        Only used if `convex=False`. Set the upper bound, determining if a point of the new (interpolated) grid is too
        far away from any original point. They are assumed to be in a "hole" and their values are set to zero. Set this
        value in nm, it will be converted to the local unit of the original points internally. If not set and
        `convex=True`, double of the the mean of `scale` is calculated and used (can be troublesome if the scales vary
        drastically).

    Returns
    -------
    interpolation: np.ndarray
        Interpolated grid with shape `(zdim, ydim, xdim)` for scalar and `(zdim, ydim, xdim, ncomp)` for vector field.

    """
    _log.debug('Calling interpolate_to_regular_grid')
    z_uniq = np.unique(points[:, 2])
    _log.info(f'unique positions along z: {len(z_uniq)}')
    #  Translate scale in local units (not necessarily nm), taken care of with `scale_factor`:
    scale = tuple([s * scale_factor for s in scale])
    # Determine the size of the point cloud of irregular coordinates:
    x_min, x_max = points[:, 0].min(), points[:, 0].max()
    y_min, y_max = points[:, 1].min(), points[:, 1].max()
    z_min, z_max = points[:, 2].min(), points[:, 2].max()
    x_diff, y_diff, z_diff = np.ptp(points[:, 0]), np.ptp(points[:, 1]), np.ptp(points[:, 2])
    _log.info(f'x-range: {x_min:.2g} <-> {x_max:.2g} ({x_diff:.2g})')
    _log.info(f'y-range: {y_min:.2g} <-> {y_max:.2g} ({y_diff:.2g})')
    _log.info(f'z-range: {z_min:.2g} <-> {z_max:.2g} ({z_diff:.2g})')
    # Determine dimensions from given grid spacing a:
    dim = tuple(np.round(np.asarray((z_diff/scale[0], y_diff/scale[1], x_diff/scale[2]), dtype=int)))
    assert all(dim) > 0, f'All dimensions of dim={dim} need to be > 0, please adjust the scale accordingly!'
    z = z_min + scale[0] * (np.arange(dim[0]) + 0.5)  # +0.5: shift to pixel center!
    y = y_min + scale[1] * (np.arange(dim[1]) + 0.5)  # +0.5: shift to pixel center!
    x = x_min + scale[2] * (np.arange(dim[2]) + 0.5)  # +0.5: shift to pixel center!
    # Create points for new Euclidian grid; fliplr for (x, y, z) order:
    points_euc = np.fliplr(np.asarray(list(itertools.product(z, y, x))))
    # Make values 2D (if not already); double .T so that a new axis is added at the END (n, 1):
    values = np.atleast_2d(values.T).T
    # Prepare interpolated grid:
    interpolation = np.empty(dim+(values.shape[-1],), dtype=np.float)
    _log.info(f'Dimensions of new grid: {interpolation.shape}')
    # Calculate the Delaunay triangulation (same for every component of multidim./vector fields):
    _log.info('Start Delaunay triangulation...')
    tick = time()
    triangulation = qhull.Delaunay(points[::step])
    tock = time()
    _log.info(f'Delaunay triangulation complete (took {tock-tick:.2f} s)!')
    # Perform the interpolation for each column of `values`:
    for i in tqdm(range(values.shape[-1])):
        # Create interpolator for the given triangulation and the values of the current column:
        interpolator = LinearNDInterpolator(triangulation, values[::step, i], fill_value=0)
        # Interpolate:
        interpolation[..., i] = interpolator(points_euc).reshape(dim)
    # If NOT convex, we have to check for additional holes in the structure (EXPERIMENTAL):
    if not convex:  # Only necessary if the user expects holes in the (-> nonconvex) distribution:
        # Create k-dimensional tree for queries:
        _log.info('Create cKDTree...')
        tick = time()
        tree = cKDTree(points)
        tock = time()
        _log.info(f'cKDTree creation complete (took {tock-tick:.2f} s)!')
        # Query the tree for nearest neighbors, x: points to query, k: number of neighbors, p: norm
        # to use (here: 2 - Euclidean), distance_upper_bound: maximum distance that is searched!
        if distance_upper_bound is None:  # Take the mean of the scale for the upper bound:
            distance_upper_bound = 2 * np.mean(scale)  # NOTE: could be problematic for wildly varying scale numbers.
        else:  # Convert to local scale:
            distance_upper_bound *= scale_factor
        _log.info('Start cKDTree neighbour query...')
        tick = time()
        data, leafsize = tree.query(x=points_euc, k=1, p=2, distance_upper_bound=distance_upper_bound)
        tock = time()
        _log.info(f'cKDTree neighbour query complete (took {tock-tick:.2f} s)!')
        # Create boolean mask that determines which interpolation points have no neighbor near enough:
        mask = np.isinf(data).reshape(dim)  # Points further away than upper bound were marked 'inf'!
        _log.info(f'{np.sum(mask)} of {points_euc.shape[0]} points were assumed to be in holes of the point cloud!')
        # Set these points to zero (NOTE: This can take a looooong time):
        interpolation[mask, :] = 0
    return np.squeeze(interpolation)
