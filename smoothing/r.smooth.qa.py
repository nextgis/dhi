#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# r.smooth.qa.py
# ---------------------------------------------------------
#
# Copyright (C) 2015 Kolesov Dmitry (kolesov.dm@gmail.com)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

#%module
#% description: Create QA rasters for DHI smoothing procedure (filter.py)
#% keyword: smoothing, QA
#%end
#%option
#% key: inputs
#% type: string
#% required: yes
#% multiple: yes
#% key_desc: input rasters
#% description: list of input rasters
#%end
#%option
#% key: outputs
#% type: string
#% required: yes
#% multiple: yes
#% key_desc: output rasters
#% description: list of output rasters
#%end
#%option
#% key: methods
#% type: string
#% required: no
#% multiple: yes
#% key_desc: methods for QA creation
#% answer: all
#% description: count; count of NULL values; longest_row; length of longest row of NULL values
#%end
#%option
#% key: mapset
#% type: string
#% required: no
#% multiple: no
#% key_desc: mapset 
#% description: name of mapset of input rasters
#%end


import sys
import os


if "GISBASE" not in os.environ:
    sys.stderr.write("You must be in GRASS GIS to run this program.\n")
    sys.exit(1)

from collections import OrderedDict

import numpy as np

import grass.script as grass
from grass.pygrass import raster
from grass.pygrass.raster.buffer import Buffer
from grass.exceptions import OpenError
from grass.pygrass.gis.region import Region



CNULL = -2147483648  # null value for CELL maps
FNULL = np.nan # null value for FCELL and DCELL maps

def init_rasters(names, mapset=""):
    """Get list of raster names,
    return array of the rasters
    """
    rasters = OrderedDict()
    for name in names:
        r = raster.RasterSegment(name, mapset=mapset)
        rasters[name] = r
    return rasters


def open_rasters(raster_list, write=False, rast_type='DCELL'):
    for r in raster_list:
        try:
            if write:
                if r.exist():
                    r.open('w', rast_type, overwrite=grass.overwrite())
                else:
                    r.open('w', rast_type)
            else:
                r.open()
        except OpenError:
            grass.fatal("Can't open raster %s" % (r.name, ))

def close_rasters(raster_list):
    for r in raster_list:
        if r.is_open():
            r.close()


def _get_row_or_nan(raster, row_num):
    row = raster.get_row(row_num)
    if raster.mtype != 'CELL':
        return row
    nans = (row == CNULL)
    row = row.astype(np.float64)
    row[nans.astype(np.bool)] = np.nan
    return row


def count_null(series):
    return np.count_nonzero(np.isnan(series))


def count_longest_row(series):
    max_len = 0
    current = 0
    for i in series:
        if np.isnan(i):
           current += 1
           max_len = max([current, max_len])
        else:
            current = 0
    return max_len


def _filter(fun, row_data):
    _, cols = row_data.shape
    result = np.empty(cols)
    for i in range(cols):
        arr = row_data[:, i]
        result[i] = fun(arr)

    return result

def make_qa(methods, input_names, out_names):

    current_mapset = grass.read_command('g.mapset', flags='p')
    current_mapset = current_mapset.strip()

    inputs = init_rasters(input_names)
    outputs = init_rasters(out_names, mapset=current_mapset)
    
    output_mapper = dict(zip(methods, out_names)) 
    try:
        open_rasters(outputs.values(), write=True)
        open_rasters(inputs.values())

        reg = Region()
        for i in range(reg.rows):
            # import ipdb; ipdb.set_trace()
            row_data = np.array([_get_row_or_nan(r, i) for r in inputs.values()])
            for map_num, met in enumerate(methods):
                fun = METHOD_MAPPER[met]
                result_row = _filter(fun, row_data)
                map = outputs[output_mapper[met]]
                buf = Buffer(result_row.shape, map.mtype, result_row)
                map.put_row(i, buf)
    finally:
        close_rasters(outputs.values())
        close_rasters(inputs.values())



METHOD_MAPPER = dict(
    count=count_null,
    longest_row=count_longest_row
)



def main(options, flags): 
    mapset = options['mapset']
    inputs = options['inputs']
    inputs = inputs.split(',')

    outputs = options['outputs']
    outputs = outputs.split(',')

    methods = options['methods']
    if methods == 'all':
        methods = 'count,longest_row'
    methods = methods.split(',')
    assert len(methods) == len(outputs)

    
    make_qa(methods, inputs, outputs)

if __name__ == "__main__":
    options, flags = grass.parser()
    sys.exit(main(options, flags))



