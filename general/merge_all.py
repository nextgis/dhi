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
#      merge_all.py [-h] [-ps PIXEL_SIZE] [-s SEPARATE] output input_folder output_folder
#      where:
#           -h              show this help message and exit
#           output          output VRT or TIF file
#           separate        "yes" if you want to layerstack, "no" for mosaiced
#           pixel_size      pixel size, pixels are square
#           input_folder    input folder with TIFs
#           output_folder   where result will be stored
# Examples:
#      python merge_all.py 2000.vrt y:\source\MOD44B\2000.03.05\tif_vcf1\ y:\source\MOD44B\2000.03.05\tif_vcf1\ 0.0083
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
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('output', help='Output VRT or TIF file')  #'MOD_Grid_MOD15A2:Lai_1km'
parser.add_argument('input_folder', help='Input folder with TIFs')
parser.add_argument('output_folder', help='Where to store the results')
parser.add_argument('-ps','--pixel_size', help='Output resolution, pixels are square')
parser.add_argument('-s','--separate', help='Create layerstack if on')
args = parser.parse_args()

def sanitize():
    if not args.input_folder.endswith('\\'): args.input_folder = args.input_folder + '\\'
    if not args.output_folder.endswith('\\'): args.output_folder = args.output_folder + '\\'
    
    return args.input_folder,args.output_folder

if __name__ == '__main__':
    id,od = sanitize()

    fn = args.output        #filename.vrt or filename.tif
    os.chdir(id)

    tifs = glob.glob('*.tif')
    if len(tifs) == 0:
            print("Nothing to merge. Exiting.")
            sys.exit(1)
            
    list_of_tifs = ' '.join(tifs)

    if args.separate: 
        separate = '-separate'
    else:
        separate = ''

    if args.pixel_size:
        pix_size = '-ps ' + args.pixel_size + ' ' + args.pixel_size
    else:
        pix_size = ''


    if fn.split('.')[-1] == 'vrt': 
        pix_size = pix_size.replace('ps','tr')
        cmd = 'gdalbuildvrt' + separate + ' ' + pix_size + ' ' + ' -o ' + fn + ' ' + list_of_tifs
    else:
        cmd = 'gdal_merge ' + separate + ' ' + pix_size + ' ' + ' -o ' + od + fn + ' ' + list_of_tifs
        
    print cmd
    os.system(cmd)
