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
#      hdf2tif.py [-h] [--recurse] [-o] dataset input_folder
#      where:
#           -h              show this help message and exit
#           dataset         subdataset code (use gdalinfo to get it)
#           input_folder    input folder with HDFs
#           -r,recurse         enter every subfolder of input folder
#           -o,overwrite       overwrite all existing files
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

parser = argparse.ArgumentParser()
parser.add_argument('dataset', help='Subdataset code (use gdalinfo to get it)')
parser.add_argument('input_folder', help='Input folder with HDFs')
parser.add_argument('-r','--recurse', action="store_true", help='Walk in directories and use their name as output name')
parser.add_argument('-o','--overwrite', action="store_true", help='Overwrite all intermediary and resulting files')
args = parser.parse_args()

def resample(hdf,f_out_name):
    cmd = 'gdal_translate -q ' + pref + '\"' + hdf + '\":' + dataset.split(':')[0] + ':' + '\"' + dataset.split(':')[1] + '\"' + ' ' + f_out_name
    os.system(cmd)
    #print(cmd)

def sanitize():
    if not args.input_folder.endswith('\\'): args.input_folder = args.input_folder + '\\'
    
    return args.input_folder

if __name__ == '__main__':
    id = sanitize()

    dataset = args.dataset   #MOD44B_250m_GRID:Percent_Tree_Cover - example
    folders = []
    if args.recurse: 
        subdirs = next(os.walk(id))[1]
        for folder in subdirs:
            folders.append(os.path.join(id, folder))
    else:
        folders = [id]
    
    pref = 'HDF4_EOS:EOS_GRID:'
    
    for folder in folders:
        print(folder)
        os.chdir(folder)
        hdfs = glob.glob("*.hdf")
        
        if len(folders) ==1 and len(hdfs) == 0:
            print("Nothing to convert. Exiting.")
            sys.exit(1)
        
        pbar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Counter(), " of " + str(len(hdfs)), ' ', ETA()]).start()
        pbar.maxval = len(hdfs)

        for hdf in hdfs:
            #f_out_name = hdf + ".tif"
            f_out_name = folder + '\\' + hdf[17:23] + ".tif"
            if not os.path.exists(f_out_name) or args.overwrite:
                resample(hdf,f_out_name)
                pbar.update(pbar.currval+1)
            
        pbar.finish()