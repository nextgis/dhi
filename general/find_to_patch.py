#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# find_to_patch.py
# ---------------------------------------------------------
# Find rasters that are needed to patch with the script <patch_raster.py> 
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      find_to_patch.py [-h] [-if INPUT_FOLDER] [-o OUTPUT_FILE] [-coor X,Y]
#      where:
#           -h                      Show this help message and exit
#           -if INPUT_FOLDER        Input folder of GeoTIFF rasters to be tested
#           -o OUTPUT_FILE          Output file with the list of rasters which needed to be patched
#           --coor                    Test coordinates
#
# Example:
#      python find_to_patch.py -if x:\MOD13A2\2003\tif-evi -of x:\MOD13A2\2003\tif-evi\rasters_to_patch.txt -coor -612944.369471 9098016.8692
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

import os
import argparse
import glob
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument('-if','--input_folder', help='Input folder of GeoTIFF rasters to be tested')
parser.add_argument('-of','--output_file', help='Output file with the list of rasters which needed to be patched')
parser.add_argument('-n','--nodata', help='Nodata value')
parser.add_argument('--coor', nargs=2, help="Test coordinates")
args = parser.parse_args()

def sanitize(folder):
    if not folder.endswith('\\'): folder = folder + '\\'
    return folder
    
if __name__ == '__main__':
    if args.input_folder: 
        inf = sanitize(args.input_folder)

    # print('\n' + 'Input folder: ' + inf + '\n')
    os.chdir(inf)

    # if not args.output_file:
        # args.output_file = os.path.join(args.input_folder, 'rasters_to_patch.txt')
    
    if args.output_file:
        print('Output file: ' + args.output_file + '\n')
        if os.path.exists(args.output_file):
            os.remove(args.output_file)

    coords = " ".join(map(str,args.coor))
        
    tifs = glob.glob('*.tif')
    
    tiflist = []
    for tif in tifs:
        cmd = 'gdallocationinfo -valonly -geoloc ' + tif + ' ' + coords
        val = subprocess.check_output(cmd, shell=True).rsplit()
        
        # if val == ['0']:
        if args.nodata in val or not val or val == ['0']:
        # if args.nodata in val or not val:
            if not args.output_file:
                print('%s' % tif) + '==>' + ('%s' % val)
                # print(tif + ' need to be patched')
                tiflist.append(tif)
            else:
                with open(args.output_file, 'w') as outfile:
                    outfile.write(tif+',')
    
    # if len(tiflist) > 0:  
        # print ",".join(map(str,tiflist))
    
    # if args.output_file:
        # try:
            # with open(args.output_file, 'r+') as outfile:
                # line = outfile.read()[:-1]
                # outfile.seek(0)
                # outfile.write(line)
                # outfile.truncate()
        # except IOError as err:
            # print err.errno 
            # print err.strerror