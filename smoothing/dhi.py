#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# dhi.py
# ---------------------------------------------------------
#
# Copyright (C) 2015 Kolesov Dmitry (kolesov.dm@gmail.com)
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

#%module
#% description: Create DHI for raster data series of vegetation indexis.
#% keyword: raster, vegetation indexes, DHI
#%end
#%option
#% key: input_prefix
#% type: string
#% required: yes
#% multiple: no
#% description: Prefix of raster names of raster time series.
#% gisprompt: list of raster names
#%end
#%option
#% key: mapset
#% type: string
#% required: yes
#% multiple: no
#% key_desc: mapset with raster data
#% description: mapset with raster data
#%end
#%option
#% key: out_prefix
#% type: string
#% required: yes
#% multiple: no
#% description: Prefix for dhi raster
#%end


import sys
import os



def main(options, flags):
      
    
    mapset = options['mapset']
    input_prefix = options['input_prefix']
    
    out_prefix = options['out_prefix']
      
    tmp = grass.read_command('g.mapset', flags='p')
    tmp = tmp.strip()
    if mapset != tmp:
        message = "Failed to change mapset. Current mapset is %s, desired mapset is %s. Exit the program" % (tmp, mapset)
        grass.fatal(message)
          

    print mapset, input_prefix
    maps = grass.read_command('g.list', type='raster', separator=',',
        mapset=mapset, pattern="%s*" % (input_prefix, ))
    maps = maps.strip()
    
    # remove previouse results (if any)
    grass.run_command('g.remove', type='raster', pattern="%s*" % (out_prefix, ), flags='f')

    code = grass.run_command('r.series', input=maps,
        output="%s1,%s2,std,mean" % (out_prefix, out_prefix), 
        method="sum,minimum,stddev,average", overwrite=True)
    if code != 0:
        grass.fatal("r.series step falls")
    else:       
        code = grass.run_command('r.mapcalc', expression="%s3 = float(std/mean)" % (out_prefix, ))
        if code != 0:
            grass.fatal("r.mapcalc step falls")
        
        
if __name__ == "__main__":
    gisbase = os.environ['GISBASE']
    gisdbase = os.environ['GISDBASE']
    location = os.environ['LOCATION_NAME']
    
    # Find mapset in params:
    for param in sys.argv:
        if not 'mapset=' in param:
            continue
        else:
            break
    mapset = param.split('=')[1]
    sys.path.append(os.path.join(os.environ['GISBASE'], "etc", "python"))
    
    from grass.script.core import gisenv
    import grass.script as grass
    import grass.script.setup as gsetup
    gsetup.init(gisbase, gisdbase, location, mapset)

    options, flags = grass.parser()
    sys.exit(main(options, flags))
    
