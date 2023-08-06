# -*- coding: utf-8 -*-
# Copyright 2020 by Forschungszentrum Juelich GmbH
# Author: J. Caron
#
"""Subpackage containing EMPyRe IO functionality for the Field class."""


from . import llg, numpy, ovf, tec, text, vtk


plugin_list = [llg, numpy, ovf, tec, text, vtk]
__all__ = ['plugin_list']
