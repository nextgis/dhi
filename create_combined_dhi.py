#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# create_combined_dhi.py
# ---------------------------------------------------------
# Create combined DHI product
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      create_combined_dhi.py [-h] [-of1 OUTPUT_FOLDER1] [-s SUFFIX] input_folder output_folder2 product
#      where:
#           -h              show this help message and exit
#           input_folder    input folder
#           output_folder1  where to store TIFs for each time slice
#           output_folder2  where to store the combined result
#           suffix          suffix to end to resulting file name
#           product         product code used in folder name
# Example:
#      python create_combined_dhi.py -s fpar8 x:\MCD15A2\ x:\MCD15A2\combined\fpar8\ y:\dhi\global\fpar_8\combined-v2\ fpar
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
import glob
import time
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_folder', help='Input folder')
parser.add_argument('-of1','--output_folder1', help='Directory to store TIFs for each time slice')
parser.add_argument('output_folder2', help='where to store the combined result')
parser.add_argument('-s', '--suffix', help='suffix to end to resulting file name')
parser.add_argument('product', help='product code used in folder name')
args = parser.parse_args()

#prepare environment
gisbase = os.environ['GISBASE'] = "c:/tools/NextGIS_QGIS/apps/grass/grass-6.4.4/"
gisdbase = os.environ['GISDBASE'] = "e:/users/maxim/thematic/dhi/"
location = "dhi_grass"
mapset   = "PERMANENT"

sys.path.append(os.path.join(gisbase, "etc", "python"))
 
import grass.script as grass
import grass.script.setup as gsetup
gsetup.init(gisbase, gisdbase, location, mapset)

prefix = 'dhi'
os.chdir(args.input_folder)

years = range(2003,2014+1)
numslices = len(glob.glob(str(years[0]) + '/tif-' + args.product + '-qa/' + '*.tif'))

for year in years:
    i = 0
    for f in glob.glob(str(year) + '/tif-' + args.product + '-qa/' + '*.tif'):
        i+=1
        grass.run_command('r.in.gdal', input=f, output=str(year) + '_' + str(i))

#Calculate counts and medians for N time slices
for i in range(1,numslices+1):
    list = ''
    for year in years:
        list = list + ',' + str(year) + '_' + str(i)
    list = list.strip(',')
    
    grass.run_command('r.series', input=list, output=str(i) + '_cnt,' + str(i) + '_med', method='count,median')

#Filter out pixels where count is 3 and less
for i in range(1,numslices+1):
    grass.mapcalc(str(i) + '_f' ' = if(' + str(i) + '_cnt>3, ' + str(i) + '_med, null())')


#export averaged rasters
od1 = args.output_folder1
if args.output_folder1:
    for i in range(1,numslices+1):
        grass.run_command('r.out.gdal', input=str(i)+'_med', output=od1 + str(i) + '_med.tif', type='Byte', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES')
        grass.run_command('r.out.gdal', input=str(i)+'_avg', output=od1 + str(i) + '_avg.tif', type='Byte', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES')
        
        cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od1 + str(i) + '_med.tif'
        os.system(cmd)
        cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od1 + str(i) + '_avg.tif'
        os.system(cmd)
    
if not args.suffix: args.suffix = ''
fn_out = prefix + '_' + args.suffix + '_f.tif'

t = '_f'
list = ''
for i in range(1,numslices+1):
    list = list + ',' + str(i) + t
    
list = list.strip(',')

grass.run_command('r.series', input=list, output='dh1' + t + ',dh2' + t + ',ave' + t + ',std' + t, method='sum,minimum,average,stddev')
grass.mapcalc('dh3' + t + ' = std' + t + '/ave' + t)


grass.run_command('i.group', group='rgb_group' + t, input='dh1' + t + ',dh2' + t + ',dh3' + t)
grass.run_command('r.out.gdal', input='rgb_group' + t, output=fn_out, type='Float32', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES')
od2 = args.output_folder2
shutil.move(fn_out,od2 + fn_out)
shutil.move(fn_out + '.aux.xml',od + fn_out + '.aux.xml')

shutil.move(fn_out.replace('.tif','.tfw'),od2 + fn_out.replace('.tif','.tfw'))

cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od2 + fn_out
os.system(cmd)

