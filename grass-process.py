'''Prepare DHI data from stacks of TIFs. To run:
   python grass-process.py 2004 x:\MCD15A2\2003\tif-lai\after-nodata\ y:\dhi\global\lai\ lai
year - year for which data should be processed
input_folder - where are input TIFs
output_folder - where to store resulting TIFs
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
#gisdbase = os.environ['GISDBASE'] = "x:/MOD13Q1/2003/tif-ndvi/"
location = "dhi_grass"
mapset   = "PERMANENT"

sys.path.append(os.path.join(gisbase, "etc", "python"))
 
import grass.script as grass
import grass.script.setup as gsetup
gsetup.init(gisbase, gisdbase, location, mapset)

year = sys.argv[1]
id = sys.argv[2]
od = sys.argv[3]
prefix = 'dhi'
suffix = sys.argv[4]
os.chdir(id)
fn_out = prefix + '_' + year + '_' + suffix + '.tif'

t = time.time()

for f in glob.glob('*.tif'):
    grass.run_command('r.in.gdal', input=f, output=f.replace('.tif',''))
    
t_import = time.time() - t

#for f in glob.glob('*.tif'):
#    grass.run_command('r.null', map=f.replace('.tif',''), setnull="249,250,251,252,253,254,255")
#    
t_nodata = time.time() - t - t_import

result = ''
p = grass.pipe_command('g.mlist', type = 'rast', quiet=True, pattern=year + '*')
for line in p.stdout:
    result = result + ',' + line.replace('\n','')

input_rast_list = result.strip(',')

grass.run_command('r.series', input=input_rast_list, output='dh1_' + year + ',dh2_' + year + ',ave_' + year + ',std_' + year, method='sum,minimum,average,stddev')
grass.mapcalc('dh3_' + year + ' = std_' + year + '/ave_' + year)
t_calc = time.time() - t - t_import - t_nodata

grass.run_command('i.group', group='rgb_group_' + year, input='dh1_' + year + ',dh2_' + year + ',dh3_' + year)
grass.run_command('r.out.gdal', input='rgb_group_' + year, output=fn_out, type='Float32', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES')
shutil.move(fn_out,od + fn_out)
shutil.move(fn_out.replace('.tif','.tfw'),od + fn_out.replace('.tif','.tfw'))
cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od + fn_out
os.system(cmd)

t_export = time.time() - t - t_import - t_nodata - t_calc

print "Import: " + str(round(t_import, 4)) + ", Nodata: " + str(round(t_nodata, 4)) + ", Calculations: " + str(round(t_calc, 4)) + ", Export: " + str(round(t_export, 4))
