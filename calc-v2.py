#!/bin/env python
# -*- coding: utf-8 -*-

'''Prepare GeoTIFF data from MODIS HDFs for DHI calculation. To run:
   python dhi-prepare.py year leap
year - year for which data should be downloaded and processed
leap - write leap here if the year is leap one
'''

import gc
import numpy as np
import numpy.ma as ma
from osgeo import gdal
from osgeo.gdalconst import *
import time
import glob
import sys

f_in = sys.argv[1] #"z:/nonfpar-binary-masks/stack-46/2003.tif"
f_out = sys.argv[2]

#get general parameters
dataset = gdal.Open(f_in, GA_ReadOnly)
band = dataset.GetRasterBand(1)
proj = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
dataset = None
gc.collect()

#parameters
cols = band.XSize
rows = band.YSize
slice_width = 200   #i.e. 200*17000=3400000 is number of pixels to read in with each slice
num_slices =  10    #cols/slice_width
nBlockXSize = band.GetBlockSize()[0]    #42542
nBlockYSize = band.GetBlockSize()[1]    #1
bands = 46

#output1
driver = gdal.GetDriverByName("GTiff")
sumdataset = driver.Create(f_out, cols, rows, 1, GDT_Int16)
sumdataset.SetGeoTransform(geotransform)
sumdataset.SetProjection(proj)

#no exec, native block, GDAL, 16000 reads of 46 rasters each from a single raster
dataset = gdal.Open(f_in, GA_ReadOnly)
t = time.time()
t_data_tot = 0
t_sum_tot = 0
t_write_tot = 0

for x in range(rows):
    data = np.zeros((bands, cols))
    
    t1 = time.time()
    
    for f in range(bands):
        band = dataset.GetRasterBand(f+1)
        array = band.ReadAsArray(0, x, nBlockXSize, 1)
        data[f] = array
        del array
        gc.collect()
    t_data = time.time() - t1
    
    sumarray = np.sum(data, axis=0)
    sumarray.shape = (1,sumarray.size)
    t_sum = time.time() - t1 - t_data
    
    sumdataset.GetRasterBand(1).WriteArray(sumarray,0,x)
    t_write = time.time() - t1 - t_data - t_sum
    
    t_data_tot = t_data_tot + t_data
    t_sum_tot = t_sum_tot + t_sum
    t_write_tot = t_write_tot + t_write
    #print "t_data: " + str(round(t_data, 4)) + ", t_sum: " + str(round(t_sum, 4)) + ", t_write: " + str(round(t_write, 4))

print "t_data_tot: " + str(round(t_data_tot, 4)) + ", t_sum_tot: " + str(round(t_sum_tot, 4)) + ", t_write_tot: " + str(round(t_write_tot, 4))
print "Read&write blocks " + str(x) + ", total time = " + str(round(time.time() - t, 4))
        
dataset = None
sumdataset = None

#takes about 30 minutes
#no exec, native block, GDAL, 16000 reads of 46 rasters each from multiple rasters
