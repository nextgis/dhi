#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# prepare_data.py
# ---------------------------------------------------------
# Wrapper script that runs other scripts. Converts all HDFs to TIFs (hdf2tif.py), mosaics them all together (merge_all.py) and reprojects to EPSG:4326 or needed.
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      prepare_data.py dataset x:\MCD15A2\2003\hdf\ x:\MCD15A2\2003\tif-fpar\ 0.0083 epsg
#      where:
#           dataset         SDS name of the dataset to process
#           input_folder    input folder with HDFs (this is folder of folders)
#           output_folder   where result will be stored
#           pixel_size      pixel size, pixels are square
#           epsg            EPSG code for output file or "no" for default
# Examples:
#      python prepare_data.py 2003 MOD_Grid_MOD15A2:Fpar_1km x:\MCD15A2\2003\hdf\ x:\MCD15A2\2003\tif-fpar\before-nodata\ 0.0083 4326
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
import glob
import sys
import calendar
    
if __name__ == '__main__':
    dataset = sys.argv[1]  #'MOD_Grid_MOD15A2:Lai_1km'
    id = sys.argv[2]
    od = sys.argv[3]
    res = sys.argv[4]
    epsg = sys.argv[5]     #4326, 'no'
    
    script_path = 'e:/users/maxim/thematic/dhi/scripts/'
    os.chdir(id)
    dates = next(os.walk('.'))[1]
    
    if epsg == 'no':
        epsg = ''
    else:
        epsg = '-t_srs EPSG:' + epsg
    
    for date in dates:
        
        cmd = 'python ' + script_path + 'hdf2tif.py ' + dataset.split(':')[0] + ':' + '\"' + dataset.split(':')[1] + '\" ' + id + date + '\\ ' + id + date + '\\'
        #print(cmd)
        os.system(cmd)
        
        if not os.path.exists(date + '.vrt'):
            cmd = 'python ' + script_path + 'merge_all.py ' + date + '.vrt no 0 '  + id + date + '\\ ' + id + date + '\\'
            os.system(cmd)
        
        if not os.path.exists(od + date + '.tif'):
            cmd = 'gdalwarp ' + epsg + ' -tr ' + res + ' ' + res + ' ' + id + date + '\\' + date + '.vrt ' + od + date + '.tif'
            os.system(cmd)
        