from osgeo import gdal
from osgeo.gdalconst import *
import numpy as np
import numpy.ma as ma
import gc

d_name = "MCD13Q1_SUBJOHANNA_8-day_UTM_cl_2_subset_16-day.dat"

ds = gdal.Open(d_name, GA_ReadOnly)
proj = ds.GetProjection()
geotransform = ds.GetGeoTransform()
band = ds.GetRasterBand(1)
cols = band.XSize
rows = band.YSize
nBlockXSize = band.GetBlockSize()[0]
nBlockYSize = band.GetBlockSize()[1]
bands = 37

#output1
mean_name = "mean" + ".tif"
driver = gdal.GetDriverByName("GTiff")
meandataset = driver.Create(mean_name, cols, rows, 1, GDT_Int16)
meandataset.SetGeoTransform(geotransform)
meandataset.SetProjection(proj)

for x in range(rows):
	print(x)
	data = np.zeros((bands, cols))
	for f in range(bands):
		band = ds.GetRasterBand(f+1)
		array = band.ReadAsArray(0, x, nBlockXSize, 1)
		nodata = np.less(array,0)
		data[f] = ma.masked_array(array,mask=nodata)
		gc.collect()
	meanarray = np.mean(data,axis=0)
	meanarray.shape = (1,meanarray.size)
	meandataset.GetRasterBand(1).WriteArray(meanarray,0,x)


#for i in range(1,38):
#	band = ds.GetRasterBand(i)
#	exec("array" + str(i) + " = ds.ReadAsArray(0, 0, band.XSize, band.YSize)")
#	print(i)

#expr = ''
#for i in range(1,38):
#	expr = expr + "array" + str(i) + ","
    
#expr = expr.strip(",")
#layers = np.dstack((eval(expr)))
