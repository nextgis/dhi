#!/usr/bin/env python
# -*- coding: utf-8 -*-

#******************************************************************************
#
# download_modis_data.py
# ---------------------------------------------------------
# Download MODIS data
# More: http://github.com/nextgis/dhi
#
# Usage: 
#      download_modis_data.py year numslices url output_folder create_hdf_folder
#      where:
#           year               year
#           numslices          number of time periods per year
#           url                base url where to download from
#           output_folder      where to store downloaded file
#           create_hdf_folder  if yes, hdf subfolder will be created for each date, else hdf folder will be created for the whole session
# Example:
#      python download_modis_data.py 2003 92 http://e4ftl01.cr.usgs.gov/MOTA/MCD15A3.005/ x:\MCD15A3\2003\ no
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

import sys
import os
import calendar

#Download data
def download(date):
    print("Downloading started: " + date)
    
    cmd = 'wget ' + link + '/' + date + '/ --quiet --recursive --level=1 --accept=hdf --no-directories'
    print cmd
    os.system(cmd)
    
    print("Downloading completed: " + date)
    
if __name__ == '__main__':
    #dates = sys.argv[1]
    year = sys.argv[1]
    numslices = int(sys.argv[2])
    link = sys.argv[3]
    wd = sys.argv[4]
    create_hdf_folder = sys.argv[5]
    
    if numslices == 46:
        dates = '01.01,01.09,01.17,01.25,02.02,02.10,02.18,02.26,03.06,03.14,03.22,03.30,04.07,04.15,04.23,05.01,05.09,05.17,05.25,06.02,06.10,06.18,06.26,07.04,07.12,07.20,07.28,08.05,08.13,08.21,08.29,09.06,09.14,09.22,09.30,10.08,10.16,10.24,11.01,11.09,11.17,11.25,12.03,12.11,12.19,12.27'
        dates_leap = '01.01,01.09,01.17,01.25,02.02,02.10,02.18,02.26,03.05,03.13,03.21,03.29,04.06,04.14,04.22,04.30,05.08,05.16,05.24,06.01,06.09,06.17,06.25,07.03,07.11,07.19,07.27,08.04,08.12,08.20,08.28,09.05,09.13,09.21,09.29,10.07,10.15,10.23,10.31,11.08,11.16,11.24,12.02,12.10,12.18,12.26'
    elif numslices == 23:
        dates = '01.01,01.17,02.02,02.18,03.06,03.22,04.07,04.23,05.09,05.25,06.10,06.26,07.12,07.28,08.13,08.29,09.14,09.30,10.16,11.01,11.17,12.03,12.19'
        dates_leap = '01.01,01.17,02.02,02.18,03.05,03.21,04.06,04.22,05.08,05.24,06.09,06.25,07.11,07.27,08.12,08.28,09.13,09.29,10.15,10.31,11.16,12.02,12.18'
    elif numslices == 12:
        dates = '01.01,02.01,03.01,04.01,05.01,06.01,07.01,08.01,09.01,10.01,11.01,12.01'
        dates_leap = dates
    elif numslices == 92:
        dates = '01.01,01.05,01.09,01.13,01.17,01.21,01.25,01.29,02.02,02.06,02.10,02.14,02.18,02.22,02.26,03.02,03.06,03.10,03.14,03.18,03.22,03.26,03.30,04.03,04.07,04.11,04.15,04.19,04.23,04.27,05.01,05.05,05.09,05.13,05.17,05.21,05.25,05.29,06.02,06.06,06.10,06.14,06.18,06.22,06.26,06.30,07.04,07.08,07.12,07.16,07.20,07.24,07.28,08.01,08.05,08.09,08.13,08.17,08.21,08.25,08.29,09.02,09.06,09.10,09.14,09.18,09.22,09.26,09.30,10.04,10.08,10.12,10.16,10.20,10.24,10.28,11.01,11.05,11.09,11.13,11.17,11.21,11.25,11.29,12.03,12.07,12.11,12.15,12.19,12.23,12.27,12.31'
        dates_leap = '01.01,01.05,01.09,01.13,01.17,01.21,01.25,01.29,02.02,02.06,02.10,02.14,02.18,02.22,02.26,03.01,03.05,03.09,03.13,03.17,03.21,03.25,03.29,04.02,04.06,04.10,04.14,04.18,04.22,04.26,04.30,05.04,05.08,05.12,05.16,05.20,05.24,05.28,06.01,06.05,06.09,06.13,06.17,06.21,06.25,06.29,07.03,07.07,07.11,07.15,07.19,07.23,07.27,07.31,08.04,08.08,08.12,08.16,08.20,08.24,08.28,09.01,09.05,09.09,09.13,09.17,09.21,09.25,09.29,10.03,10.07,10.11,10.15,10.19,10.23,10.27,10.31,11.04,11.08,11.12,11.16,11.20,11.24,11.28,12.02,12.06,12.10,12.14,12.18,12.22,12.26,12.30 '
    
    if calendar.isleap(int(year)): dates = dates_leap
    
    if not os.path.exists(wd): os.mkdir(wd)
    os.chdir(wd)
    if create_hdf_folder != "yes":
        if not os.path.exists('hdf'): os.mkdir("hdf")
        os.chdir("hdf")
    
    for date in dates.split(','):
        date = year + '.' + date
        if not os.path.exists(date): os.mkdir(date)
        os.chdir(date)
        if create_hdf_folder == "yes":
            if not os.path.exists('hdf'): os.mkdir("hdf")
            os.chdir("hdf")
        
        download(date)
        if create_hdf_folder == "yes":
            os.chdir('../..')
        else:
            os.chdir('../')