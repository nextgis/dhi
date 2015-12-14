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
#      calc_all.py val input_folder output_folder type
#      where:
#           val            all values greater than val will be set to NODATA
#           input_folder   input folder
#           output_folder  output folder
#           type           Int32, Int16, Float64, UInt16, Byte, UInt32, Float32
# Example:
#      python calc_all.py 200 y:\vcf\global\ y:\vcf\global\calc UInt16
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

import glob
import os
import sys
import shutil

wd = os.getcwd()
val = sys.argv[1]
id = sys.argv[2]
od = sys.argv[3]
type = sys.argv[4]

os.chdir(id)

tifs = glob.glob('*.tif')
for tif in tifs:
    cmd = 'gdal_calc.bat ' + type + '-A ' + tif + ' --outfile=temp.tif ' + tif + ' --calc="A*(A>' + val + ') " --NoDataValue=0'
    os.system(cmd)
    
    shutil.move('temp.tif',od + tif)