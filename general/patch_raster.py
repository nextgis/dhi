#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# patch_raster.py
# ---------------------------------------------------------
# Apply raster B to raster A to add 0 where raster A values are nodata or missing (but exist in raster B)
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      patch_raster.py [-h] [-o OUTPUT_FOLDER] (-rs INPUT_RASTERS | -if INPUT_FOLDER) template value
#      where:
#           -h                      show this help message and exit
#           -rs INPUT_RASTERS       input GeoTIFF rasters to be patched, separated by comma
#           -if INPUT_FOLDER        input folder of GeoTIFF rasters to be patched
#           -o OUTPUT_FOLDER        output folder, if missing input will be overwritten
#           template                template raster
#           value                   Maximum meaningful value
# Example:
#      python patch_raster.py input.tif -o output.tif template.tif
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
import argparse
import glob

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-rs','--input_rasters', help='Input GeoTIFF(s) separated by comma')
group.add_argument('-if','--input_folder', help='Input folder with GeoTIFF(s)')
parser.add_argument('-pl','--patch_list', help='File with the list of GeoTIFF(s) which are needed to be patched')
parser.add_argument('-of','--output_folder', help='Output folder, if missing input(s) will be overwritten')
parser.add_argument('-t','--template', help='Template raster')
parser.add_argument('-v','--value', help='Maximum meaningful value')


args = parser.parse_args()

def sanitize(folder):
    if not folder.endswith('\\'): folder = folder + '\\'
    return folder
    
if __name__ == '__main__':
    if args.patch_list and not args.input_folder:
        print('Please select the input folder')
        sys.exit(1)
    if args.patch_list and args.input_rasters:
        print('Please select either input rasters OR the patch list file')
        sys.exit(1)
    
    od = ''
    if args.output_folder: od = sanitize(args.output_folder)
    if args.input_folder: 
        id = sanitize(args.input_folder)
        inputs = glob.glob(id + '*.tif')
    else:
        inputs = args.input_rasters.split(',')
    if args.input_folder and args.patch_list:
        os.chdir(args.input_folder)
        with open(args.patch_list, 'r') as infile:
            inputs = infile.read().split(',')
    
    #create mask from template
    print('Preparing mask from ' + args.template)
        
    cmd = 'gdal_calc.py -A ' + args.template  + ' --outfile=mask.tif ' + ' --calc="A*(A>=' + args.value + ')'
    
    os.system(cmd)
    
    for input in inputs:
        if os.path.exists(input):
            input_name = os.path.basename(input)
            
            print('Processing ' + input)
            
            #apply input raster over mask
                        
            cmd = 'gdalwarp' + ' mask.tif ' + input + ' merge.tif' + ' -srcnodata -3000 ' + ' --config GDAL_CACHEMAX 1000 -wm 500'
            
            os.system(cmd)
            
            #calculate to drop nodata to 0
            #gdal_calc -A !merge1.tif -B 2003.07.20.tif --outfile=!res.tif --calc="A*(A<255) +  A*(logical_and(B==255,A<>255)) + 0*(logical_and(A==255,B<>255))"
                        
            cmd = 'gdal_calc.py -A merge.tif -B ' + args.template + ' --outfile=out.tif ' + ' --calc="A*(A<' + args.value + ')'
            
            os.system(cmd)
            
            if args.output_folder:
                shutil.move('out.tif',od + input_name)
            else:
                shutil.move('out.tif',input)
            os.remove('merge.tif')
        else:
            print('File %s doesn\'t exist. Skipping...'%input)
            
os.remove('mask.tif')