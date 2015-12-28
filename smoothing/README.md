
This directory contains scripts for smoothing raster time series (in time domain).
The scripts are wrappers for r.series.filter GRASS GIS addons module. 

## Installation

### Requirements:

* GRASS GIS 7 (installation is described here: https://github.com/simgislab/dhi/wiki/Install-GRASS);
* Install numpy (```virtualenv ~/venv; source ~/venv/bin/activate;pip install numpy```)
* Install scipy (```virtualenv ~/venv; source ~/venv/bin/activate;pip install scipy```)
* GRASS GIS module r.series.filer (it is avialable from GRASS ADDONS) (to install run ```g.extension r.series.filter```;
* (optional) Linux system for parallel computing;

## Smoothing procedure

### Import data

Import raw data into PERMANENT mapset. To do that you have to create new LOCATION (if it doesn't exist) using a raster
from the time series. It helps you to set up default region (boundaries and resolution).

### Start calculations with parallelization of the smoothing process

To run the calculations in several processes you have to:

1. Create chuncks -- new MAPSETs with smaller regions that contains a part of initial rasters.
2. Run the process in several chuncks simultaneously. Wait until the results have done in every chunck.
3. Patch the partial results in PERMANENT location.

The steps are described bellow in details.

#### Chunk creation
You  can create chuncks manually or you can use script create_mapset.py:

```
python -d create_mapsets.py cols=1000 rows=1000
```
MAPSETs with size 1000x1000 pixels will be created. The mapsets covers default PERMANENT region. The names of the mapsets 
are consctucted by the rule: 'PREFIX_rowNumber_colNumber'; PREFIX is fixed string and it equals to 'node_'.

*Note.* This procedure have to be done only once. If you want to restart the smoothing procedure and you have the chunks already,
then skip this step.

*Note.* The script must be executed in active GRASS seesion.

#### Smoothing in the chuncks

Export enviroment variables 
 * GISBASE: path to GRASS binary, the subdirectory where GRASS GIS was installed, 
 * GISDBASE: path to GRASS GIS database, 
 * LOCATION_NAME: name of the mapset containig data,
 * MAPSET: initial mapset with data (PERRMANENT),
 * GUI: type of used user interface (text).

For example if GRASS GIS was installed to /home/local/RUSSELL/kolesov/GRASSBIN/,
GRASSDATA directory is /mnt/kolesov/nimbus/GRASSDATA and data location is  WordLL,
then the enviroment variables can be exported by the next lines (unux shell commands):
 
```
export GISBASE='/home/local/RUSSELL/kolesov/GRASSBIN/grass-7.0.3svn'
export GISDBASE='/mnt/kolesov/nimbus/GRASSDATA'
export LOCATION_NAME='WorldLL'
export GUI='text'
export MAPSET='PERMANENT'
```

To check if the variables are difined correctly you can run smoothing in one
chunck (for example for upper-left node, assume that input rasters have prefix "mod2003*"):
```
python filter.py -i -d input=mod2003* step1="res." step2="fin." mapset=node_0_0
```
The script filter.py is a wrapper around r.series.filter, it runs the smoothing procedure (two steps)
in particular mapset. If it runs without errors, the variables are defined correctly.


##### Parallelisation
To run filter.py in several chuncks simultaneously we have to create a file with list of  all chunk names.
To do that we can run the shell command:
```
find "$GISDBASE/$LOCATION_NAME" -name "node_*" | cut -d'/' -f7 > nodes
```
This command creates list of MAPSETs (with pattern "node_*"), then extructs the last part of the paths and saves them
in file "nodes". Note the number of the field (7 in this case) depends on the path.

When you have the list of chunck you can run the parallel calculations using 'xargs' command. For example,
to run filter.py in ten mapsets at once, you can use the command:
```
cat nodes | xargs -n1 -I {} -P 10 python filter.py -i -d input=mod2003* step1="res." step2="fin." mapset={}
```
