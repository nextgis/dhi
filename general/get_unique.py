#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# get_unique.py
# ---------------------------------------------------------
# Create a list of unique values from series of rasters
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      get_unique.py [-h] (-rs RASTERS | -fs FOLDERS) output
#      where:
#           -h                 show this help message and exit
#           -rs                path(s) to raster, separate by comma if several
#           -fs                path(s) to folders with raster, separate by comma if several
#           output             text file where unique values will be stored
# Examples:
#      python get_unique.py -fs y:\dhi\global\fpar_4\,y:\dhi\global\fpar_4\combined\ out.txt
#      python get_unique.py -rs y:\dhi\global\fpar_4\raster1.tif,y:\dhi\global\fpar_4\combined\raster2.tif out.txt
#
# Copyright (C) 2015 Maxim Dubinin (sim@gis-lab.info)
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

from osgeo import gdal
import numpy as np
import sys
import glob
import argparse
from progressbar import *
import struct

parser = argparse.ArgumentParser()
parser.add_argument('output_unique', help='Output file with unique value')
parser.add_argument('output_counts', help='Output file with counts')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-rs','--rasters', help='full raster path(s), separate by comma if several')
group.add_argument('-fs','--folders', help='path(s) to folders with raster, separate by comma if several')

args = parser.parse_args()
inRasters = []

if args.folders:
    rasterPaths = args.folders.split(',')
    for rasterPath in rasterPaths:
        inRasters.extend(glob.glob(rasterPath + '*.tif'))

if args.rasters:
    inRasters.extend(args.rasters.split(','))

unique_values_all = ()

def countValues(val):
    #TODO: use something faster, get rid on struct

    count_value = 0

    pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Counter(), " of " + str(band.YSize), ' ', ETA()]).start()
    pbar.maxval = band.YSize

    for y in range(band.YSize):

        pbar.update(pbar.currval+1)

        scanline = band.ReadRaster(0, y, band.XSize, 1, band.XSize, 1, band.DataType)
        values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)

        for value in values:
            if value == val:
                count_value += 1

    dataset = None
    pbar.finish()

    return count_value


if __name__ == '__main__':
    fmttypes = {'Byte':'B', 'UInt16':'H', 'Int16':'h', 'UInt32':'I', 'Int32':'i', 'Float32':'f', 'Float64':'d'}

    for raster in inRasters:
        print('Processing raster ' + raster)
        
        ds = gdal.Open(raster)
        band = ds.GetRasterBand(1)
        BandType = gdal.GetDataTypeName(band.DataType)

        cols = band.XSize
        rows = band.YSize

        nBlockXSize = band.GetBlockSize()[0]
        nBlockYSize = band.GetBlockSize()[1]
        
        pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Counter(), " of " + str(rows), ' ', ETA()]).start()
        pbar.maxval = rows
        
        unique_values = ()
        for x in range(rows):
            array = band.ReadAsArray(0, x, cols, 1)
            unique_values_line = np.unique(array)
            
            unique_values = np.unique(np.hstack((unique_values,unique_values_line)))
            pbar.update(pbar.currval+1)
        
        unique_values_all = np.unique(np.hstack((unique_values_all,unique_values)))
        print('Found ' + str(len(unique_values)) + ' values for current raster. Total unique: ' + str(len(unique_values_all))+'\n')
        pbar.finish()
            
        f_out_unique = open(args.output_unique,'wb')
        for val in unique_values_all:
            f_out_unique.write(str(int(val)) + '\n')

        f_out_unique.close()

        f_out_counts = open(args.output_counts,'wb')
        for val in unique_values_all:
            print "Calculating count for %d" % val
            count_value = countValues(val)
            f_out_counts.write(str(int(val)) + ',' + str(count_value) + '\n')

        f_out_counts.close()
        