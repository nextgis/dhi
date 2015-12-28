#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# filter.py
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
#% description: Filter raster data series of vegetation indexis.
#% keyword: raster, vegetation indexis
#%end
#%flag
#% key: i
#% description: Transform results to integer raster maps.
#%end
#%flag
#% key: d
#% description: remove results of the first step on exit.
#%end
#%option
#% key: input_prefix
#% type: string
#% required: yes
#% multiple: no
#% description: Prefix of raster names of equally spaced time series.
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
#% key: step1_resprefix
#% type: string
#% required: yes
#% multiple: no
#% description: Prefix for smoothed results after first step of smoothing
#%end
#%option
#% key: step2_resprefix
#% type: string
#% required: yes
#% multiple: no
#% description: Prefix for smoothed results after second step of smoothing
#%end
#%option
#% key: logfile
#% type: string
#% required: no
#% multiple: no
#% description: Name of logfile
#% answer: filter.log
#%end
#%option
#% key: winsize
#% type: integer
#% required: no
#% multiple: no
#% description: Initial winsize for filtering
#% answer: 13
#%end


import sys
import os

import logging

def setup_log(logfile, mapset, level=logging.DEBUG):
    logger = logging.getLogger(mapset)
    logger.setLevel(level)
    
    fh = logging.FileHandler(logfile)
    fh.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    
    return logger


def main(options, flags):
      
    transform_type = flags['i']
    remove_first_step = flags['d']
    
    mapset = options['mapset']
    input_prefix = options['input_prefix']
    
    step1_resprefix = options['step1_resprefix']
    step2_resprefix = options['step2_resprefix']
    
    winsize = options['winsize']
    logfile = options['logfile']
    
    logger = setup_log(logfile, mapset)
    
    logger.info('Start calculations in "%s" mapset' % (mapset, ))
      
    tmp = grass.read_command('g.mapset', flags='p')
    tmp = tmp.strip()
    if mapset != tmp:
        message = "Failed to change mapset. Current mapset is %s, desired mapset is %s. Exit the program" % (tmp, mapset)
        logger.error(message)
        grass.fatal(message)
          
    logger.debug('Enter in "%s" mapset' % (tmp, ))

    maps = grass.read_command('g.list', type='raster', separator=',',
        mapset='PERMANENT', pattern="%s*" % (input_prefix, ))
    maps = maps.strip()
    logger.debug('Found rasters: %s' % (maps, ))
    
    # remove previouse results (if any)
    grass.run_command('g.remove', type='raster', pattern="%s*" % (step1_resprefix, ), flags='f')
    code = grass.run_command('r.series.filter', input=maps, result_prefix=step1_resprefix, 
        method='median', winsize=winsize, flags='u')
    if code != 0:
        logger.error("First step falls")
    else:       
        logger.info("First step done")
        # remove previouse results (if any)
        grass.run_command('g.remove', type='raster', pattern="%s*" % (step2_resprefix, ), flags='f')
        maps = grass.read_command('g.list', type='raster', separator=',',
            mapset=mapset, pattern="%s*" % (step1_resprefix, ))
        maps = maps.strip()
        
        code = grass.run_command('r.series.filter', input=maps, result_prefix=step2_resprefix, 
            method='savgol', winsize=winsize)
            
        if code != 0:
            logger.error("Second step falls")
        else:
            logger.info("Second step done")
            if transform_type:
                maps = grass.read_command('g.list', type='raster', pattern="%s*" % (step2_resprefix, ))
                maps = maps.split()
                for map in maps:
                    grass.run_command('r.mapcalc', expression = "%s = round(%s)" % (map, map), overwrite=True)
    
    if remove_first_step:
        grass.run_command('g.remove', type='raster', pattern="%s*" % (step1_resprefix, ), flags='f')

    logger.info('Calculations in "%s" mapset done' % (mapset, ))

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
    
