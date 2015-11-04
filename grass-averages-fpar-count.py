'''Prepare DHI data from stacks of TIFs. To run:
   python grass-averages-fpar.py x:\MCD15A2\combined\fpar8\cnt 46
input_folder - where are input TIFs
output_folder - where to store count TIFs for each time slice
suffix - suffix for output names
'''

import os
import sys
import glob
import time
import shutil

#prepare environment
gisbase = os.environ['GISBASE'] = "c:/tools/NextGIS_QGIS/apps/grass/grass-6.4.4/"
gisdbase = os.environ['GISDBASE'] = "e:/users/maxim/thematic/dhi/"
location = "dhi_grass"
mapset   = "PERMANENT"

sys.path.append(os.path.join(gisbase, "etc", "python"))
 
import grass.script as grass
import grass.script.setup as gsetup
gsetup.init(gisbase, gisdbase, location, mapset)

od = sys.argv[1]
numslices = int(sys.argv[2])
prefix = 'dhi'
os.chdir(od)

years = range(2003,2014+1)


for i in range(1,numslices+1):
    list = ''
    for year in years:
        list = list + ',' + str(year) + '_' + str(i)
    list = list.strip(',')
    
    grass.run_command('r.series', input=list, output=str(i) + '_cnt', method='count')

#export averaged rasters
for i in range(1,numslices+1):
    grass.run_command('r.out.gdal', input=str(i)+'_cnt', output=str(i) + '_cnt.tif', type='Byte', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES')
    
    cmd = "gdal_edit -a_srs \"EPSG:4326\" " + str(i) + '_cnt.tif'
    os.system(cmd)
    