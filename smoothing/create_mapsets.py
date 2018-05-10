#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# create_mapsets.py
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
#% description: Splits region to small chunkcs and creates separate mapsets for the chunks.
#% keyword: general, settings
#%end
#%flag
#% key: d
#% description: Set from PERMANENT default region
#%end
#%option
#% key: rows
#% type: integer
#% required: yes
#% multiple: no
#% key_desc: value
#% description: Number of rows in the new regions
#% guisection: Resolution
#%end
#%option
#% key: cols
#% type: integer
#% required: yes
#% multiple: no
#% key_desc: value
#% description: Number of columns in the new regions
#% guisection: Resolution
#%end

import sys
import os

if "GISBASE" not in os.environ:
    sys.stderr.write("You must be in GRASS GIS to run this program.\n")
    sys.exit(1)

import grass.script as grass

def main(options, flags): 
    if flags['d']:
        grass.run_command('g.mapset', mapset='PERMANENT', quiet=True)
        grass.run_command('g.region', flags='d')

    reg = grass.region()

    cols = int(options['cols'])  # Count of columns in the mapsets
    rows = int(options['rows'])  # Count of rows in the mapsets
    
    # ew = reg['e'] - reg['w']
    dx = cols * reg['ewres']

    ns = reg['n'] - reg['s']
    dy = rows * reg['nsres']

    west = reg['w']
    south = reg['s']

    i = j = 0
    try:
        while west < reg['e'] - reg['ewres']:  # Don't create mapset less then one-pixel size => subtract reg['ewres']
            while south < reg['n'] - reg['nsres']:
                mapset_name = "node_%s_%s" % (j, i)
                grass.run_command('g.mapset', mapset=mapset_name, flags='c', quiet=True)
                grass.run_command('g.region', s=south, n=min(reg['n'], south+dy),
                                  w=west, e=min(reg['e'], west+dx), flags='p')
                south += dy
                j += 1
            west += dx
            i += 1
            j = 0
            south = reg['s']
    finally:
        grass.run_command('g.mapset', mapset='PERMANENT')
        # grass.run_command('g.mapset', mapset='test')

if __name__ == "__main__":
    options, flags = grass.parser()
    sys.exit(main(options, flags))



