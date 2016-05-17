#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# calc_all.py
# ---------------------------------------------------------
# Run a calculation for a series of rasters
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      calc_all.py [-h] [-t TYPE] val input_folder output_folder
#      where:
#           -h             show this help message and exit
#           value          all values greater than val will be set to NODATA
#           input_folder   input folder
#           output_folder  output folder
#           type           Int32, Int16, Float64, UInt16, Byte, UInt32, Float32
# Example:
#      python calc_all.py 200 y:\vcf\global\ y:\vcf\global\calc UInt16
#
# Copyright (C) 2015 Maxim Dubinin (sim@gis-lab.info), Alexander Muriy (amuriy AT gmail.com)
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

import glob
import os
import sys
import shutil
import argparse
import tempfile

parser = argparse.ArgumentParser()
#parser.add_argument('val', help='Value to use as a threshold')
parser.add_argument('input_folder', help='Input folder')
parser.add_argument('output_folder', help='Output folder')
parser.add_argument('-t','--type', help='Int32, Int16, Float64, UInt16, Byte, UInt32, Float32')
parser.add_argument('-o','--overwrite', action="store_true", help='Overwrite outputs')
args = parser.parse_args()


def sanitize():
    if not args.input_folder.endswith('\\'): args.input_folder = args.input_folder + '\\'
    if not args.output_folder.endswith('\\'): args.output_folder = args.output_folder + '\\'
    return args.input_folder,args.output_folder

if __name__ == '__main__':
    id,od = sanitize()

    if not args.type:
        type = ''
    else:
        type = '--type=' + args.type

    os.chdir(id)

    tifs = glob.glob('*.tif')
    # tifs = glob.glob('2015.01.01.tif')
    for tif in tifs:
        if not os.path.exists(od + tif) or args.overwrite:
            print('Processing ... ' + tif)
            temp1 = id + os.sep + 'temp1_' + tif 
            temp2 = id + os.sep + 'temp2_' + tif

            cmd1 = 'gdal_calc.bat ' + type + '-A ' + tif + ' --outfile=' + temp1 + ' --calc="A/10000.0" --NoDataValue=255 --type="Float32" --overwrite'
            cmd2 = 'gdal_calc.bat ' + type + '-A ' + temp1 + ' --outfile=' + temp2 + ' --calc="A*(A>0)" --NoDataValue=255 --type="Float32" --overwrite'
            print (cmd1)
            os.system(cmd1)
            print (cmd2)
            os.system(cmd2)
            shutil.move(temp2,od + tif)
            os.remove(temp1)
            
        elif os.path.exists(od + tif) and not args.overwrite:
            print('Output exists and overwrite is off, skipping')