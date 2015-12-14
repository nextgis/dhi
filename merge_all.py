#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# merge_all.py
# ---------------------------------------------------------
# Merge series of rasters in virtual dataset or TIF
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      merge_all.py output separate pixel_size input_folder output_folder
#      where:
#           output          output.vrt file or output.tif
#           separate        "yes" if you want to layerstack, "no" for mosaiced
#           pixel_size      pixel size, pixels are square
#           input_folder    input folder with TIFs
#           output_folder   where result will be stored
# Examples:
#      python merge_all.py 2000.vrt no 0 y:\source\MOD44B\2000.03.05\tif_vcf1\ y:\source\MOD44B\2000.03.05\tif_vcf1\
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

wd = os.getcwd()

fn = sys.argv[1]        #filename.vrt or filename.tif
separate = sys.argv[2]  #yes is set
pix_size = sys.argv[3]  #0 if not set
id = sys.argv[4]        #input
od = sys.argv[5]

os.chdir(id)

tifs = glob.glob('*.tif')
list_of_tifs = ' '.join(tifs)

if separate == 'yes': 
    separate = '-separate'
else:
    separate = ''
    
if pix_size != '0': 
    pix_size = '-ps ' + pix_size + ' ' + pix_size
else:
    pix_size = ''

if fn.split('.')[-1] == 'vrt': 
    pix_size = pix_size.replace('ps','tr')
    cmd = 'gdalbuildvrt' + separate + ' ' + pix_size + ' ' + ' -o ' + fn + ' ' + list_of_tifs
else:
    cmd = 'gdal_merge ' + separate + ' ' + pix_size + ' ' + ' -o ' + od + fn + ' ' + list_of_tifs
    
print cmd
os.system(cmd)
