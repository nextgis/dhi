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
#           input_folder    input_ folder
#           output_folder1  where to store TIFs for each time slice
#           output_folder2  where to store the combined result
#           suffix          suffix to end to resulting file name
#           product         product code used in folder name
# Example:
#      python create_combined_dhi.py -s fpar8 x:\MCD15A2\ -of1 x:\MCD15A2\combined\fpar8\ y:\dhi\global\fpar_8\combined-v2\ fpar
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

import multiprocessing as multi

parser = argparse.ArgumentParser()
parser.add_argument('input_folder', help='Input folder')
parser.add_argument('-of1','--output_folder1', help='Directory to store TIFs for each time slice')
parser.add_argument('-of2','--output_folder2', help='where to store the combined result')
parser.add_argument('-s', '--suffix', help='suffix to end to resulting file name')
parser.add_argument('product', help='product code used in folder name')
args = parser.parse_args()

def sanitize():
    if not args.input_folder.endswith('\\'): args.input_folder = args.input_folder + '\\'
    if not args.output_folder2.endswith('\\'): args.output_folder2 = args.output_folder2 + '\\'
    return args.input_folder,args.output_folder2

if __name__ == '__main__':
    id,od2 = sanitize()
    
    #prepare environment
    # gisbase = os.environ['GISBASE'] = "c:/tools/NextGIS_QGIS/apps/grass/grass-6.4.4/"
    gisbase = os.environ['GISBASE'] = "c:/OSGeo4W/apps/grass/grass-7.0.3/"
    # gisdbase = os.environ['GISDBASE'] = "e:/users/maxim/thematic/dhi/"
    gisdbase = os.environ['GISDBASE'] = "x:/"
    location = "dhi_grass"
    # mapset   = "gpp"
    mapset   = args.product
    if args.product == 'fpar':
        mapset = 'fpar8'
    if args.product == 'lai':
        mapset = 'lai8'
 
    sys.path.append(os.path.join(gisbase, "etc", "python"))
     
    import grass.script as grass
    import grass.script.setup as gsetup
    gsetup.init(gisbase, gisdbase, location, mapset)

    prefix = 'dhi'
    os.chdir(id)

    
    
    # # grass.run_command('g.remove', type = 'rast', pat = '*', flags = 'f')
    # # grass.run_command('g.remove', type = 'rast', name = '11_med')
    # grass.run_command('g.list', type = 'rast')
    
    years = range(2003,2014+1)
    numslices = len(glob.glob(str(years[0]) + '/tif-' + args.product + '-qa/' + '*.tif'))
    # numslices = len(glob.glob(str(years[0]) + '/tif-' + args.product + '-qa-mask/' + '*.tif'))
    print(numslices)

    
    workers = multi.cpu_count()
    # workers = 1
    if workers is 1 and "WORKERS" in os.environ:
        workers = int(os.environ["WORKERS"])
    if workers < 1:
        workers = 1
            
    proc = {}
    
    # global nuldev
    # nuldev = file(os.devnull, 'w')
   
    
    for year in years:
        i = 0
        # for f in glob.glob(str(year) + '/tif-' + args.product + '-qa-mask/' + '*.tif'):
        for f in glob.glob(str(year) + '/tif-' + args.product + '-qa/' + '*.tif'):
            i += 1
            proc[i] = grass.start_command('r.in.gdal', input_ = f, output=str(year) + '_' + str(i), overwrite = True)
            # grass.run_command('r.in.gdal', input_ = f, output=str(year) + '_' + str(i))
            
            # try:
                # grass.run_command('r.info', map_ = str(year) + '_' + str(i), quiet = True, stdout = nuldev)
            # except:
                # print (str(year) + '_' + str(i)) + ' is not found' 
                # grass.run_command('r.in.gdal', input_ = f, output=str(year) + '_' + str(i), overwrite = True)
            
            if i % workers is 0:
                for j in range(workers):
                    proc[i - j].wait()
    
    
    
    #Calculate counts and medians for N time slices
    for i in range(1,numslices+1):
        list = ''
        for year in years:
            list = list + ',' + str(year) + '_' + str(i)
        list = list.strip(',')
        
        cnt = str(i) + '_cnt'
        med = str(i) + '_med'
        
        proc[i] = grass.start_command('r.series', input_=list, output=str(i) + '_cnt,' + str(i) + '_med',   method='count,median', overwrite = True)
        
        if i % workers is 0:
                for j in range(workers):
                    proc[i - j].wait()
    
    #Filter out pixels where count is 3 and less
    for i in range(1,numslices+1):
        grass.mapcalc(str(i) + '_f' ' = if(' + str(i) + '_cnt>3, ' + str(i) + '_med, null())', overwrite = True)
        
    proc = {}  
        
    #export averaged rasters
    od1 = args.output_folder1
    if args.output_folder1:
        for i in range(1,numslices+1):
            proc[i] = grass.start_command('r.out.gdal', input_=str(i)+'_med', output=od1 + str(i) + '_med.tif', type='Byte', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES', flags = 'f', overwrite = True)
            
            if i % workers is 0:
                for j in range(workers):
                    proc[i - j].wait()
    
            
            cmd = "gdal_edit -a_srs \"+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs\" " + od1 + str(i) + '_med.tif'
            os.system(cmd)
        
    if not args.suffix: args.suffix = ''
    fn_out = prefix + '_' + args.suffix + '_f.tif'

    t = '_f'
    list = ''
    
    years = range(2003,2014+1)
    numslices = len(glob.glob(str(years[0]) + '/tif-' + args.product + '-qa/' + '*.tif'))
    # print(numslices)
    
    for i in range(1,numslices+1):
        list = list + ',' + str(i) + t
        
    list = list.strip(',')

    grass.run_command('r.series', input_=list, output='dh1' + t + ',dh2' + t + ',ave' + t + ',std' + t, method='sum,minimum,average,stddev')
    grass.mapcalc(('dh3' + t + ' = std' + t + '/ave' + t), overwrite = True)
    
    # Need for 0 / null stuff
    grass.mapcalc("$dh3_new = if(isnull($dh3)&&($dh2==0),$dh2,$dh3)", dh3_new = 'dh3' + t + '2', dh3 = 'dh3' + t, dh2 = 'dh2' + t)
    grass.run_command('g.rename', raster =('dh3' + t + '2', 'dh3' + t ), overwrite = True)
    
    grass.run_command('g.remove', type_ = 'group', name = 'rgb_group' + t, flags = 'f')
    grass.run_command('i.group', group='rgb_group' + t, input_='dh1' + t + ',dh2' + t + ',dh3' + t)
    grass.run_command('r.out.gdal', input_='rgb_group' + t, output=fn_out, type='Float32', flags = 'f', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES',  overwrite = True)
    shutil.move(fn_out,od2 + fn_out)
    shutil.move(fn_out + '.aux.xml',od2 + fn_out + '.aux.xml')
    shutil.move(fn_out.replace('.tif','.tfw'),od2 + fn_out.replace('.tif','.tfw'))

    cmd = "gdal_edit -a_srs \"+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs\" " + od2 + fn_out
    os.system(cmd)

