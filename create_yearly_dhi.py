#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# create_yearly_dhi.py
# ---------------------------------------------------------
# Create yearly DHI product
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      create_yearly_dhi.py year input_folder output_folder suffix
#      where:
#           year            year
#           input_folder    input folder
#           output_folder   where to store the result
#           suffix          suffix to end to resulting file name
# Example:
#      python create_yearly_dhi.py 2004 x:\MCD15A2\2003\tif-lai\after-nodata\ y:\dhi\global\lai\ lai
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

year = sys.argv[1]
id = sys.argv[2]
od = sys.argv[3]
prefix = 'dhi'
suffix = sys.argv[4]
os.chdir(id)
fn_out = prefix + '_' + year + '_' + suffix + '.tif'

t = time.time()

#for f in glob.glob('*.tif'):
#    grass.run_command('r.in.gdal', input=f, output=f.replace('.tif',''))
    
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
shutil.move(fn_out + '.aux.xml',od + fn_out + '.aux.xml')
cmd = "gdal_edit -a_srs \"EPSG:4326\" " + od + fn_out
os.system(cmd)

t_export = time.time() - t - t_import - t_nodata - t_calc

print "Import: " + str(round(t_import, 4)) + ", Nodata: " + str(round(t_nodata, 4)) + ", Calculations: " + str(round(t_calc, 4)) + ", Export: " + str(round(t_export, 4))
