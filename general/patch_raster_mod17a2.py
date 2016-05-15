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
import random

parser = argparse.ArgumentParser()
parser.add_argument('-rs','--input_rasters', help='Input GeoTIFF(s) separated by comma')
parser.add_argument('-if','--input_folder', help='Input folder with GeoTIFF(s)')
parser.add_argument('-pl','--patch_list', help='File with the list of GeoTIFF(s) which are needed to be patched')
parser.add_argument('-of','--output_folder', help='Output folder, if missing input(s) will be overwritten')
parser.add_argument('-t','--template', help='Template raster')
parser.add_argument('-v','--value', help='Maximum meaningful value')
parser.add_argument('-n','--nodata', help='Nodata value')
parser.add_argument('-o','--overwrite', action="store_true", help='Overwrite outputs')

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
        os.chdir(args.input_folder)
        if args.input_rasters:
            inputs = args.input_rasters.split(',')
        else:
            inputs = glob.glob(id + '*.tif')
        if args.patch_list:
            os.chdir(args.input_folder)
            with open(args.patch_list, 'r') as infile:
                inputs = infile.read().split(',')    
        
    if args.input_rasters:
        inputs = args.input_rasters.split(',')
        
    inputs = [id + x for x in inputs] 
                
    #create mask from template
    print('Preparing mask from ' + args.template)
    
    if args.input_folder:
        temp1 = id + str(random.randrange(1, 999)) + 'temp1.tif'
        mask = id + str(random.randrange(1, 999)) + 'mask.tif'
    else:
        temp1 = str(random.randrange(1, 999)) + 'temp1.tif'
        mask = str(random.randrange(1, 999)) + 'mask.tif'
    
    # cmd1 = 'gdalwarp -srcnodata ' + args.value + ' -dstnodata ' + args.nodata + ' ' + args.template + ' ' + temp1 + ' --config GDAL_CACHEMAX 500 -wm 500 ' + ' -overwrite'
    cmd1 = 'gdalwarp -srcnodata ' + args.value + ' -dstnodata ' + args.nodata + ' ' + args.template + ' ' + temp1 + ' -overwrite'
    
    cmd2 = 'gdal_calc.py -A ' + temp1 + ' --outfile=' + mask + ' --calc="A*(A>' + args.value + ')" --NoDataValue=' + args.nodata + ' --overwrite'
    
    print(cmd1)
    os.system(cmd1)
    print(cmd2)
    os.system(cmd2)
    
    for input in inputs:
        if os.path.exists(input):
            input_name = os.path.basename(input)
            print('Processing ' + input)
            
            ### apply input raster over mask
            if args.input_folder:
                temp2 = id + str(random.randrange(1, 999)) + 'temp2.tif'
            else:
                temp2 = str(random.randrange(1, 999)) + 'temp2.tif'
            # cmd1 = 'gdalwarp -srcnodata ' + args.value + ' -dstnodata ' + args.nodata + ' ' + input + ' ' + temp2 + ' --config GDAL_CACHEMAX 500 -wm 500' + ' -overwrite'
            cmd1 = 'gdalwarp -srcnodata ' + args.value + ' -dstnodata ' + args.nodata + ' ' + input + ' ' + temp2 +  ' -overwrite' + ' --config GDAL_CACHEMAX 500 -wm 500'
            
            print(cmd1)
            os.system(cmd1)
            
            if 'qa' in input:
                if args.input_folder:
                    temp2qa = id + str(random.randrange(1, 999)) + 'temp2qa.tif'
                else:
                    temp2qa = str(random.randrange(1, 999)) + 'temp2qa.tif'
                    
                cmd = 'gdalwarp -srcnodata 0' + ' -dstnodata ' + args.nodata + ' ' + temp2 + ' ' + temp2qa + ' --config GDAL_CACHEMAX 500 -wm 500' + ' -overwrite'
                print(cmd)
                os.system(cmd)
                shutil.move(temp2qa,temp2)
            
            if args.input_folder:
                merge = id + str(random.randrange(1, 999)) + 'merge.tif'
                out = id + str(random.randrange(1, 999)) + 'out.tif'
            else:
                merge = str(random.randrange(1, 999)) + 'merge.tif'
                out = str(random.randrange(1, 999)) + 'out.tif'
            
            # cmd2 = 'gdalwarp ' + mask + ' ' + temp2 + ' ' + merge + ' -srcnodata ' + args.nodata + ' -dstnodata ' + args.nodata + ' --config GDAL_CACHEMAX 500 -wm 500' + ' -overwrite'
            cmd2 = 'gdalwarp ' + mask + ' ' + temp2 + ' ' + merge + ' -srcnodata ' + args.nodata + ' -dstnodata ' + args.nodata + ' -overwrite'
            
            cmd3 = 'gdal_calc -A ' + merge + ' --outfile=' + out + ' --calc="A*(A<' + args.value + ')" --NoDataValue=' + args.nodata
           
            print(cmd2)
            os.system(cmd2)
            print(cmd3)
            os.system(cmd3)
            
            os.remove('%s' % temp1)
            os.remove('%s' % temp2)
             
            if args.output_folder:
                shutil.move(out,od + input_name)
            else:
                shutil.move(out,input)
            os.remove('%s' % merge)
            
        else:
            print('File %s doesn\'t exist. Skipping...'%input)
            
os.remove('%s' % mask)