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
parser.add_argument('-rs','--input_rasters', help='Input GeoTIFF(s) separated by comma')
parser.add_argument('-if','--input_folder', help='Input folder with GeoTIFF(s)')
parser.add_argument('-of','--output_folder', help='Output folder, if missing input(s) will be overwritten')
parser.add_argument('-o','--overwrite', action="store_true", help='Overwrite outputs')

args = parser.parse_args()

def sanitize(folder):
    if not folder.endswith('\\'): folder = folder + '\\'
    return folder
    
if __name__ == '__main__':
    if not args.input_folder:
        print('Please select the input folder')
        sys.exit(1)
    
    od = ''
    if args.output_folder: od = sanitize(args.output_folder)
    
    if args.input_folder:
        id = sanitize(args.input_folder)
        os.chdir(args.input_folder)
        if args.input_rasters:
            inputs = args.input_rasters.split(',')
            inputs = [id + os.sep + x for x in inputs] 
        else:
            inputs = glob.glob(id + '*.tif')
    elif args.input_rasters and not args.input_folder:
        inputs = args.input_rasters.split(',')
    
    # gisbase = os.environ['GISBASE'] = "c:/OSGeo4W/apps/grass/grass-7.0.3/"
    # gisdbase = os.environ['GISDBASE'] = "e:/users/maxim/thematic/dhi/"
    # location = "dhi_grass"
    # mapset   = "gpp"

    # sys.path.append(os.path.join(gisbase, "etc", "python"))
     
    # import grass.script as grass
    # import grass.script.setup as gsetup
    # gsetup.init(gisbase, gisdbase, location, mapset)
    
    # grass.run_command('r.in.gdal', input_ = 'y:/dhi/masks/Fpar_NoData_sin.tif', output = 'Fpar_NoData_sin_b', overwrite = True)
    
    for input in inputs:
        if os.path.exists(input):
            input_name = os.path.basename(input).replace('.tif','')
            print('Processing ' + input)
            
            # grass.run_command('r.in.gdal', input_ = input, output = input_name, overwrite = True)
            # grass.mapcalc(input_name + '_0 = if(isnull(' + input_name + '),Fpar_NoData_sin_b,' + input_name + ')', overwrite = True)
            # grass.run_command('r.out.gdal', input_ = input_name + '_0', output = id + input_name + '_0.tif', overwrite = True)
            
            cmd = 'gdal_calc.py --overwrite ' + ' -A y:/dhi/masks/Fpar_NoData_sin_b_resize.tif ' + ' -B ' + input + ' --outfile=' + od + input_name + ' --calc="A*B"' + ' --NoDataValue=255'
            
            # cmd = 'gdal_calc.py --overwrite ' + ' -A y:/dhi/masks/Fpar_NoData_sin_b.tif ' + ' -B ' + id + input_name + '_0.tif' + ' --outfile=' + od + input_name + '.tif' + ' --calc="A*B"  --NoDataValue=255' + ' --overwrite'
            
            print cmd
            os.system(cmd)
            
            
