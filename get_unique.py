'''Prepare DHI data from stacks of TIFs. To run:
   python grass-averages.py y:\dhi\global\fpar_4\ y:\dhi\global\fpar_4\combined\ fpar4
input_folder - where are input TIFs
output_folder - where to store resulting TIFs
suffix - suffix for output names
'''

from osgeo import gdal
import numpy as np
import sys


ds = gdal.Open(sys.argv[1])
band = ds.GetRasterBand(1)

cols = band.XSize
rows = band.YSize

nBlockXSize = band.GetBlockSize()[0]
nBlockYSize = band.GetBlockSize()[1]

unique_values = ()
for x in range(rows):
    array = band.ReadAsArray(0, x, cols, 1)
    unique_values_line = np.unique(array)
    
    unique_values = np.unique(np.hstack((unique_values,unique_values_line)))
    
for val in unique_values:
    print int(val)