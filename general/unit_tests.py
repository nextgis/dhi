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
parser.add_argument('-rs','--input_rasters', help='Input GeoTIFF(s) separated by comma')
parser.add_argument('-if','--input_folder', help='Input folder with GeoTIFF(s)')
args = parser.parse_args()

def sanitize(folder):
    if not folder.endswith('\\'): folder = folder + '\\'
    return folder

def test(i,x):
    if x != correct_values[i]:
        print("Test failed. Expected: %s, got: %s. Continue? [Y/N]" % (correct_values[i],x))
        choice = raw_input().lower()
        if choice not in set(['yes','y', 'ye', '']):
            sys.exit()
    
if __name__ == '__main__':
    if args.input_folder:
        id = sanitize(args.input_folder)
        os.chdir(args.input_folder)
        if args.input_rasters:
            inputs = args.input_rasters.split(',')
            inputs = [id + x for x in inputs]
        else:
            inputs = glob.glob(id + '*.tif')
    else:
        inputs = args.input_rasters.split(',')
        
    # print inputs


    ## MAKE TESTS ##
    
    coords = {
            'data': '3048626.22047 5464238.58633', 
            'patch': '2809283.46018 8371634.55813',
            'city': '2354412.22137 6199867.96243', 
            'sea': '2879839.13164 4854666.74599', 
            'water': '2245015.49646 6497925.47104', 
            'desert': '-132908.181906 2481548.63916'
    }
    
    # print coords['data']
    
    # values = {
            # 'data': ['3048626.22047 5464238.58633'], 
            # 'patch': ['2809283.46018 8371634.55813'],
            # 'city': ['2354412.22137 6199867.96243'], 
            # 'sea': ['2879839.13164 4854666.74599'], 
            # 'water': ['2245015.49646 6497925.47104'], 
            # 'desert': ['-132908.181906 2481548.63916']
    # }
    
    # tiflist = []
    
    # for coor in coords.itervalues():
    for item in coords.iteritems():
        place = item[0]
        coor = item[1]
        
        for tif in inputs:
            cmd = 'gdallocationinfo -valonly -geoloc ' + tif + ' ' + coor
            val = subprocess.check_output(cmd, shell=True).rsplit()
            # if val == ['-1.#IND', '-1.#IND', '-1.#IND']:
            # if not val or val == ['0']:
            print tif + '  -->  ' + place  + '  -->  ' + str(val)
                # # print(tif + ' need to be patched')
                # tiflist.append(tif)
    
