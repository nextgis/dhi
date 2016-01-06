#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# landcovers_majority.py
# ---------------------------------------------------------
# Calculate stable landcovers, i.e. landcovers that never changed during whole time period
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      landcovers_majority.py input_folder suffix final_name numclasses
#      where:
#           -h              show this help message and exit
#           input_folder    input folder with HDFs
#           output          output file with path
#           suffix          subdataset code (use gdalinfo to get it)
#           numclasses      number of classes in this landcover
# Examples:
#      python landcovers_majority.py y:\landcover\global\fpar-lai\ majority_landcovers.tif fpar 11
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
import string
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_folder', help='Input folder with TIFs')
parser.add_argument('output', help='Output file with path')
parser.add_argument('suffix', help='Product')
parser.add_argument('numclasses', help='Number of classes in this landcover', type=int)
args = parser.parse_args()

def sanitize():
    if not args.input_folder.endswith('\\'): args.input_folder = args.input_folder + '\\'
    
    return args.input_folder

if __name__ == '__main__':
    id = sanitize()

    os.chdir(id)
    startyear = 2003
    endyear = 2012

    #separate each landcover year into binary masks
    numclasses = args.numclasses
    numyears = len(range(startyear,endyear+1))

    for c in range(0, numclasses + 1):
        for year in range(startyear,endyear+1):
            year = 'lc_' + str(year) + '_' + args.suffix + '.tif'
            year_c = year.replace('.tif','_' + str(c) + '.tif')
            cmd = 'gdal_calc --overwrite -A ' + year + ' --outfile=' + year_c + ' --calc="1*(A==' + str(c) + ')"'
            print(cmd)
            os.system(cmd)

    #sum them all up
    for c in range(numclasses + 1):
        i=0
        inputs = ''
        strsum = ''
        for year in glob.glob('*_' + str(c) + '.tif'):
            inputs = inputs + '-' + string.uppercase[i] + ' ' + year + ' '
            strsum = strsum + string.uppercase[i] + '+'
            i+=1
        
        inputs = inputs.rstrip(' ')
        strsum = strsum.rstrip('+')
        cmd = 'gdal_calc --overwrite ' + inputs + ' --outfile=' + str(c) + '_sum.tif ' + '--calc="(' + strsum + ')"'
        print(cmd)
        os.system(cmd)

    #recalculate to class value if numyears, for 0 recalc to 100
    c = 0
    cmd = 'gdal_calc --overwrite -A 0_sum.tif --outfile=0_stable.tif --calc="100*(A>5)" --NoDataValue=0'
    print(cmd)
    os.system(cmd)

    for c in range(1,numclasses + 1):
        cmd = 'gdal_calc --overwrite -A ' + str(c) + '_sum.tif ' + '--outfile=' + str(c) + '_stable.tif ' + ' --calc="'+ str(c) + '*(A>5)" --NoDataValue=0'
        print(cmd)
        os.system(cmd)

    #remove nodata=0
    for c in range(numclasses + 1):
        cmd = 'gdal_translate -a_nodata none ' + str(c) + '_stable.tif ' + str(c) + '_stable1.tif '
        print(cmd)
        os.system(cmd)

    #sum rasters back together
    inputs = ''
    strsum = ''
    for c in range(numclasses + 1):
        inputs = inputs + '-' + string.uppercase[c] + ' ' + str(c) + '_stable1.tif '
        strsum = strsum + string.uppercase[c] + '+'
        
    inputs = inputs.rstrip(' ')
    strsum = strsum.rstrip('+')
    cmd = 'gdal_calc --overwrite ' + inputs + ' --outfile=sum.tif ' + '--calc="(' + strsum + ')"'
    os.system(cmd)

    #recalc 100 back to 0

    cmd = 'gdal_calc --overwrite -A sum.tif --outfile=_res.tif --calc="255*(A==0)+0*(A==100)+A*(A<100)" --NoDataValue=255'
    os.system(cmd)

    #assign colortable
    cmd = 'python e:/users/maxim/thematic/dhi/scripts/add_colortable.py _res.tif ' + agrs.output + ' e:/users/maxim/thematic/dhi/scripts/colortables/' + suffix + '.txt'
    os.system(cmd)

    #clean up
    if os.path.exists(agrs.output):
        for c in range(numclasses + 1):
            os.remove(str(c) + '_sum.tif')
            os.remove(str(c) + '_stable.tif')
            os.remove(str(c) + '_stable1.tif')
            for year in range(startyear,endyear+1):
                year = 'lc_' + str(year) + '_' + suffix + '.tif'
                year_c = year.replace('.tif','_' + str(c) + '.tif')
                os.remove(year_c)
            
    os.remove('sum.tif')
    os.remove('_res.tif')
