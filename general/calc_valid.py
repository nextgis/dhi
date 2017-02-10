#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# calc_valid.py
# ---------------------------------------------------------
# 'Good pixels' calculation script
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      calc_valid.py [-h] [-if INPUT_FOLDER] [-of OUTPUT_FOLDER] product
#      where:
#           -h                  show this help message and exit
#           -if INPUT_FOLDER    input_ folder
#           -of OUTPUT_FOLDER   input_ folder
#           product             product code used in folder name
# Example:
#      python calc_valid.py -if x:\MCD15A2\ -of x:\MCD15A2\valid\ fpar
#
# Copyright (C) 2015-2017 Maxim Dubinin (sim@gis-lab.info)
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
parser.add_argument('-if','--input_folder', help='Input folder')
parser.add_argument('-of','--output_folder', help='Directory to store TIFs for each time slice')
parser.add_argument('product', help='product code used in folder name')
args = parser.parse_args()

def sanitize():
    if not args.input_folder.endswith('\\'): args.input_folder = args.input_folder + '\\'
    if not args.output_folder.endswith('\\'): args.output_folder = args.output_folder + '\\'
    return args.input_folder,args.output_folder

if __name__ == '__main__':
    id,od = sanitize()
    
    #prepare environment
    gisbase = os.environ['GISBASE'] = "c:/OSGeo4W/apps/grass/grass-7.0.3/"
    # gisdbase = os.environ['GISDBASE'] = "e:/users/maxim/thematic/dhi/"
    gisdbase = os.environ['GISDBASE'] = "x:/"
    location = "dhi_grass"
    # mapset   = "gpp"
    mapset   = args.product

    sys.path.append(os.path.join(gisbase, "etc", "python"))
     
    import grass.script as grass
    import grass.script.setup as gsetup
    gsetup.init(gisbase, gisdbase, location, mapset)

    prefix = 'dhi'
    os.chdir(id)
    
    if 'fpar8' in args.product:
        args.product = str(args.product).replace('8','') 
        
    
    # grass.run_command('g.remove', type = 'rast', pat = '*', flags = 'f')
    # grass.run_command('g.remove', type = 'rast', name = '11_med')
    # grass.run_command('g.list', type = 'rast', pat = '*cnt*')
    # grass.run_command('g.list', type = 'rast')
    
    years = range(2003,2014+1)
    numslices = len(glob.glob(str(years[0]) + '/tif-' + args.product + '-qa-mask/' + '*.tif'))
    print 'Number of slices: %s ' % numslices

    workers = multi.cpu_count()
    if workers is 1 and "WORKERS" in os.environ:
        workers = int(os.environ["WORKERS"])
    if workers < 1:
        workers = 1
    
    workers = 30
    
    for year in years:
        proc = {}
        i = 0
        for f in glob.glob(str(year) + '/tif-' + args.product + '-qa-mask/' + '*.tif'):
            i+=1
            proc[i] = grass.start_command('r.in.gdal', input = f, output=str(year) + '_' + str(i), overwrite = True, memory = '50')
    
            if i % workers is 0:
                for j in range(workers):
                    proc[i - j].wait()
    
    
    workers = multi.cpu_count()
    proc = {}
    
    outf = file('tmp_reclass.txt', 'w')
    s = """
1 thru 3 = 0
4 thru 12 = 1
"""    
    outf.write(s)
    outf.close()
    
    #Calculate counts for N time slices and reclass rasters
    for i in range(1,numslices+1):
        list = ''
        for year in years:
            list = list + ',' + str(year) + '_' + str(i)
        list = list.strip(',')
        
        cnt = str(i) + '_cnt'
        
        # proc[i] = grass.start_command('r.series', input_= list, output = cnt, method='count', overwrite = True)
        
        # if i % workers is 0:
            # for j in range(workers):
                # proc[i - j].wait()

        recl = str(cnt) + '_recl'
        
        grass.run_command('r.reclass', input_ = cnt, output = recl, rules = 'tmp_reclass.txt', overwrite = True)
        
    os.remove('tmp_reclass.txt')
    
    sum_rast = '%s_cnt_sum' % args.product

    list = grass.read_command('g.list', type_ = 'rast', pattern = '*recl', sep = ',').strip()
    
    grass.run_command('r.series', input_= list, output = sum_rast, method='sum', overwrite = True)
    
    grass.run_command('r.null', map_= sum_rast, setnull = '0')
    
    #export sum raster
    od = args.output_folder
    if args.output_folder:
        tif = od + os.sep + sum_rast + '.tif'
        grass.run_command('r.out.gdal', input_ = sum_rast, output = tif, type='Byte', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES', flags = 'f', overwrite = True)
        
        cmd = "gdal_edit -a_srs \"+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +a=6371007.181 +b=6371007.181 +units=m +no_defs\" " + tif
        os.system(cmd)
