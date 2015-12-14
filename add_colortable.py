#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# add_colortable.py
# ---------------------------------------------------------
# Apply a colortable to turn grayscale raster to pseudocolor
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      add_colortable.py input output colortable
#      where:
#           input       input GeoTIFF with Gray legend to which colortable will be attached
#           output      output GeoTIFF
#           colortable  path to colortable e:\dhi\colortables\fpar.txt
# Example:
#      python add_colortable.py input.tif output.tif 
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

import os
import sys
import shutil

def attach_color_table(f_in_name,f_out_name,f_clrs_name):
    f_vrt_name = f_in_name.replace(".tif",".vrt")
    f_vrt_name2 = f_in_name.replace(".tif","_2.vrt")
    cmd = "gdal_translate -of VRT " + f_in_name + " " + f_vrt_name
    os.system(cmd)
    
    f_vrt_in = open(f_vrt_name,'rb')
    f_vrt_out = open(f_vrt_name2,'wb')
    f_clrs = open(f_clrs_name,'rb')
    
    for str in f_vrt_in:
        if "<ColorInterp>Gray" in str:
            f_vrt_out.write("<ColorInterp>Palette</ColorInterp>\n")
            for clr in f_clrs:
                f_vrt_out.write(clr)
        else:
            f_vrt_out.write(str)
    
    f_vrt_out.write("\n")
    f_vrt_out.close()
    f_vrt_in.close()
    
    cmd = "gdal_translate " + f_vrt_name2 + " temp.tif"
    os.system(cmd)
    shutil.move('temp.tif',f_out_name)
    os.remove(f_vrt_name)
    os.remove(f_vrt_name2)
    
if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    colortable = sys.argv[3]
    
    #attach color table
    attach_color_table(input,output,colortable)
    