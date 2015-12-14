#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# colortable_all.py
# ---------------------------------------------------------
# Apply a colortable to turn grayscale raster to pseudocolor to a series of rasters
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      colortable_all.py input_folder output_folder colortable
#      where:
#           input_folder   input folder
#           output_folder  output folder
#           colortable     path to colortable
# Example:
#      python colortable_all.py y:\landcover\gray\ y:\landcover\color e:\dhi\colortables\fpar.txt
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
import shutil
import sys

wd = os.getcwd()
f_clrs_name = sys.argv[1]
id = sys.argv[2]
od = sys.argv[3]
os.chdir(id)

tifs = glob.glob('*.tif')
for f_in_name in tifs:
    f_vrt_name = f_in_name.replace(".tif",".vrt")
    f_vrt_name2 = f_in_name.replace(".tif","_2.vrt")
    cmd = "gdal_translate -of VRT " + f_in_name + " " + f_vrt_name
    os.system(cmd)
    
    f_vrt_in = open(f_vrt_name,'rb')
    f_vrt_out = open(f_vrt_name2,'wb')
    f_clrs = open(f_clrs_name,'rb')
    
    for str in f_vrt_in:
        if "<ColorInterp>Gray" in str or "<ColorInterp>Palette" in str:
            f_vrt_out.write("<ColorInterp>Palette</ColorInterp>\n")
            for clr in f_clrs:
                f_vrt_out.write(clr)
        elif "ColorTable" in str or "Entry" in str:
            continue #do nothing
        else:
            f_vrt_out.write(str)
    
    f_vrt_out.write("\n")
    f_vrt_out.close()
    f_vrt_in.close()
    
    cmd = "gdal_translate " + f_vrt_name2 + " temp.tif"
    os.system(cmd)
    os.remove(f_in_name)
    shutil.move('temp.tif',od + f_in_name)
    os.remove(f_vrt_name)
    os.remove(f_vrt_name2)
    
