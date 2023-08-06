# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""IO plugin for simple text format."""


import logging
import os

import numpy as np

from ...fields.field import Field


_log = logging.getLogger(__name__)

file_extensions = ('.ovf', '.omf', '.ohf', 'obf')  # Recognised file extensions


def reader(filename, scale=None, vector=None, segment=None, **kwargs):
    """More info at:

    http://math.nist.gov/oommf/doc/userguide11b2/userguide/vectorfieldformat.html
    http://math.nist.gov/oommf/doc/userguide12a5/userguide/OVF_2.0_format.html

    """
    _log.debug('Calling reader')
    if vector is None:
        vector = True
    assert vector is True, 'Only vector fields can be loaded from ovf-files!'
    with open(filename, 'rb') as load_file:
        line = load_file.readline()
        assert line.startswith(b'# OOMMF')  # File has OVF format!
        read_header, read_data = False, False
        header = {'version': line.split()[-1].decode('utf-8')}
        x_mag, y_mag, z_mag = [], [], []
        data_mode = None
        while True:
            # --- READ START OF FILE OR IN BETWEEN SEGMENTS LINE BY LINE ---------------------------
            if not read_header and not read_data:  # Start of file or between segments!
                line = load_file.readline()
                if line == b'':
                    break  # End of file is reached!
                if line.startswith(b'# Segment count'):
                    seg_count = int(line.split()[-1])  # Total number of segments (often just 1)!
                    seg_curr = 0  # Current segment (0: not in first segment, yet!)
                    if seg_count > 1:  # If multiple segments, check if "segment" was set correctly:
                        assert segment is not None, (f'Multiple ({seg_count}) segments were found! '
                                                     'Chose one via the segment parameter!')
                    elif segment is None:  # Only one segment AND parameter not set:
                        segment = 1  # Default to the first/only segment!
                    assert 0 < segment <= seg_count, (f'parameter segment={segment} out of bounds, '
                                                      f'Use value between 1 and {seg_count}!')
                    header['segment_count'] = seg_count
                elif line.startswith(b'# Begin: Segment'):  # Segment start!
                    seg_curr += 1
                    if seg_curr > segment:
                        break  # Stop reading the file!
                elif line.startswith(b'# Begin: Header'):  # Header start!
                    read_header = True
                elif line.startswith(b'# Begin: Data'):  # Data start!
                    read_data = True
                    data_mode = ' '.join(line.decode('utf-8').split()[3:])
                    assert data_mode in ['text', 'Text', 'Binary 4', 'Binary 8'], \
                        f'Data mode {data_mode} is currently not supported by this reader!'
                    assert header.get('meshtype') == 'rectangular', \
                        'Only rectangular grids can be currently read!'
            # --- READ HEADER LINE BY LINE ---------------------------------------------------------
            elif read_header:
                line = load_file.readline()
                if line.startswith(b'# End: Header'):  # Header is done:
                    read_header = False
                    continue
                line = line.decode('utf-8')  # Decode to use strings here!
                line_list = line.split()
                if '##' in line_list:  # Strip trailing comments:
                    del line_list[line_list.index('##'):]
                if len(line_list) <= 1:  # Just '#' or empty line:
                    continue
                key, value = line_list[1].strip(':'), ' '.join(line_list[2:])
                if key not in header:  # Add new key, value pair if not existant:
                    header[key] = value
                elif key == 'Desc':  # Description can go over several lines:
                    header['Desc'] = ' '.join([header['Desc'], value])
            # --- READ DATA LINE BY LINE -----------------------------------------------------------
            elif read_data:  # Currently in a data block:
                if data_mode in ['text', 'Text']:  # Read data as text, line by line:
                    line = load_file.readline()
                    if line.startswith(b'# End: Data'):
                        read_data = False  # Stop reading data and search for new segments!
                        continue
                    elif seg_curr < segment:  # Do nothing with the line if wrong segment!
                        continue
                    else:
                        x, y, z = [float(i) for i in line.split()]
                        x_mag.append(x)
                        y_mag.append(y)
                        z_mag.append(z)
                elif 'Binary' in data_mode:  # Read data as binary, all bytes at the same time:
                    # Currently every segment is read until the wanted one is processed. Only that one is returned!
                    count = int(data_mode.split()[-1])  # Either 4 or 8!
                    if header['version'] == '1.0':  # Big endian float:
                        dtype = f'>f{count}'
                    elif header['version'] == '2.0':  # Little endian float:
                        dtype = f'<f{count}'
                    test = np.fromfile(load_file, dtype=dtype, count=1)  # Read test byte!
                    if count == 4:  # Binary 4:
                        assert test == 1234567.0, 'Wrong test bytes!'
                    elif count == 8:  # Binary 8:
                        assert test == 123456789012345.0, 'Wrong test bytes!'
                    dim = (int(header['znodes']), int(header['ynodes']), int(header['xnodes']))
                    data_raw = np.fromfile(load_file, dtype=dtype, count=3*np.prod(dim))
                    x_mag, y_mag, z_mag = data_raw[0::3], data_raw[1::3], data_raw[2::3]
                    read_data = False  # Stop reading data and search for new segments (if any).
        # --- READING DONE -------------------------------------------------------------------------
        # Format after reading:
        dim = (int(header['znodes']), int(header['ynodes']), int(header['xnodes']))
        x_mag = np.asarray(x_mag).reshape(dim)
        y_mag = np.asarray(y_mag).reshape(dim)
        z_mag = np.asarray(z_mag).reshape(dim)
        data = np.stack((x_mag, y_mag, z_mag), axis=-1) * float(header.get('valuemultiplier', 1))
        if scale is None:
            unit = header.get('meshunit', 'nm')
            if unit == 'unspecified':
                unit = 'nm'
            _log.info(f'unit: {unit}')
            unit_scale = {'m': 1e9, 'mm': 1e6, 'µm': 1e3, 'nm': 1}[unit]
            xstep = float(header.get('xstepsize')) * unit_scale
            ystep = float(header.get('ystepsize')) * unit_scale
            zstep = float(header.get('zstepsize')) * unit_scale
            scale = (zstep, ystep, xstep)
    return Field(data, scale=scale, vector=True)


