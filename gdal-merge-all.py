#python gdal-merge-all.py 2000.vrt no 0 y:\source\MOD44B\2000.03.05\tif_vcf1\ y:\source\MOD44B\2000.03.05\tif_vcf1\

import glob
import os
import sys

wd = os.getcwd()

fn = sys.argv[1]        #filename.vrt or filename.tif
separate = sys.argv[2]  #yes is set
pix_size = sys.argv[3]  #0 if not set
id = sys.argv[4]        #input
od = sys.argv[5]

os.chdir(id)

tifs = glob.glob('*.tif')
list_of_tifs = ' '.join(tifs)

if separate == 'yes': 
    separate = '-separate'
else:
    separate = ''
    
if pix_size != '0': 
    pix_size = '-ps ' + pix_size + ' ' + pix_size
else:
    pix_size = ''

if fn.split('.')[-1] == 'vrt': 
    pix_size = pix_size.replace('ps','tr')
    cmd = 'gdalbuildvrt' + separate + ' ' + pix_size + ' ' + ' -o ' + fn + ' ' + list_of_tifs
else:
    cmd = 'gdal_merge ' + separate + ' ' + pix_size + ' ' + ' -o ' + od + fn + ' ' + list_of_tifs
    
print cmd
os.system(cmd)
