#!/bin/env python
# -*- coding: utf-8 -*-

'''Prepare GeoTIFF data from MODIS HDFs for DHI calculation. To run:
   python dhi_prepare2.py 2003 MOD_Grid_MOD15A2:Fpar_1km x:\MCD15A2\2003\hdf\ x:\MCD15A2\2003\tif-fpar\before-nodata\ 0.0083 4326
year - year for which data should be processed
band_number - order number of sds to import (starts with 1)
input_folder - where are input HDFs (this is folder of folders)
output_folder - where to store resulting TIFs
res - resolution
epsg - code for reprojection, 'no' for no reprojection
'''

import os
import glob
import sys
import calendar
    
if __name__ == '__main__':
    year = sys.argv[1]          #2003
    dataset = sys.argv[2]  #'MOD_Grid_MOD15A2:Lai_1km'
    id = sys.argv[3]
    od = sys.argv[4]
    res = sys.argv[5]
    epsg = sys.argv[6]  #4326, 'no'
    
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
            cmd = 'python ' + script_path + 'gdal-merge-all.py ' + date + '.vrt no 0 '  + id + date + '\\ ' + id + date + '\\'
            os.system(cmd)
        
        if not os.path.exists(od + date + '.tif'):
            cmd = 'gdalwarp ' + epsg + ' -tr ' + res + ' ' + res + ' ' + id + date + '\\' + date + '.vrt ' + od + date + '.tif'
            os.system(cmd)
        