def writer(filename, field, **kwargs):
    _log.debug('Call writer')
    assert field.vector and len(field.dim) == 3, 'Only 3D vector fields can be saved to ovf files!'
    with open(filename, 'w') as save_file:
        save_file.write('# OOMMF OVF 2.0\n')
        save_file.write('# Segment count: 1\n')
        save_file.write('# Begin: Segment\n')
        # Write Header:
        save_file.write('# Begin: Header\n')
        name = os.path.split(filename)[1]
        save_file.write(f'# Title: PYRAMID-VECTORDATA {name}\n')
        save_file.write('# meshtype: rectangular\n')
        save_file.write('# meshunit: nm\n')
        save_file.write('# valueunit: A/m\n')
        save_file.write('# valuemultiplier: 1.\n')
        save_file.write('# xmin: 0.\n')
        save_file.write('# ymin: 0.\n')
        save_file.write('# zmin: 0.\n')
        save_file.write(f'# xmax: {field.scale[2] * field.dim[2]}\n')
        save_file.write(f'# ymax: {field.scale[1] * field.dim[1]}\n')
        save_file.write(f'# zmax: {field.scale[0] * field.dim[0]}\n')
        save_file.write('# xbase: 0.\n')
        save_file.write('# ybase: 0.\n')
        save_file.write('# zbase: 0.\n')
        save_file.write(f'# xstepsize: {field.scale[2]}\n')
        save_file.write(f'# ystepsize: {field.scale[1]}\n')
        save_file.write(f'# zstepsize: {field.scale[0]}\n')
        save_file.write(f'# xnodes: {field.dim[2]}\n')
        save_file.write(f'# ynodes: {field.dim[1]}\n')
        save_file.write(f'# znodes: {field.dim[0]}\n')
        save_file.write('# End: Header\n')
        # Write data:
        save_file.write('# Begin: Data Text\n')
        x_mag, y_mag, z_mag = field.comp
        x_mag = x_mag.data.ravel()
        y_mag = y_mag.data.ravel()
        z_mag = z_mag.data.ravel()
        for i in range(np.prod(field.dim)):
            save_file.write(f'{x_mag[i]:g} {y_mag[i]:g} {z_mag[i]:g}\n')
        save_file.write('# End: Data Text\n')
        save_file.write('# End: Segment\n')
