import numpy as np
import numpy.ma as ma
from osgeo import gdal
from osgeo.gdalconst import *
import glob
import gc

variable = 'fpar'
inputdir = 'e:/users/maxim/thematic/dhi/source/mcd15a2/'

c = 1
files = glob.glob('*.tif')

cols = 43000
rows = 17000
slice_width = 200
num_slices = cols/slice_width

#get vals from one of the rasters
driver = gdal.GetDriverByName("GTiff")
dataset = gdal.Open(files[0], GA_ReadOnly)
proj = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()

#output1
sum_name = "dhi_1_fpar" + ".tif"
sumdataset = driver.Create(sum_name, cols, rows, 1, GDT_Int16)
sumdataset.SetGeoTransform(geotransform)
sumdataset.SetProjection(proj)

for x in range(num_slices):
    c = 1
    print('--- Reading chunk ' + str(x*slice_width) + "-" + str(x*slice_width + slice_width))
    for f in files:
        dataset = gdal.Open(f, GA_ReadOnly)
        band = dataset.GetRasterBand(1)
        dataset_def = " = dataset.ReadAsArray(" + str(x*slice_width) + ", 0, " + str(x*slice_width + slice_width) + ", band.YSize)"
        exec("array" + str(c) + dataset_def)
        dataset = None
        c = c + 1
    
    expr = ''
    for i in range(1,c):
        expr = expr + "array" + str(i) + ","
    
    expr = expr.strip(",")
    expr = expr + ''
    annualarray = np.dstack((eval(expr)))
    nodata = np.equal(annualarray,250)
    maskarray = ma.masked_array(annualarray,mask=nodata)
    del(annualarray)
    for i in range(1,c): exec("del(array" + str(i) + ")")       # free up memory
    
    # calc summed FPAR
    sumarray = np.sum(maskarray, axis=2)
    
    # DHI #1
    sumdataset.GetRasterBand(1).WriteArray(sumarray,x*slice_width,0)
    del(sumarray)
    gc.collect()
    
