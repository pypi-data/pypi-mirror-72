# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO functionality for Field objects."""


import logging
import os

from ..fields.field import Field
from .field_plugins import plugin_list


__all__ = ['load_field', 'save_field']
_log = logging.getLogger(__name__)


def load_field(filename, scale=None, vector=None, **kwargs):
    """Load supported file into a :class:`~..fields.Field` instance.

    The function loads the file according to the extension:
        SCALAR???
        - hdf5 for HDF5.  # TODO: You can use comp_pos here!!!
        - EMD Electron Microscopy Dataset format (also HDF5).
        - npy or npz for numpy formats.

        PHASEMAP
        - hdf5 for HDF5.
        - rpl for Ripple (useful to export to Digital Micrograph).
        - dm3 and dm4 for Digital Micrograph files.
        - unf for SEMPER unf binary format.
        - txt format.
        - npy or npz for numpy formats.
        - Many image formats such as png, tiff, jpeg...

        VECTOR
        - hdf5 for HDF5.
        - EMD Electron Microscopy Dataset format (also HDF5).
        - llg format.
        - ovf format.
        - npy or npz for numpy formats.

    Any extra keyword is passed to the corresponsing reader. For available options see their individual documentation.

    Parameters
    ----------
    filename:  str
        The filename to be loaded.
    scale: tuple of float, optional
        Scaling along the dimensions of the underlying data. Default is 1.
    vector: bool, optional
        True if the field should be a vector field, False if it should be interpreted as a scalar field (default).

    Returns
    -------
    field: `Field`
        A `Field` object containing the loaded data.

    Notes
    -----
    Falls back to HyperSpy routines for loading data, make sure it is installed if you need the full capabilities.

    """
    _log.debug('Calling load_field')
    extension = os.path.splitext(filename)[1]
    for plugin in plugin_list:  # Iterate over all plugins:
        if extension in plugin.file_extensions:  # Check if extension is recognised:
            return plugin.reader(filename, scale=scale, vector=vector, **kwargs)
    # If nothing was found, try HyperSpy
    _log.debug('Using HyperSpy')
    try:
        import hyperspy.api as hs
    except ImportError:
        _log.error('This extension recquires the hyperspy package!')
        return
    comp_pos = kwargs.pop('comp_pos', -1)
    return Field.from_signal(hs.load(filename, **kwargs), scale=scale, vector=vector, comp_pos=comp_pos)


def save_field(filename, field, **kwargs):
    """Saves the Field  in the specified format.

    The function gets the format from the extension:
        - hdf5 for HDF5.
        - EMD Electron Microscopy Dataset format (also HDF5).
        - npy or npz for numpy formats.

    If no extension is provided, 'hdf5' is used. Most formats are saved with the HyperSpy package (internally the field
    is first converted to a HyperSpy Signal.
    Each format accepts a different set of parameters. For details see the specific format documentation.

    Parameters
    ----------
    filename : str, optional
        Name of the file which the Field is saved into. The extension determines the saving procedure.

    """
    """Saves the phasemap in the specified format.

    The function gets the format from the extension:
        - hdf5 for HDF5.
        - rpl for Ripple (useful to export to Digital Micrograph).
        - unf for SEMPER unf binary format.
        - txt format.
        - Many image formats such as png, tiff, jpeg...

    If no extension is provided, 'hdf5' is used. Most formats are
    saved with the HyperSpy package (internally the phasemap is first
    converted to a HyperSpy Signal.

    Each format accepts a different set of parameters. For details
    see the specific format documentation.

    Parameters
    ----------
    filename: str, optional
        Name of the file which the phasemap is saved into. The extension
        determines the saving procedure.
    save_mask: boolean, optional
        If True, the `mask` is saved, too. For all formats, except HDF5, a separate file will
        be created. HDF5 always saves the `mask` in the metadata, independent of this flag. The
        default is False.
    save_conf: boolean, optional
        If True, the `confidence` is saved, too. For all formats, except HDF5, a separate file
        will be created. HDF5 always saves the `confidence` in the metadata, independent of
        this flag. The default is False
    pyramid_format: boolean, optional
        Only used for saving to '.txt' files. If this is True, the grid spacing is saved
        in an appropriate header. Otherwise just the phase is written with the
        corresponding `kwargs`.

    """
    _log.debug('Calling save_field')
    extension = os.path.splitext(filename)[1]
    for plugin in plugin_list:  # Iterate over all plugins:
        if extension in plugin.file_extensions:  # Check if extension is recognised:
            plugin.writer(filename, field, **kwargs)
            return
    # If nothing was found, try HyperSpy:
    _log.debug('Using HyperSpy')
    field.to_signal().save(filename, **kwargs)
