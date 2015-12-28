#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# hdf2tif.py
# ---------------------------------------------------------
# Convert series of HDFs to TIFs
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      hdf2tif.py dataset input_folder output_folder
#      where:
#           -h              show this help message and exit
#           dataset         subdataset code (use gdalinfo to get it)
#           input_folder    input folder with HDFs
#           output_folder   output folder with TIFs
# Examples:
#      python hdf2tif.py MOD44B_250m_GRID:Percent_Tree_Cover y:\source\MOD44B\2000.03.05\hdf\ y:\source\MOD44B\2000.03.05\tif_vcf1\
#
# Copyright (C) 2015 Maxim Dubinin (sim@gis-lab.info)
#
# This source is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This code is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# A copy of the GNU General Public License is available on the World Wide Web
# at <http://www.gnu.org/copyleft/gpl.html>. You can also obtain it by writing
# to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA.
#
#******************************************************************************

import glob
import sys
import os
from progressbar import *
import argparse

def resample(hdf,f_out_name):
    cmd = 'gdal_translate -q ' + pref + '\"' + hdf + '\":' + dataset.split(':')[0] + ':' + '\"' + dataset.split(':')[1] + '\"' + ' ' + args.output_folder + f_out_name
    os.system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', help='Subdataset code (use gdalinfo to get it)')
    parser.add_argument('input_folder', help='Output folder with HDFs')
    parser.add_argument('output_folder', help='Output folder with HDFs')
    args = parser.parse_args()
    
    dataset = args.dataset   #MOD44B_250m_GRID:Percent_Tree_Cover - example
    
    print(args.input_folder)
    
    os.chdir(args.input_folder)
    hdfs = glob.glob("*.hdf")
    if len(hdfs) == 0:
        print("Nothing to convert. Exiting.")
        sys.exit(1)
        
    pref = 'HDF4_EOS:EOS_GRID:'
    
    pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Counter(), " of " + str(len(hdfs)), ' ', ETA()]).start()
    pbar.maxval = len(hdfs)
    
    for hdf in hdfs:
        #f_out_name = hdf + ".tif"
        f_out_name = hdf[17:23] + ".tif"
        if not os.path.exists(args.output_folder + f_out_name):
            resample(hdf,f_out_name)
            pbar.update(pbar.currval+1)
        
    pbar.finish()