#python gdal-calc-all.py 200 y:\vcf\global\ y:\vcf\global\calc UInt16

import glob
import os
import sys
import shutil

wd = os.getcwd()
val = sys.argv[1]       #200 - all values greater than that will be set to NODATA
id = sys.argv[2]        #input folder
od = sys.argv[3]        #output folder
type = '' #sys.argv[4]      #output data type

os.chdir(id)

tifs = glob.glob('*.tif')
for tif in tifs:
    cmd = 'gdal_calc.bat ' + type + '-A ' + tif + ' --outfile=temp.tif ' + tif + ' --calc="A*(A<' + val + ') " --NoDataValue=0'
    os.system(cmd)
    
    shutil.move('temp.tif',od + tif)