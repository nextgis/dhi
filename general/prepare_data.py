#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# prepare_data.py
# ---------------------------------------------------------
# Wrapper script that runs other scripts. Converts all HDFs to TIFs (hdf2tif.py), mosaics them all together (merge_all.py) and reprojects to EPSG:4326 or needed.
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      prepare_data.py [-h] [-ps PIXEL_SIZE] [-e EPSG] dataset input_folder output_folder
#      where:
#           -h              show this help message and exit
#           dataset         SDS name of the dataset to process
#           input_folder    input folder with HDFs (this is folder of folders)
#           output_folder   where result will be stored
#           pixel_size      Output resolution, pixels are square
#           epsg            EPSG code for output file, EPSG:4326 if empty
# Examples:
#      python prepare_data.py MOD_Grid_MOD15A2:Fpar_1km x:\MCD15A2\2003\hdf\ x:\MCD15A2\2003\tif-fpar\ -ps 0.0083 -e 4326
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
import glob
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('dataset', help='SDS name of the dataset to process')  #'MOD_Grid_MOD15A2:Lai_1km'
parser.add_argument('input_folder', help='Input folder with HDFs (this is folder of folders)')
parser.add_argument('output_folder', help='Where to store the results')
parser.add_argument('-ps','--pixel_size', help='Output resolution, pixels are square')
parser.add_argument('-e','--epsg', help='EPSG code for output file, EPSG:4326 if empty, sinusoidal (no resampling) if SIN')
args = parser.parse_args()
    
if __name__ == '__main__':
    id = args.input_folder
    script_path = os.getcwd() + '\\'
    
    os.chdir(id)
    dates = next(os.walk('.'))[1]
    
    if args.epsg:
        epsg = '-t_srs EPSG:' + args.epsg
    else:
        epsg = '-t_srs EPSG:4326'
    
    if args.pixel_size:
        pixel_size = ' -tr ' + args.pixel_size + ' ' + args.pixel_size
    else:
        pixel_size = ''
    
    for date in dates:
        cmd = 'python ' + script_path + 'hdf2tif.py ' + args.dataset.split(':')[0] + ':' + '\"' + args.dataset.split(':')[1] + '\" ' + id + date + '\\'
        #print(cmd)
        os.system(cmd)
        
        if not os.path.exists(id + date + '\\' + date + '.vrt'):
            cmd = 'python ' + script_path + 'merge_all.py ' + date + '.vrt '  + id + date + '\\ ' + id + date + '\\ '
            os.system(cmd)
        
        if not os.path.exists(args.output_folder + date + '.tif') and os.path.exists(id + date + '\\' + date + '.vrt'):
            if args.epsg != 'SIN':
                cmd = 'gdalwarp ' + epsg + pixel_size + ' ' + id + date + '\\' + date + '.vrt ' + args.output_folder + date + '.tif'
            else:
                if args.pixel_size:
                    cmd = 'gdalwarp ' + pixel_size + ' ' + id + date + '\\' + date + '.vrt ' + args.output_folder + date + '.tif'
                else:
                    cmd = 'gdal_translate ' + id + date + '\\' + date + '.vrt ' + args.output_folder + date + '.tif'
            os.system(cmd)
        