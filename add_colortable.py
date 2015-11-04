#!/bin/env python
# -*- coding: utf-8 -*-

'''Prepare GeoTIFF data from MODIS HDFs for DHI calculation. To run:
   python add_colortable.py input output colortable
input - input GeoTIFF with Gray legend to which colortable will be attached
output - output GeoTIFF
colortable - path to colortable
'''

import os
import sys
import shutil

def attach_color_table(f_in_name,f_out_name,f_clrs_name):
    f_vrt_name = f_in_name.replace(".tif",".vrt")
    f_vrt_name2 = f_in_name.replace(".tif","_2.vrt")
    cmd = "gdal_translate -of VRT " + f_in_name + " " + f_vrt_name
    os.system(cmd)
    
    f_vrt_in = open(f_vrt_name,'rb')
    f_vrt_out = open(f_vrt_name2,'wb')
    f_clrs = open(f_clrs_name,'rb')
    
    for str in f_vrt_in:
        if "<ColorInterp>Gray" in str:
            f_vrt_out.write("<ColorInterp>Palette</ColorInterp>\n")
            for clr in f_clrs:
                f_vrt_out.write(clr)
        else:
            f_vrt_out.write(str)
    
    f_vrt_out.write("\n")
    f_vrt_out.close()
    f_vrt_in.close()
    
    cmd = "gdal_translate " + f_vrt_name2 + " temp.tif"
    os.system(cmd)
    shutil.move('temp.tif',f_out_name)
    os.remove(f_vrt_name)
    os.remove(f_vrt_name2)
    
if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    colortable = sys.argv[3]
    
    #attach color table
    attach_color_table(input,output,colortable)
    