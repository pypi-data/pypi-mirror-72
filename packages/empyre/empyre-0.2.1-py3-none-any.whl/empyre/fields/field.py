# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""This module provides a container class for multidimensional scalar or vector fields."""


import logging
from numbers import Number
from numpy.lib.mixins import NDArrayOperatorsMixin

import numpy as np
from numpy.core import numeric
from scipy.ndimage import interpolation

from ..utils import Quaternion


__all__ = ['Field']


class Field(NDArrayOperatorsMixin):
    """Container class for storing multidimensional scalar or vector fields.

    The `Field` class is a sophisticated wrapper around a multidimensional numpy array. The user can access the
    underlying data via the `data` attribute, or by using the `numpy.asarray` function.

    `Field` defines the `ufunc` interface for numpys vast library of universal functions. This includes all operator
    definitions, i.e., you can add, subtract, multiply and devide `Field` objects element-wise. Note that for vector
    fields, `Field` will handle all vector components separately and for ufuncs with two inputs, the other object will
    be broadcast accordingly. It is therefore also possible to add (or multiply) vector and scalar fields, assuming
    their dimensions `dim` match (their `shape` can't match, because it includes the number of components `ncomp` for
    the vector field). For ufuncs that reduce the output shape (e.g. `numpy.sum`), if the `axis` parameter is set to
    `None` (default), component axes for vector fields are kept (they can however explicitely reduced by including
    them in the `axis` paremeter, e.g. by setting `axis = -1`).

    `Field` objects can be indexed like numpy arrays and scalar fields (`vector=False`) behave as expected. A vector
    field (`vector=True`) can be indexed by only the non-component indices (see `dim`) and the according components of
    the specified point are returned as a tuple. Slicing with integers will return a `Field` object with reduced
    dimensionality (or a scalar/tuple if all spatial dimensions are reduced) that also drops the associated `scales`
    as needed. New axes (indexing with `None` or `numpy.newaxis`) is disabled because that would mean that an unknown
    scale would need to be added (you can always create a new `Field` object with an appropriately prepared ndarray).

    Some callables exposed by numpy's public API (e.g. `numpy.mean(...)`) will treat `Field` objects as if they
    were identical to their underlying numpy array (by envoking the `__array__` function which just returns `data`).
    The result often is a simple `numpy.ndarray` and not a `Field` object. Some functions (e.g. `clip`) are also defined
    on `Field` as methods. They might behave differently and will return `Field` objects instead, so take care and
    refer to their docstrings for further information!
    # TODO: Too verbose? In documentation instead?

    Attributes
    ----------
    data: np.ndarray
        The underlying data array of the field.
    scale: tuple of float
        Scaling along the dimensions of the underlying data.
    vector: bool
        True if the field is a vector field, False if it is a scalar field.
    shape: tuple of ints
        Shape of the underlying data. Includes the number of components as the first dimension if the field is a
        vector field.
    dim: tuple of ints
        Dimensions of the underlying data. Only includes spatial dimensions, NOT the number of vector components!
        (Use `ncomp` to get the number of components, if any, `shape` for the full shape of the underlying array).
    ncomp: None or tuple of ints
        Number of components if the field is a vector field (can be 2 or 3), None if it is a scalar field. The component
        axis is always the last axis (index `-1`) of the underlying data array!

    Notes
    -----
    See https://docs.scipy.org/doc/numpy/reference/arrays.classes.html for information about ndarray subclassing!
    See https://docs.scipy.org/doc/numpy-1.13.0/neps/ufunc-overrides.html for information about __array_ufunc__!
    See https://numpy.org/neps/nep-0018-array-function-protocol.html for information about __array_function__!
    """

    _log = logging.getLogger(__name__ + '.Field')

    @property
    def data(self):
        return self.__data

    @property
    def vector(self):
        return self.__vector

    @vector.setter
    def vector(self, vector):
        assert isinstance(vector, bool), 'vector has to be a boolean!'
        self.__vector = vector

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, scale):
        if isinstance(scale, Number):  # Scale is the same for each dimension!
            self.__scale = (float(scale),) * len(self.dim)
        elif isinstance(scale, tuple):
            ndim = len(self.dim)
            assert len(scale) == ndim, f'Each of the {ndim} dimensions needs a scale, but {scale} was given!'
            self.__scale = scale
        else:
            raise AssertionError(f'Scaling has to be a number or a tuple of numbers, was {scale} instead!')

    @property
    def shape(self):
        return self.data.shape

    @property
    def dim(self):
        if self.vector:
            return self.shape[:-1]
        else:
            return self.shape

    @property
    def ncomp(self):
        return self.shape[-1] if self.vector else 0

    @property
    def comp(self):  # TODO: Function or property? Philosophical question?
        # Return empty list for scalars (ncomp is 0) and a list of components as scalar fields for a vector field:
        return [Field(self.data[..., i], self.scale, vector=False) for i in range(self.ncomp)]

    @property
    def amp(self):  # TODO: Function or property? Philosophical question?
        if self.vector:
            amp = np.sqrt(np.sum([comp.data**2 for comp in self.comp], axis=0))
        else:
            amp = np.abs(self.data)
        return Field(amp, self.scale, vector=False)

    @property
    def mask(self):  # TODO: Function or property? Philosophical question?
        return Field(np.where(np.asarray(self.amp) > 0, True, False), self.scale, vector=False)

    def __init__(self, data, scale=1.0, vector=False):
        self._log.debug('Calling __init__')
        self.__data = data
        self.vector = vector  # Set vector before scale, because scale needs to know if vector (via calling dim)!
        self.scale = scale
        if self.vector:
            assert self.ncomp in (2, 3), 'Only 2- or 3-component vector fields are supported!'
        self._log.debug('Created ' + str(self))

    def __repr__(self):
        self._log.debug('Calling __repr__')
        data_string = str(self.data)  # String of JUST the data array, without metadata (compared to repr)!
        return f'{self.__class__.__name__}(data={data_string}, scale={self.scale}, vector={self.vector})'

    def __str__(self):
        self._log.debug('Calling __repr__')
        ncomp_string = f', ncomp={self.ncomp}' if self.vector else ''
        return f'{self.__class__.__name__}(dim={self.dim}, scale={self.scale}, vector={self.vector}{ncomp_string})'

    def __array__(self):
        self._log.debug('Calling __array__')
        return self.data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        self._log.debug('Calling __array_ufunc__')
        outputs = kwargs.pop('out', ())
        outputs = kwargs.pop('out', (None,)*ufunc.nout)  # Defaults to tuple of None (currently: nout=1 all the time)
        outputs_arr = tuple([np.asarray(out) if isinstance(out, Field) else out for out in outputs])
        # Cannot handle items that have __array_ufunc__ (other than our own).
        for item in inputs + outputs:
            if hasattr(item, '__array_ufunc__') and not isinstance(item, Field):  # Something else with __array_ufunc__:
                if type(item).__array_ufunc__ is not np.ndarray.__array_ufunc__:  # Can't handle other overrides:
                    return NotImplemented
        # TODO: BIGGEST NOTE HERE: Delegate work to ndarray.__array_ufunc__!
        # TODO: For this to work, we have to make sure that we dispatch input as ndarrays, NOT Fields!
        # Convert all Field inputs to simple ndarrays to avoid infinite recursion!
        # ndarray.__array_ufunc__ delegates to the called ufunc method ONLY if all inputs and outputs are ndarrays
        # (or have no __array_ufunc__ method, e.g. a scalar), so that's what we need to ensure here.:
        # inputs = tuple([inp.view(np.ndarray) if isinstance(inp, Field) else inp for inp in inputs])
        # TODO: possibly need to sort out which input (if two) is a Field (vector or scalar?), order matters?
        # TODO: DOCUMENT: most things are same as in ndarrays, but if only one input is a vector field, try broadcast!
        # TODO: for security, newaxis is not allowed (most other indexing works though), because scale would be unknown!
        # 1 input (has to be a Field, otherwise we wouldn't be here):
        if len(inputs) == 1:
            self._log.debug(f'__array_ufunc__ inputs: {len(inputs)}')
            field = inputs[0]
            scale_new = field.scale
            vector_new = field.vector
            # Preprocess axis keyword if it exists:
            axis = kwargs.get('axis', False)  # Default must not be None, because None is a possible setting!
            full_reduction = False
            if axis is not False:
                ax_full = tuple(range(len(field.dim)))  # All axes (minus a possible component axis for vector Fields)!
                ax_full_wc = tuple(range(len(field.dim) + 1))  # All axes WITH component axis (does not need to exist)!
                axis = ax_full if axis is None else axis  # This keeps possible components untouched if axis was None!
                axis = numeric.normalize_axis_tuple(axis, field.ndim)  # Takes care of pot. neg. indices, ensures tuple!
                kwargs['axis'] = axis  # Put normalized axis back into kwargs!
                if axis in (ax_full, ax_full_wc):  # Full reduction (or reduction to just components) takes place:
                    full_reduction = True
                if ax_full_wc[-1] in axis:  # User explicitely wants component reduction (can only be true for vector):
                    vector_new = False  # Force scalar field!
                scale_new = tuple([s for i, s in enumerate(field.scale) if i not in axis])  # Drop axis from scale!
            inputs_arr = np.asarray(field)  # Convert inputs that are Fields to ndarrays to avoid recursion!
            data_new = getattr(ufunc, method)(inputs_arr, out=outputs_arr, **kwargs)
            if full_reduction:  # Premature return because the result is no longer a Field:
                return data_new
        # More than 1 input (at least one has to be a Field, otherwise we wouldn't be here):
        elif len(inputs) > 1:
            is_field = [isinstance(inp, Field) for inp in inputs]
            is_vector = [getattr(inp, 'vector', False) for inp in inputs]
            # Determine scale:
            if np.sum(is_field) > 1:  # More than one input is a Field objects:
                scales = [inp.scale for i, inp in enumerate(inputs) if is_field[i]]  # Only takes scales of Field obj.!
                scale_new = scales[0]
                err_msg = f'Scales of all Field objects must match! Given scales: {scales}!'
                assert all(scale == scale_new for scale in scales), err_msg
            else:  # Only one input is a field, pick the scale of that one:
                scale_new = inputs[np.argmax(is_field)].scale  # argmax returns the index of first True!
            # Determine vector:
            vector_new = True if np.any(is_vector) else False  # Output is vector field if any input is a vector field!
            if np.sum(is_vector) > 1:  # More than one input is a vector Field objects:
                ncomps = [inp.ncomp for i, inp in enumerate(inputs) if is_vector[i]]  # Only takes ncomp of v.-Fields!
                err_msg = f'# of components of all Field objects must match! Given ncomps: {ncomps}!'
                assert all(ncomp == ncomps[0] for ncomp in ncomps), err_msg
            # Append new axis at the end of non vector objects to broadcast to components:
            if np.any(is_vector):
                inputs = list(inputs)
                for i, inp in enumerate(inputs):
                    if not is_vector[i] and not isinstance(inp, Number):  # Numbers work for broadcasting anyway:
                        if len(np.asarray(inp).shape) == len(scale_new):  # No. of dimensions w/o comp., have to match!
                            inputs[i] = np.asarray(inputs[i])[..., np.newaxis]  # Broadcasting, try to cast as ndarray!
                inputs = tuple(inputs)
            # Convert inputs that are Fields to ndarrays to avoid recursion and determine data_new:
            inputs_arr = tuple([np.asarray(inp) if isinstance(inp, Field) else inp for inp in inputs])
            data_new = getattr(ufunc, method)(*inputs_arr, out=outputs_arr, **kwargs)
        # Return results:
        result = Field(data_new, scale_new, vector_new)
        return result

    def __getitem__(self, index):
        self._log.debug('Calling __getitem__')
        # Pre-processing index:
        index = index if isinstance(index, tuple) else (index,)  # Make sure item is a tuple!
        if None in index:
            raise Exception('Field does not support indexing with newaxis/None! Please cast as ndarray first!')
        if len(index) < len(self.shape) and Ellipsis not in index:  # Ellipsis is IMPLICIT at the end if index < dim:
            index += (Ellipsis,)
        if Ellipsis in index:  # Expand Ellipsis (...) into slice(None) (:) to make iterating consistent:
            index = list(index)
            i = index.index(Ellipsis)
            missing_dims = len(self.shape) - len(index)  # Number of non-specified dimensions
            index[i:i+1] = [slice(None)] * (missing_dims + 1)  # +1 because at least Ellipsis is replaced!
            index = tuple(index)
        # Indexing with a scalar drops the dimension, indexing with slice always keeps the dimension:
        index_scale = index[:-1] if self.vector else index  # Disregard last index for vector fields (has no scale)!
        scale_new = ()
        for i, item in enumerate(index_scale):
            if isinstance(item, slice):  # Indexing with slice keeps the dimension and therefore the scale:
                scale_new += (self.scale[i],)
        # Get data with classic indexing from underlying data array:
        data_new = self.data[index]
        # Determine vector state of output:
        vector_new = self.vector
        if self.vector and isinstance(index[-1], Number):  # For vector fields if last index (component) is dropped:
            vector_new = False
        # Return:
        if not scale_new:  # scale_new=(), i.e. full reduction of all dimensions (not regarding possible vector comp.):
            if isinstance(data_new, Number):  # full reduction:
                return data_new
            else:  # Only important for vector fields:
                return tuple(data_new)  # return single vector as tuple
        else:  # Return Field object
            return Field(data_new, scale_new, vector=vector_new)

    @classmethod
    def from_scalar_fields(cls, scalar_list):
        """Create a vector `Field` object from a list of scalar `Fields`.

        Parameters
        ----------
        scalar_list : list
            List of scalar `Field` objects (`vector=False`).

        Returns
        -------
        vector_field: `Field`
            A vector `Field` object containing the input scalar fields as components.

        """
        cls._log.debug('Calling from_scalar_fields')
        assert len(scalar_list) in (2, 3), 'Needs two or three scalar fields as components for vector field!'
        assert all(isinstance(item, Field) for item in scalar_list), 'All items have to be Field objects!'
        assert all(not item.vector for item in scalar_list), 'All items have to be scalar fields!'
        assert all(item.scale == scalar_list[0].scale for item in scalar_list), 'Scales of fields must match!'
        return cls(np.stack(scalar_list, axis=-1), scalar_list[0].scale, vector=True)

    @classmethod
    def from_signal(cls, signal, scale=None, vector=None, comp_pos=-1):
        """Convert a :class:`~hyperspy.signals.Signal` object to a :class:`~.Field` object.

        Parameters
        ----------
        signal: :class:`~hyperspy.signals.Signal`
            The :class:`~hyperspy.signals.Signal` object which should be converted to Field.

        Returns
        -------
        field: :class:`~.Field`
            A :class:`~.Field` object containing the loaded data.
        scale: tuple of float, optional
            Scaling along the dimensions of the underlying data. If not provided, will be read from the axes_manager.
        vector: boolean, optional
            If set to True, forces the signal to be interpreted as a vector field. EMPyRe will check if the first axis
            is named 'vector components' (EMPyRe saves vector fields like this). If this is the case, vector will be
            automatically set to True and the signal will also be interpreted as a vector field.
        comp_pos: int, optoinal
            The index of the axis containing the vector components (if `vector=True`). EMPyRe needs this to be the last
            axis (index `-1`, which is the default). In case another position is given, the vector component will be
            moved to the last axis. Old Pyramid files will have this axis at index `0`, so use this for backwards
            compatibilty.

        Notes
        -----
        Signals recquire the hyperspy package!

        """
        cls._log.debug('Calling from_signal')
        data = signal.data
        if vector and comp_pos != -1:  # component axis should be last, but is currently first -> roll to the end:
            data = np.moveaxis(data, source=comp_pos, destination=-1)
        if vector is None:  # Automatic detection:
            vector = True if signal.axes_manager[0].name == 'vector components' else False
        if scale is None:  # If not provided, try to read from axes_manager, one less axis if vector!:
            scale = tuple([signal.axes_manager[i].scale for i in range(len(data.shape) - vector)])
        return cls(data, scale, vector)

    def to_signal(self):
        """Convert :class:`~.Field` data into a HyperSpy signal.

        Returns
        -------
        signal: :class:`~hyperspy.signals.Signal`
            Representation of the :class:`~.Field` object as a HyperSpy Signal.

        Notes
        -----
        This method recquires the hyperspy package!

        """
        self._log.debug('Calling to_signal')
        try:  # Try importing HyperSpy:
            import hyperspy.api as hs
        except ImportError:
            self._log.error('This method recquires the hyperspy package!')
            return
        # Create signal:
        signal = hs.signals.BaseSignal(self.data)  # All axes are signal axes!
        # Set axes:
        if self.vector:
            signal.axes_manager[0].name = 'vector components'
        for i in range(len(self.dim)):
            ax = i+1 if self.vector else i  # take component axis into account if vector!
            num = ['x', 'y', 'z'][i] if len(self.dim) <= 3 else i
            signal.axes_manager[ax].name = f'axis {num}'
            signal.axes_manager[ax].scale = self.scale[i]
            signal.axes_manager[ax].units = 'nm'
        signal.metadata.Signal.title = f"EMPyRe {'vector' if self.vector else 'scalar'} Field"
        return signal

    def copy(self):
        """Returns a copy of the :class:`~.Field` object.

        Returns
        -------
        field: :class:`~.Field`
            A copy of the :class:`~.Field`.

        """
        self._log.debug('Calling copy')
        return Field(self.data.copy(), self.scale, self.vector)

    def rotate(self, angle, axis='z', **kwargs):
        """Rotate the :class:`~.Field`, based on :function:`~scipy.ndimage.interpolation.rotate`.

        Rotation direction is from the first towards the second axis. Works for 2D and 3D Fields.

        Parameters
        ----------
        angle : float
            The rotation angle in degrees.
        axis: {'x', 'y', 'z'}, optional
            The axis around which the vector field is rotated. Default is 'z'. Ignored for 2D Fields.

        Returns
        -------
        field: :class:`~.Field`
            The rotated :class:`~.Field`.

        Notes
        -----
        All additional kwargs are passed through to :function:`~scipy.ndimage.interpolation.rotate`.
        The `reshape` parameter, controlling if the output shape is adapted so that the input array is contained
        completely in the output is False per default, contrary to :function:`~scipy.ndimage.interpolation.rotate`,
        where it is True.

        """
        self._log.debug('Calling rotate')
        assert len(self.dim) in (2, 3), 'rotate is currently  only defined for 2D and 3D Fields!'
        kwargs.setdefault('reshape', False)  # Default here is no reshaping!
        if len(self.dim) == 2:  # For 2D, there are only 2 axes:
            axis = 'z'  # Overwrite potential argument if 2D!
            axes = (0, 1)  # y and x
        else:  # 3D case:
            axes = {'x': (0, 1), 'y': (0, 2), 'z': (1, 2)}[axis]
        if axis == 'z':  # TODO: Somehow needed... don't know why, maybe because origin='lower' in imshow?
            angle *= -1
        sc_0, sc_1 = self.scale[axes[0]], self.scale[axes[1]]
        assert sc_0 == sc_1, f'rotate needs the scales in the rotation plane to be equal (they are {sc_0} & {sc_1})!'
        if not self.vector:  # Scalar field:
            data_new = interpolation.rotate(self.data, angle, axes=axes, **kwargs)
        else:  # Vector field:
            # Rotate coordinate system:
            comps = [np.asarray(comp) for comp in self.comp]
            if self.ncomp == 3:
                data_new = np.stack([interpolation.rotate(c, angle, axes=axes, **kwargs) for c in comps], axis=-1)
                # Up till now, only the coordinates are rotated, now we need to rotate the vectors inside the voxels:
                rot_axis = [i for i in (0, 1, 2) if i not in axes][0]  # [0] because list!
                i, j, k = axes[0], axes[1], rot_axis  # next line only works if i != j != k
                levi_civita = int((j-i) * (k-i) * (k-j) / (np.abs(j-i) * np.abs(k-i) * np.abs(k-j)))
                # Create Quaternion, note that they have (x, y, z) order instead of (z, y, x):
                # TODO: Again a minus sign needed before levi_civita, still not sure why (see angle above)!
                quat_axis = tuple([-levi_civita if i == rot_axis else 0 for i in (2, 1, 0)])
                quat = Quaternion.from_axisangle(quat_axis, np.deg2rad(angle))
                data_new = quat.matrix.dot(data_new.reshape((-1, 3)).T).T.reshape(self.shape)  # T needed b.c. ordering!
            elif self.ncomp == 2:
                u_comp, v_comp = comps
                u_rot = interpolation.rotate(u_comp, angle, axes=axes, **kwargs)
                v_rot = interpolation.rotate(v_comp, angle, axes=axes, **kwargs)
                # Up till now, only the coordinates are rotated, now we need to rotate the vectors inside the voxels:
                # TODO: Again a minus sign needed for vector rotation, still not sure why (see angle above)!
                ang_rad = np.deg2rad(-angle)
                u_mix = np.cos(ang_rad)*u_rot - np.sin(ang_rad)*v_rot
                v_mix = np.sin(ang_rad)*u_rot + np.cos(ang_rad)*v_rot
                data_new = np.stack((u_mix, v_mix), axis=-1)
            else:
                raise ValueError('rotate currently only works for 2- or 3-component vector fields!')
        return Field(data_new, self.scale, self.vector)

    def rot90(self, k=1, axis='z'):
        """Rotate the :class:`~.Field` 90° around the specified axis (right hand rotation).

        Parameters
        ----------
        k : integer
            Number of times the array is rotated by 90 degrees.
        axis: {'x', 'y', 'z'}, optional
            The axis around which the vector field is rotated. Default is 'z'. Ignored for 2D Fields.

        Returns
        -------
        field: :class:`~.Field`
            The rotated :class:`~.Field`.

        """
        self._log.debug('Calling rot90')
        assert axis in ('x', 'y', 'z'), "Wrong input! 'x', 'y', 'z' allowed!"
        assert len(self.dim) in (2, 3), 'rotate is currently  only defined for 2D and 3D Fields!'
        if len(self.dim) == 2:  # For 2D, there are only 2 axes:
            axis = 'z'  # Overwrite potential argument if 2D!
            axes = (0, 1)  # y and x
        else:  # 3D case:
            axes = {'x': (0, 1), 'y': (0, 2), 'z': (1, 2)}[axis]
        sc_0, sc_1 = self.scale[axes[0]], self.scale[axes[1]]
        assert sc_0 == sc_1, f'rot90 needs the scales in the rotation plane to be equal (they are {sc_0} & {sc_1})!'
        # TODO: Later on, rotation could also flip the scale (not implemented here, yet)!
        if not self.vector:  # Scalar Field:
            data_new = np.rot90(self.data, k=k, axes=axes)
        else:  # Vector Field:
            if len(self.dim) == 3:  # 3D:
                assert self.ncomp == 3, 'rot90 currently only works for vector fields with 3 components in 3D!'
                comp_x, comp_y, comp_z = self.comp
                if axis == 'x':  # RotMatrix for 90°: [[1, 0, 0], [0, 0, -1], [0, 1, 0]]
                    comp_x_rot = np.rot90(comp_x, k=k, axes=axes)
                    comp_y_rot = np.rot90(comp_z, k=k, axes=axes)
                    comp_z_rot = -np.rot90(comp_y, k=k, axes=axes)
                elif axis == 'y':  # RotMatrix for 90°: [[0, 0, 1], [0, 1, 0], [-1, 0, 0]]
                    comp_x_rot = np.rot90(comp_z, k=k, axes=axes)
                    comp_y_rot = np.rot90(comp_y, k=k, axes=axes)
                    comp_z_rot = -np.rot90(comp_x, k=k, axes=axes)
                elif axis == 'z':  # RotMatrix for 90°: [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
                    comp_x_rot = np.rot90(comp_y, k=k, axes=axes)
                    comp_y_rot = np.rot90(comp_x, k=k, axes=axes)
                    comp_z_rot = np.rot90(comp_z, k=k, axes=axes)
                data_new = np.stack((comp_x_rot, comp_y_rot, comp_z_rot), axis=-1)
            if len(self.dim) == 2:  # 2D:
                assert self.ncomp == 2, 'rot90 currently only works for vector fields with 2 components in 2D!'
                comp_x, comp_y = self.comp
                comp_x_rot = np.rot90(comp_y, k=k, axes=axes)
                comp_y_rot = np.rot90(comp_x, k=k, axes=axes)
                data_new = np.stack((comp_x_rot, comp_y_rot), axis=-1)
        # Return result:
        return Field(data_new, self.scale, self.vector)

    def get_vector(self, mask=None):
        """Returns the field as a vector, specified by a mask.

        Parameters
        ----------
        mask : :class:`~numpy.ndarray` (boolean)
            Masks the pixels from which the entries should be taken. Must be a numpy array for indexing to work!

        Returns
        -------
        vector : :class:`~numpy.ndarray` (N=1)
            The vector containing the field of the specified pixels. If the field is a vector field, components are
            first vectorised, then concatenated!

        """
        self._log.debug('Calling get_vector')
        if mask is None:  # If not given, take full data:
            mask = np.full(self.dim, True)
        if self.vector:  # Vector field:
            return np.ravel([comp.data[mask] for comp in self.comp])
        else:  # Scalar field:
            return np.ravel(self.data[mask])

    def set_vector(self, vector, mask=None):
        """Set the field of the masked pixels to the values specified by `vector`.

        Parameters
        ----------
        mask : :class:`~numpy.ndarray` (boolean), optional
            Masks the pixels from which the field should be taken.
        vector : :class:`~numpy.ndarray` (N=1)
            The vector containing the field of the specified pixels.

        Returns
        -------
        None

        """
        self._log.debug('Calling set_vector')
        if mask is None:  # If not given, set full data:
            mask = np.full(self.dim, True)
        if self.vector:  # Vector field:
            assert np.size(vector) % self.ncomp == 0, 'Vector has to contain all components for every pixel!'
            count = np.size(vector) // self.ncomp
            for i in range(self.ncomp):
                sl = slice(i*count, (i+1)*count)
                self.data[..., i][mask] = vector[sl]
        else:  # Scalar field:
            self.data[mask] = vector

    def squeeze(self):
        """Squeeze the `Field` object to remove single-dimensional entries in the shape.

        Returns
        -------
        field: `Field`
            Squeezed `Field` object. Note that scales associated with squeezed dimensions are also dropped.

        Notes
        -----
        Also works via `numpy.squeeze(field)`, because `numpy.squeeze` searches for a local implementation first and
        then uses `_wrapit` to envoke this function here!

        """
        self._log.debug('Calling squeeze')
        squeezed_indices = np.flatnonzero(np.asarray(self.dim) == 1)
        squeezed_data = np.squeeze(self.data)
        if squeezed_indices:
            self._log.info(f'The following indices were squeezed: {squeezed_indices}')
        squeezed_scale = tuple([self.scale[i] for i in range(len(self.dim)) if i not in squeezed_indices])
        return Field(squeezed_data, squeezed_scale, self.vector)

    def pad(self, pad_width, mode='constant', **kwargs):
        """Pad the `Field` object and increase the size of the underlying array.

        Parameters
        ----------
        pad_width : {sequence, array_like, int}
            Number of values padded to the edges of each axis. Can be a single number for all, one number per axis or
            a tuple `(before, after)` for each axis for finer control.
        mode : str, optional
            Padding mode (see `numpy.pad` for all options), by default 'constant', which pads with zeros.

        Returns
        -------
        field: `Field`
            The padded `Field` object.

        """
        if isinstance(pad_width, Number):  # Paddding is the same for each dimension (make sure it is a tuple)!
            pad_width = (pad_width,) * len(self.dim)
        pad_width = [(p, p) if isinstance(p, Number) else p for p in pad_width]
        if self.vector:  # Append zeros to padding, so component axis stays as is:
            pad_width = pad_width + [(0, 0)]
        data_new = np.pad(self.data, pad_width, mode, **kwargs)
        return Field(data_new, self.scale, self.vector)

    def bin(self, n):
        """Bins data of the `Field` to decrease the size of the underlying array by averaging over a number of values.

        Parameters
        ----------
        n : {sequence, array_like, int}
            Number of entries along each axis over which the average is taken. Can be a single integer for all axes or a
            list, specifying the number of entries over which to average for each individual axis.

        Returns
        -------
        field: `Field`
            The binned `Field` object.

        Notes
        -----
        Padding takes place before binning to ensure the dimensions are multiples of `n`. The padding mode is `edge`.

        """
        self._log.debug('Calling bin')
        assert isinstance(n, (int, tuple)), 'n must be a positive integer or a tuple of positive integers!'
        if isinstance(n, Number):  # Binning is the same for each dimension (make sure it is a tuple)!
            n = (n,) * len(self.dim)
        assert all([n_i >= 0 for n_i in n]), 'All entries of n must be positive integers!'
        # Pad if necessary (use padded 'field' from here on), formula for clarity: (n - dim % n) % n
        pad_width = [(0, (n[i] - self.dim[i] % n[i]) % n[i]) for i in range(len(self.dim))]
        field = self.pad(pad_width, mode='edge')
        # Create new shape used for binning (mean over every second axis will be taken):
        bin_shape = list(np.ravel([(field.dim[i]//n[i], n[i]) for i in range(len(field.dim))]))
        mean_axes = np.arange(1, 2*len(field.dim), 2)  # every 2nd axis!
        if self.vector:  # Vector field:
            bin_shape += [field.ncomp]  # Append component axis (they stay unchanged)
        # Bin data and scale accordingly:
        data_new = field.data.reshape(bin_shape).mean(axis=tuple(mean_axes))
        scale_new = tuple([field.scale[i] * n[i] for i in range(len(field.dim))])
        return Field(data_new, scale_new, self.vector)

    def zoom(self, zoom, **kwargs):
        """Wrapper for the `scipy.ndimage.zoom` function.

        Parameters
        ----------
        zoom : float or sequence
            Zoom factor along the axes. If a float, `zoom` is the same for each axis. If a sequence, `zoom` needs to
            contain one value for each axis.

        Returns
        -------
        field: `Field`
            The zoomed in `Field` object.

        Notes
        -----
        As in `scipy.ndimage.zoom`, a spline order can be specified, which defaults to 3.

        """
        self._log.debug('Calling zoom')
        if not self.vector:  # Scalar field:
            data_new = interpolation.zoom(self.data, zoom, **kwargs)
        else:  # Vector field:
            comps = [np.asarray(comp) for comp in self.comp]
            data_new = np.stack([interpolation.zoom(comp, zoom, **kwargs) for comp in comps], axis=-1)
        if isinstance(zoom, Number):  # Zoom is the same for each dimension!
            zoom = (zoom,) * len(self.dim)
        scale_new = tuple([self.scale[i]/z for i, z in enumerate(zoom)])
        return Field(data_new, scale_new, self.vector)

    def gradient(self):
        """Returns the gradient of an N-dimensional scalar `Field`. Wrapper around the according numpy function.

        Returns
        -------
        gradients: ndarray or list of ndarray
            A set of ndarrays (or a single ndarray for 1D input), corresponding to the derivatives of the field with
            respect to each dimension.

        Notes
        -----
        The field is implicitely squeezed before the gradient is calculated!

        """
        self._log.debug('Calling gradient')
        assert not self.vector, 'Gradient can only be computed from scalar fields!'
        squeezed_field = self.squeeze()  # Gradient along dimension of length 1 does not work!
        gradients = np.gradient(np.asarray(squeezed_field), *squeezed_field.scale)
        if len(squeezed_field.dim) == 1:  # Only one gradient!
            return Field(gradients, squeezed_field.scale, vector=False)
        else:  # Multidimensional gradient (flip component order with [::-1], so that e.g x/y/z instead of z/y/x):
            return Field(np.stack(gradients[::-1], axis=-1), squeezed_field.scale, vector=True)

    def curl(self):
        """Returns the curl of an N-dimensional `Field`.

        Returns
        -------
        field: `Field`
            The curl/rotation.

        Notes
        -----
        The calculation depends on the input:
        3 dimensions, 3 components: Calculates the full 3D rotational vector field!
        2 dimensions, 2 components: Calculates the out-of-plane component of the curl as a 2D scalar field!
        2 dimensions, scalar: Calculates the planar rotation as a 2D vector field!

        """
        self._log.debug('Calling curl')
        squeezed_field = self.squeeze()
        if len(squeezed_field.dim) == 3:  # 3 dimensions:
            if squeezed_field.ncomp == 3:  # 3 component vector field (standard case):
                self._log.debug('input: 3 dimensions, 3 components!')
                field_x, field_y, field_z = squeezed_field.comp
                gradx_x, grady_x, gradz_x = field_x.gradient().comp
                gradx_y, grady_y, gradz_y = field_y.gradient().comp
                gradx_z, grady_z, gradz_z = field_z.gradient().comp
                curl_x = grady_z - gradz_y
                curl_y = gradz_x - gradx_z
                curl_z = gradx_y - grady_x
                return Field.from_scalar_fields([curl_x, curl_y, curl_z])
            else:
                raise AssertionError('Can only handle 3 component vector fields in 3D!')
        elif len(squeezed_field.dim) == 2:  # 2 dimensions (tricky, usually not hardly defined):
            if squeezed_field.ncomp == 2:  # 2 component vector field (return perpendicular component as scalar field):
                self._log.debug('input: 2 dimensions, 2 components!')
                field_x, field_y = squeezed_field.comp
                gradx_x, grady_x = field_x.gradient().comp
                gradx_y, grady_y = field_y.gradient().comp
                return gradx_y - grady_x
            elif not squeezed_field.vector:  # scalar field (return planar components as 2D vector field):
                self._log.debug('input: 3 dimensions, scalar field!')
                gradx, grady = squeezed_field.gradient().comp
                curl_x = grady
                curl_y = -gradx
                return Field.from_scalar_fields([curl_x, curl_y])
            else:
                raise AssertionError('Can only handle 3 component vector or scalar fields in 2D!')
        else:
            raise AssertionError('Can only handle 3D or 2D cases (see documentation for specifics)!')

    def clip(self, vmin=None, vmax=None, sigma=None, mask=None):
        """Clip (limit) the values in an array. For vector fields, this will take the amplitude into account.

        Parameters
        ----------
        vmin : float, optional
            Mimimum value, by default None. Is ignored for vector fields. Will overwrite values found via `sigma` or
            `mask`.
        vmax : float, optional
            Maximum value, by default None. Will overwrite values found via `sigma` or `mask`.
        sigma : float, optional
            Defines a range in standard deviations, that results in a boolean mask that excludes outliers, by default
            None. E.g. `sigma=2` will mark points within the 5% highest amplitude as outliers. `vmin` and `vmax` will be
            searched in the remaining region. Is logically combined with `mask` if both are set.
        mask : ndarray, optional
            Boolean array that directly describes where to search for `vmin` and `vmax`, by default None. Is logically
            combined with the mask from `sigma` if both are set.

        Returns
        -------
        field: `Field`
            The clipped `Field`.

        Notes
        -----
        In contrast to the corresponding numpy function, `vmin` and `vmax` can both be `None` due to the alternative
        clipping strategies employed here.

        """
        self._log.debug('Calling clip')
        amp = self.amp.data
        if mask is None:  # If no mask is set yet, default to True everywhere:
            mask = np.full(self.dim, True)
        if sigma is not None:  # Mark outliers that are outside `sigma` standard deviations:
            sigma_mask = (amp - amp.mean()) < (sigma * amp.std())
            mask = np.logical_and(mask, sigma_mask)
        # Determine vmin and vmax if they are not set by the user:
        amp_masked = np.where(mask, amp, np.nan)
        if vmin is None:
            vmin = np.nanmin(amp_masked)
        if vmax is None:
            vmax = np.nanmax(amp_masked)
        if self.vector:  # Vector fields need to scale components according to masked amplitude
            mask_vec = (amp <= vmax)[..., None]  # Only vmax is important for vectors! mask_vec broadcast to components!
            data = np.where(mask_vec, self.data, vmax * self.data/amp[..., None])  # Scale outliers to vmax!
        else:  # For scalar fields, just delegate to the numpy function:
            data = np.clip(self.data, vmin, vmax)
        return Field(data, self.scale, self.vector)
