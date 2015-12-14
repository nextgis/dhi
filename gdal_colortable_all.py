import glob
import os
import shutil

wd = os.getcwd()
ds_prefix = 'fpar'

tifs = glob.glob('*.tif')
for f_in_name in tifs:
    f_vrt_name = f_in_name.replace(".tif",".vrt")
    f_vrt_name2 = f_in_name.replace(".tif","_2.vrt")
    f_clrs_name = "e:/users/maxim/thematic/dhi/scripts/colortables/" + ds_prefix + ".txt"
    cmd = "gdal_translate -of VRT " + f_in_name + " " + f_vrt_name
    os.system(cmd)
    
    f_vrt_in = open(f_vrt_name,'rb')
    f_vrt_out = open(f_vrt_name2,'wb')
    f_clrs = open(f_clrs_name,'rb')
    
    for str in f_vrt_in:
        if "<ColorInterp>Gray" in str or "<ColorInterp>Palette" in str:
            f_vrt_out.write("<ColorInterp>Palette</ColorInterp>\n")
            for clr in f_clrs:
                f_vrt_out.write(clr)
        elif "ColorTable" in str or "Entry" in str:
            continue #do nothing
        else:
            f_vrt_out.write(str)
    
    f_vrt_out.write("\n")
    f_vrt_out.close()
    f_vrt_in.close()
    
    cmd = "gdal_translate " + f_vrt_name2 + " temp.tif"
    os.system(cmd)
    os.remove(f_in_name)
    shutil.move('temp.tif',f_in_name)
    os.remove(f_vrt_name)
    os.remove(f_vrt_name2)
    
