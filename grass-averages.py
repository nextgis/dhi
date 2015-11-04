'''Prepare DHI data from stacks of TIFs. To run:
   python grass-averages.py y:\dhi\global\fpar_4\ y:\dhi\global\fpar_4\combined\ fpar4
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
location = "dhi_grass"
mapset   = "PERMANENT"

sys.path.append(os.path.join(gisbase, "etc", "python"))
 
import grass.script as grass
import grass.script.setup as gsetup
gsetup.init(gisbase, gisdbase, location, mapset)

id = sys.argv[1]
od = sys.argv[2]
prefix = 'dhi'
suffix = sys.argv[3]
os.chdir(id)

names = ['dh1','dh2','dh3']
for f in glob.glob('*.tif'):
    for i in range(3):
        grass.run_command('r.in.gdal', input=f, band=i+1, output=f.replace('.tif','') + '_' + names[i])
    
dh1_list = ''
dh2_list = ''
dh3_list = ''
p = grass.pipe_command('g.mlist', type = 'rast', quiet=True, pattern='*dh1')
for line in p.stdout:
    dh1_list = dh1_list + ',' + line.replace('\n','')

p = grass.pipe_command('g.mlist', type = 'rast', quiet=True, pattern='*dh2')
for line in p.stdout:
    dh2_list = dh2_list + ',' + line.replace('\n','')

p = grass.pipe_command('g.mlist', type = 'rast', quiet=True, pattern='*dh3')
for line in p.stdout:
    dh3_list = dh3_list + ',' + line.replace('\n','')

dh1_list = dh1_list.strip(',')
dh2_list = dh2_list.strip(',')
dh3_list = dh3_list.strip(',')

grass.run_command('r.series', input=dh1_list, output='dh1_med,dh1_ave,dh1_sd', method='median,average,stddev')
grass.run_command('r.series', input=dh2_list, output='dh2_med,dh2_ave,dh2_sd', method='median,average,stddev')
grass.run_command('r.series', input=dh3_list, output='dh3_med,dh3_ave,dh3_sd', method='median,average,stddev')

grass.run_command('i.group', group='rgb_group_med', input='dh1_med,dh2_med,dh3_med')
grass.run_command('i.group', group='rgb_group_ave', input='dh1_ave,dh2_ave,dh3_ave')
grass.run_command('i.group', group='rgb_group_sd', input='dh1_sd,dh2_sd,dh3_sd')

groups = ('rgb_group_med','rgb_group_ave','rgb_group_sd')
output_names = ('dhi_median','dhi_average','dhi_sddev')
output_names_short = ('median','average','sddev')
dhs = ('dh1','dh2','dh3')

for i in range(3):
    fn_out = output_names[i]
    grass.run_command('r.out.gdal', input=groups[i], output=fn_out + '.tif', type='Float32', createopt='PROFILE=BASELINE,INTERLEAVE=PIXEL,TFW=YES')
    
    shutil.move(fn_out + '.tif',od + fn_out + '_' + suffix + '.tif')
    shutil.move(fn_out + '.tfw',od + fn_out + '_' + suffix + '.tfw')
    
    cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od + fn_out + '_' + suffix + '.tif'
    os.system(cmd)
    
    for j in range(3):
        fn_out2 = output_names_short[i]
        cmd = "gdal_translate -b " + str(j+1) + ' ' + od + fn_out + '_' + suffix + '.tif ' + od + dhs[j] + '_' + fn_out2 + '_' + suffix + '.tif'
        os.system(cmd)
        
