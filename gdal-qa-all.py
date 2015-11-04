#python gdal-qa-all.py x:\MCD15A2\2003\tif-fpar\before-nodata\qa\ x:\MCD15A2\2003\tif-fpar\before-nodata\ x:\MCD15A2\2003\tif-fpar-qa\

import glob
import os
import sys

wd = os.getcwd()

id_qa = sys.argv[1]        #input folder with QA rasters
id_rs = sys.argv[2]        #input folder with rasters to patch, names should match 1:1
od = sys.argv[3]           #output folder with rasters patched with QA

os.chdir(id_qa)

tifs = glob.glob('*.tif')

for tif in tifs:
    cmd = 'gdal_calc.bat -A ' + tif + ' --outfile=' + tif.replace('.tif','_b.tif') + ' --calc="1*(A<50)" --NoDataValue=0'
    print cmd
    #os.system(cmd)
    
    cmd = 'gdal_calc.bat -A ' + tif.replace('.tif','_b.tif') + ' -B ' + id_rs + tif + ' --outfile=' + od + tif + ' --calc="A*B" --NoDataValue=0'
    print cmd
    os.system(cmd)
    