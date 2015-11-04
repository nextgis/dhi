import time
import numpy as np
from osgeo import gdal
from osgeo.gdalconst import *

d1 = "../source/mcd15a2/2014.06.02.tif"
d2 = "../source/mcd15a2/2014.06.10.tif"

t = time.time()
dataset1 = gdal.Open(d1, GA_ReadOnly)
band11 = dataset1.GetRasterBand(1)	
print "open time = ", time.time() - t

dataset2 = gdal.Open(d2, GA_ReadOnly)
band12 = dataset2.GetRasterBand(1)	

t = time.time()
exec("array" + str(1) + " = dataset1.ReadAsArray(0, 0, band11.XSize, band11.YSize)")
print "read time = ", time.time() - t

exec("array" + str(1) + " = dataset2.ReadAsArray(0, 0, band12.XSize, band12.YSize)")

