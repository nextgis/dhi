#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# qa_all.py
# ---------------------------------------------------------
# Apply QA rasters to DATA rasters to produce patched versions
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      qa_all.py [-h] [-s SKIP_MASKS] input_dir_qa input_dir_rs output_dir
#      where:
#           -h              show this help message and exit
#           input_dir_qa    directory with input QA rasters
#           input_dir_rs    directory with input rasters to apply QA to
#           output_dir      directory where patched rasters will be stored
#           -s              skip creation of binary masks if they exist to reuse them (yes/no)
#           -o,overwrite    overwrite output files
# Example:
#      python qa_all.py -iq x:\MOD17A2\2003\tif-gpp\qa\ -ir x:\MOD17A2\2003\tif-gpp\ -o x:\MOD17A2\2003\tif-gpp-qa\ -s yes
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
parser.add_argument('input_dir_qa', help='Directory with input QA rasters')
parser.add_argument('input_dir_rs', help='Directory with input rasters to apply QA to')
parser.add_argument('output_dir', help='Directory where patched rasters will be stored')
parser.add_argument('-s','--skip_masks', action="store_true", help='Skip creation of binary masks if they exist')
parser.add_argument('-o','--overwrite', action="store_true", help='Overwrite outputs')
args = parser.parse_args()

def sanitize():
    if not args.input_dir_qa.endswith('\\'): args.input_dir_qa = args.input_dir_qa + '\\'
    if not args.input_dir_rs.endswith('\\'): args.input_dir_rs = args.input_dir_rs + '\\'
    if not args.output_dir.endswith('\\'): args.output_dir = args.output_dir + '\\'
    
    return args.input_dir_qa,args.input_dir_rs,args.output_dir

if __name__ == '__main__':
    id_qa,id_rs,od = sanitize()
    
    wd = os.getcwd()

    os.chdir(id_qa)

    # tifs = glob.glob('*.tif')
    tifs = glob.glob('2015.12.[1|2][1|7|9].tif')
    # tifs = glob.glob('2015.12.27.tif')

    for tif in tifs:
        if '_b.tif' not in tif:
            if not os.path.exists(tif.replace('.tif','_b.tif')) or not args.skip_masks:
                # cmd = 'gdal_calc.py -A ' + tif + ' --outfile=' + tif.replace('.tif','_b.tif') + ' --calc="1*(A<157) +255*(A==157)" --NoDataValue=255' +  ' --overwrite'
                cmd = 'gdal_calc.bat -A ' + tif + ' --outfile=' + tif.replace('.tif','_b.tif') + ' --calc="1*(logical_or(A<84,A==157)) + 255*(logical_and(A>84,A<157))" --NoDataValue=255' +  ' --overwrite'
                
                print cmd
                os.system(cmd)
                # pass
            
            if not os.path.exists(od + tif) or args.overwrite:
                cmd = 'gdal_calc.py --overwrite -A ' + tif.replace('.tif','_b.tif') + ' -B ' + id_rs + tif + ' --outfile=' + od + tif + ' --calc="A*B" --NoDataValue=255'
                
                print cmd
                os.system(cmd)
            elif os.path.exists(od + tif) and not args.overwrite:
                print('Output exists and overwrite is off, skipping')
            