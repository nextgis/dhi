'''Prepare DHI data from stacks of TIFs. To run:
   python get_unique.py y:\dhi\global\fpar_4\,y:\dhi\global\fpar_4\combined\ out.txt
argument1 - list of folders separated by commas
out.txt - where to store list of unique values
'''

from osgeo import gdal
import numpy as np
import sys
import glob
import argparse
from progressbar import *

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('output', help='Output file')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-rs','--rasters', help='path(s) to raster, separate by comma if several')
group.add_argument('-fs','--folders', help='path(s) to folders with raster, separate by comma if several')

args = parser.parse_args()
inRasters = []

if args.folders:
    rasterPaths = args.folders.split(',')
    for rasterPath in rasterPaths:
        inRasters.extend(glob.glob(rasterPath + '*.tif'))

if args.rasters:
    inRasters.extend(args.rasters.split(','))

unique_values_all = ()

for raster in inRasters:
    print('Processing raster ' + raster)
    
    ds = gdal.Open(raster)
    band = ds.GetRasterBand(1)

    cols = band.XSize
    rows = band.YSize

    nBlockXSize = band.GetBlockSize()[0]
    nBlockYSize = band.GetBlockSize()[1]
    
    pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Counter(), " of " + str(rows), ' ', ETA()]).start()
    pbar.maxval = rows
    
    unique_values = ()
    for x in range(rows):
        array = band.ReadAsArray(0, x, cols, 1)
        unique_values_line = np.unique(array)
        
        unique_values = np.unique(np.hstack((unique_values,unique_values_line)))
        pbar.update(pbar.currval+1)
    
    unique_values_all = np.unique(np.hstack((unique_values_all,unique_values)))
    print('Found ' + str(len(unique_values)) + ' values for current raster. Total unique: ' + str(len(unique_values_all))+'\n')
    pbar.finish()
        
    f_out = open(args.output,'wb')
    for val in unique_values_all:
        f_out.write(str(int(val)) + '\n')

    f_out.close()