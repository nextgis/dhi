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
import shutil
import time
import calendar

def mosaic():
    #create list with all hdfs
    f_list_name = "list.prm"
    f_list = open(f_list_name, "wb")
    for hdf in glob.glob("*.hdf"):
        f_list.write(os.getcwd() + "\\" + hdf + "\n")
    f_list.close()

    #run mrtmosaic
    cmd = path_to_mrtbin + "mrtmosaic -i " + f_list_name + " -s \"" + spectral_subset + "\" -o input.hdf"
    os.system(cmd)
    os.remove(f_list_name)
    
    print("Mosaicking completed:" + date)

def resample(date):
    #create output prm
    f_outprm_name = "out.prm"
    f_outprm = open(f_outprm_name, "wb")
    f_outprm.write("INPUT_FILENAME = " + os.getcwd() + "\\" + "input.hdf" + "\n")
    f_outprm.write("SPECTRAL_SUBSET = (1 0 0 0 0 0)\n")
    f_outprm.write("OUTPUT_FILENAME = " + os.getcwd() + "\\" + "output.tif" + "\n")
    f_outprm.write("RESAMPLING_TYPE = NEAREST_NEIGHBOR" + "\n")
    f_outprm.write("OUTPUT_PROJECTION_TYPE = GEO" + "\n")
    f_outprm.write("OUTPUT_PROJECTION_PARAMETERS = (0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)" + "\n")
    f_outprm.close()

    #run resample
    cmd = path_to_mrtbin + "resample -p " + f_outprm_name
    os.system(cmd)
    shutil.move('output.'  + filename + '.tif',date + '.tif')
    
    os.remove("input.hdf")
    os.remove(f_outprm_name)
    os.remove("resample.log")
    
    print("Resampling completed:" + date)

def nodata(date):
    cmd = 'gdal_calc.bat -A ' + f_in_name + ' --outfile=temp.tif --calc=\"A*(A<' + str(nodata_value) + ')\" --NoDataValue=0'
    os.system(cmd)
    os.remove(f_in_name)
    shutil.move("temp.tif",f_in_name)
    
def fix_crs(date):
    cmd = "gdal_edit -a_srs \"EPSG:4326\" " + f_in_name
    os.system(cmd)
    
if __name__ == '__main__':
    year = sys.argv[1]
    band = sys.argv[2]
    
    #Set parameters start
    ##FPAR: 249, 'MCD15A2.005', 'Fpar_1km'
    ##LANDCOVER: 254, 'MCD12Q1.051', 'Land_Cover_Type_1'
    nodata_value, modis_data_type, filename = 249, 'MCD15A2.005', 'Lai_1km'
    s = list("000000")
    s[int(band) - 1] = '1'
    spectral_subset = ' '.join(s)
    id = sys.argv[3]
    od = sys.argv[4]
    
    path_to_mrtbin = 'c:\\tools\\MRT\\bin\\'
    os.environ['MRT_DATA_DIR'] = "c:\\tools\\MRT\\data"
    
    dates = ["01.01"]
    dates = ["01.01","01.09","01.17","01.25","02.02","02.10","02.18","02.26","03.06","03.14","03.22","03.30","04.07","04.15","04.23","05.01","05.09","05.17","05.25","06.02","06.10","06.18","06.26","07.04","07.12","07.20","07.28","08.05","08.13","08.21","08.29","09.06","09.14","09.22","09.30","10.08","10.16","10.24","11.01","11.09","11.17","11.25","12.03","12.11","12.19","12.27"]
    dates_leap = ["01.01","01.09","01.17","01.25","02.02","02.10","02.18","02.26","03.05","03.13","03.21","03.29","04.06","04.14","04.22","04.30","05.08","05.16","05.24","06.01","06.09","06.17","06.25","07.03","07.11","07.19","07.27","08.04","08.12","08.20","08.28","09.05","09.13","09.21","09.29","10.07","10.15","10.23","10.31","11.08","11.16","11.24","12.02","12.10","12.18","12.26"]
    
    if calendar.isleap(int(year)): dates = dates_leap
    
    #init timings
    t = time.time()
    t_mos_tot = 0
    t_res_tot = 0
    t_nodata_tot = 0
    
    for date in dates:
        date = year + "." + date
        os.chdir(id + date)
        f_in_name = date + ".tif" 
        if not os.path.isdir(od + date):
            t1 = time.time()
            
            #mosaic them into one huge HDF
            mosaic()
            t_mos = time.time() - t1
            
            #resample one huge HDF in sinusoidal projection into one huge GeoTIFF in geographic projection
            resample(date)
            t_res = time.time() - t1 - t_mos
            
            nodata(date)
            fix_crs(date)
            t_nodata = time.time() - t1 - t_mos - t_res
            shutil.move(f_in_name,od + f_in_name)
            
            t_mos_tot = t_mos_tot + t_mos
            t_res_tot = t_res_tot + t_res
            t_nodata_tot = t_nodata_tot + t_nodata
    
    print "Total time: " + str(round(time.time() - t, 4))
    print "Mosaic: " + str(round(t_mos_tot, 4)) + ", Resample: " + str(round(t_res_tot, 4)) + ", Set nodata: " + str(round(t_nodata_tot, 4))