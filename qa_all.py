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
#      qa_all.py [-h] [-iq INPUT_DIR_QA] [-ir INPUT_DIR_RS] [-o OUTPUT_DIR] [-s SKIP_MASKS]
#      where:
#           -h   show this help message and exit
#           -iq  directory with input QA rasters
#           -ir  directory with input rasters to apply QA to
#           -o   directory where patched rasters will be stored
#           -s   Skip creation of binary masks if they exist to reuse them (yes/no)
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
parser.add_argument('-iq','--input_dir_qa', help='Directory with input QA rasters')
parser.add_argument('-ir','--input_dir_rs', help='Directory with input rasters to apply QA to')
parser.add_argument('-o','--output_dir', help='Directory where patched rasters will be stored')
parser.add_argument('-s','--skip_masks', help='Skip creation of binary masks if they exist (yes/no)')

args = parser.parse_args()

wd = os.getcwd()

id_qa = args.input_dir_qa
id_rs = args.input_dir_rs
od = args.output_dir

os.chdir(id_qa)

tifs = glob.glob('*.tif')

for tif in tifs:
    if '_b.tif' not in tif:
        if args.skip_masks == "no":
            #cmd = 'gdal_calc.bat -A ' + tif + ' --outfile=' + tif.replace('.tif','_b.tif') + ' --calc="1*(A<50)" --NoDataValue=0'
            cmd = 'gdal_calc.bat -A ' + tif + ' --outfile=' + tif.replace('.tif','_b.tif') + ' --calc="1*(A<4097) + 1*(logical_and(A>=18433,A<=19946)) + 1*(logical_and(A>=34817,A<=36334))+ 1*(logical_and(A>=51201,A<=52721))" --NoDataValue=0'
            print cmd
            os.system(cmd)
            
        cmd = 'gdal_calc.bat --overwrite -A ' + tif.replace('.tif','_b.tif') + ' -B ' + id_rs + tif + ' --outfile=' + od + tif + ' --calc="A*B" --NoDataValue=0'
        print cmd
        os.system(cmd)
        