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
#% description: Extract pixel value in random location to csv file 
#%end
#%option
#% key: input_prefix
#% type: string
#% required: yes
#% multiple: no
#% description: Prefix of raster names for extracting values. 
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
#% key: output
#% type: string
#% required: yes
#% multiple: no
#% description: Name of output csv file
#%end
#%option
#% key: n
#% type: inteeger
#% required: no
#% multiple: no
#% description: Number of random points for value extruction
#% answer: 1000
#%end



import sys
import os
import uuid


def main(options, flags):
      
    mapset = options['mapset']
    input_prefix = options['input_prefix']
    output = options['output']

    n_points = options['n']
      
    tmp = grass.read_command('g.mapset', flags='p')
    tmp = tmp.strip()
    if mapset != tmp:
        message = "Failed to change mapset. Current mapset is %s, desired mapset is %s. Exit the program" % (tmp, mapset)
        grass.fatal(message)
          
    maps = grass.read_command('g.list', type='raster',
        mapset=mapset, pattern="%s*" % (input_prefix, ))
    maps = maps.split()

    perm_maps = grass.read_command('g.list', type='raster',
        mapset='PERMANENT', pattern="%s*" % (input_prefix, ))
    perm_maps = perm_maps.split()
    perm_maps = [p + '@PERMANENT' for p in perm_maps]
    
    maps = maps + perm_maps

    try:
        tmp_vect = 'v' + uuid.uuid4().hex
        outfile = open(output, "a")
        grass.run_command('v.random', output=tmp_vect, npoints=n_points)
        for m in maps:
            values = grass.read_command('r.what', map=m, points=tmp_vect, separator=',') 
            for val in values.split():
                new = val.strip() +',' + m
                outfile.write(new+'\n')
                
    finally:
        try:
            grass.run_command('g.remove', type='vector', name=tmp_vect, flags='f') 
        except:
            pass
        outfile.close()
        
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
    
