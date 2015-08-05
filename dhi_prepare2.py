#!/bin/env python
# -*- coding: utf-8 -*-

'''Prepare GeoTIFF data from MODIS HDFs for DHI calculation. To run:
   python dhi-prepare.py year leap
year - year for which data should be processed
band_number - order number of sds to import (starts with 1)
input_folder - where are input HDFs (this is folder of folders)
output_folder - where to store resulting TIFs
'''

import os
import glob
import sys
import calendar
    
if __name__ == '__main__':
    year = sys.argv[1]          #2003
    dataset_full = sys.argv[2]  #'MOD_Grid_MOD15A2:Lai_1km'
    id = sys.argv[3]
    od = sys.argv[4]
    
    script_path = 'e:/users/maxim/thematic/dhi/scripts/'
    os.chdir(id)
    dates = next(os.walk('.'))[1]
    
    for date in dates:
        
        cmd = 'python ' + script_path + 'hdf2tif.py ' + dataset_full + ' ' + id + date + '\\ ' + id + date + '\\'
        os.system(cmd)
        
        cmd = 'python ' + script_path + 'gdal-merge-all.py ' + date + '.vrt no 0 '  + id + date + '\\ ' + id + date + '\\'
        os.system(cmd)
        
        cmd = 'gdalwarp -t_srs EPSG:4326 -tr 0.0083 0.0083 ' + id + date + '\\' + date + '.vrt ' + od + date + '.tif'
        os.system(cmd)