#!/bin/env python
# -*- coding: utf-8 -*-

'''Prepare GeoTIFF data from MODIS HDFs for DHI calculation. To run:
   python lc-prepare.py year band_number output_folder
year - year for which data should be processed
band_number - order number of sds to import (starts with 1)
input_folder - where are input HDFs
output_folder - where to store resulting TIFs
'''

import os
import glob
import sys
import shutil
import time

def resample(hdf):
    #create output prm
    f_outprm_name = "out.prm"
    f_outprm = open(f_outprm_name, "wb")
    f_outprm.write("INPUT_FILENAME = " + os.getcwd() + "\\" + hdf + "\n")
    f_outprm.write("SPECTRAL_SUBSET = (" + spectral_subset + ")\n")
    f_outprm.write("OUTPUT_FILENAME = " + os.getcwd() + "\\" + "output.tif\n")
    f_outprm.write("RESAMPLING_TYPE = NEAREST_NEIGHBOR\n")
    f_outprm.write("OUTPUT_PROJECTION_TYPE = GEO\n")
    f_outprm.write("OUTPUT_PROJECTION_PARAMETERS = (0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" + "\n")
    f_outprm.close()

    #run resample
    cmd = path_to_mrtbin + "resample -p " + f_outprm_name
    os.system(cmd)
    shutil.move('output.'  + filename + '.tif',f_out_name)

    os.remove(f_outprm_name)
    os.remove("resample.log")

def nodata(f_in_name):
    cmd = 'gdal_calc.bat -A ' + f_in_name + ' --outfile=temp.tif --calc=\"A*(A<' + str(nodata_value) + ')\" --NoDataValue=0'
    os.system(cmd)
    os.remove(f_in_name)
    shutil.move("temp.tif",od + f_in_name)
    
def fix_crs(f_in_name):    
    cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od + f_in_name
    os.system(cmd)

if __name__ == '__main__':
    year = sys.argv[1]
    
    #Set parameters start
    ##FPAR: 249, 'MCD15A2.005', 'Fpar_1km'
    ##LANDCOVER: 254, 'MCD12Q1.051', 'Land_Cover_Type_1'
    band = sys.argv[2]
    nodata_value, modis_data_type, filename, ds_prefix = 200, 'MOD44B', 'Percent_Tree_Cover', 'vcf1'
    s = list("000000")
    s[int(band) - 1] = '1'
    spectral_subset = ' '.join(s)
    id = sys.argv[3]
    od = sys.argv[4]
    
    path_to_mrtbin = 'c:\\tools\\MRT\\bin\\'
    os.environ['MRT_DATA_DIR'] = "c:\\tools\\MRT\\data"

    #init timings
    t = time.time()
    
    date = year + ".01.01"
    os.chdir(id)
    hdfs = glob.glob("*.hdf")
    
    t1 = time.time()
    for hdf in hdfs:
        f_out_name = hdf[17:22] + ".tif"
        if not os.path.exists(od + f_out_name):
            #resample one huge HDF in sinusoidal projection into one huge GeoTIFF in geographic projection
            resample(hdf)
            
            fix_crs(f_out_name)
    t_res = time.time() - t1
    
    #merge
    t1 = time.time()
    os.chdir(od)
    tifs = glob.glob('*.tif')
    list_of_tifs = ' '.join(tifs)
    cmd = 'gdal_merge -n 255 -ps 0.00416 0.00416 -o ' + od + str(year) + '.tif ' + list_of_tifs
    os.system(cmd)
    t_merge = time.time() - t1
    
    nodata(f_out_name)
    
    print "Total time: " + str(round(time.time() - t, 4))
    print "Resample: " + str(round(t_res, 4)) + ", Merge: " + str(round(t_merge, 4))
    