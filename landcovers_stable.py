'''Calculate stable landcovers, i.e. landcovers that never changed during whole time period
   stable_landcovers.py y:\landcover\global\fpar-lai\ fpar
input_folder - where are input TIFs
suffix - product, used for filenames and colors assignment
'''

import glob
import os
import sys
import string

wd = sys.argv[1]
os.chdir(wd)
suffix = sys.argv[2]
startyear = 2003
endyear = 2012

#separate each landcover year into binary masks
numclasses = 11
numyears = len(range(startyear,endyear+1))

for c in range(0, numclasses + 1):
    for year in range(startyear,endyear+1):
        year = 'lc_' + str(year) + '_' + suffix + '.tif'
        year_c = year.replace('.tif','_' + str(c) + '.tif')
        cmd = 'gdal_calc --overwrite -A ' + year + ' --outfile=' + year_c + ' --calc="1*(A==' + str(c) + ')" --NoDataValue=0'
        print(cmd)
        os.system(cmd)

#sum them all up
for c in range(numclasses + 1):
    i=0
    inputs = ''
    strsum = ''
    for year in glob.glob('*_' + str(c) + '.tif'):
        inputs = inputs + '-' + string.uppercase[i] + ' ' + year + ' '
        strsum = strsum + string.uppercase[i] + '+'
        i+=1
    
    inputs = inputs.rstrip(' ')
    strsum = strsum.rstrip('+')
    cmd = 'gdal_calc --overwrite ' + inputs + ' --outfile=' + str(c) + '_sum.tif ' + '--calc="(' + strsum + ')"'
    print(cmd)
    os.system(cmd)

#recalculate to class value if numyears, for 0 recalc to 100
c = 0
cmd = 'gdal_calc --overwrite -A 0_sum.tif --outfile=0_stable.tif --calc="100*(A==' + str(numyears) + ')" --NoDataValue=0'
print(cmd)
os.system(cmd)

for c in range(1,numclasses + 1):
    cmd = 'gdal_calc --overwrite -A ' + str(c) + '_sum.tif ' + '--outfile=' + str(c) + '_stable.tif ' + ' --calc="'+ str(c) + '*(A==' + str(numyears) + ')" --NoDataValue=0'
    print(cmd)
    os.system(cmd)

#remove nodata=0
for c in range(numclasses + 1):
    cmd = 'gdal_translate -a_nodata none ' + str(c) + '_stable.tif ' + str(c) + '_stable1.tif '
    print(cmd)
    os.system(cmd)

#sum rasters back together
inputs = ''
strsum = ''
for c in range(numclasses + 1):
    inputs = inputs + '-' + string.uppercase[c] + ' ' + str(c) + '_stable1.tif '
    strsum = strsum + string.uppercase[c] + '+'
    
inputs = inputs.rstrip(' ')
strsum = strsum.rstrip('+')
cmd = 'gdal_calc --overwrite ' + inputs + ' --outfile=sum.tif ' + '--calc="(' + strsum + ')"'
os.system(cmd)

#recalc 100 back to 0

cmd = 'gdal_calc --overwrite -A sum.tif --outfile=_res.tif --calc="255*(A==0)+0*(A==100)+A*(A<100)" --NoDataValue=255'
os.system(cmd)

#assign colortable
cmd = 'python e:/users/maxim/thematic/dhi/scripts/add_colortable.py y:/landcover/global/fpar-lai/_res.tif y:/landcover/global/fpar-lai/stable_landscapes.tif e:/users/maxim/thematic/dhi/scripts/colortables/fpar.txt'
os.system(cmd)

#clean up
for c in range(numclasses + 1):
    os.remove(str(c) + '_sum.tif')
    os.remove(str(c) + '_stable.tif')
    os.remove(str(c) + '_stable1.tif')
    for year in range(startyear,endyear+1):
        year = str(year) + '.tif'
        year_c = year.replace('.tif','_' + str(c) + '.tif')
        os.remove(year_c)
        
os.remove('sum.tif')
os.remove('_res.tif')
