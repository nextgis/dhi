#!/bin/env python
# -*- coding: utf-8 -*-

'''Prepare GeoTIFF data from MODIS HDFs for DHI calculation. To run:
   python hdf2tiff.py year band_number output_folder
dataset - dataset name
input_folder - where are input HDFs
output_folder - where to store resulting TIFs
'''

#python hdf2tif.py MOD44B_250m_GRID:Percent_Tree_Cover y:\source\MOD44B\2000.03.05\hdf\ y:\source\MOD44B\2000.03.05\tif_vcf1\

import glob
import sys
import os
from progressbar import *

def resample(hdf,f_out_name):
    cmd = 'gdal_translate -q ' + pref + '\"' + hdf + '\":' + dataset + ' ' + od + f_out_name
    os.system(cmd)

if __name__ == '__main__':
    dataset = sys.argv[1]   #MOD44B_250m_GRID:Percent_Tree_Cover - example
    id = sys.argv[2]
    od = sys.argv[3]
    
    os.chdir(id)
    hdfs = glob.glob("*.hdf")
    pref = 'HDF4_EOS:EOS_GRID:'
    
    pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Counter(), " of " + str(len(hdfs)), ' ', ETA()]).start()
    pbar.maxval = len(hdfs)
    
    for hdf in hdfs:
        f_out_name = hdf[17:23] + ".tif"
        if not os.path.exists(od + f_out_name):
            resample(hdf,f_out_name)
            pbar.update(pbar.currval+1)
        
    pbar.finish()