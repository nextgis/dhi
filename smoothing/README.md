
This directory contains scripts for smoothing raster time series (in time domain).
The scripts are wrappers for r.series.filter GRASS GIS addons module. 

## Installation

### Requirements:

* GRASS GIS 7;
* GRASS GIS module r.series.filer (it is avialable from GRASS ADDONS);
* (option) Linux system for parallel computings;


### Installation steps

#### GRASS GIS

Install GRASS GIS 7 from the system repository (recomended) or compile it from the source code 
(it's usefull if you don't have credentials to install software in system level). In the second case
you can install GRASS GIS in your home directory.

Some notes for compilation from source code are given bellow. Skip them if you have installed GRASS from the
system repo.

##### Compillaion

Full description of the process can be found here: https://svn.osgeo.org/grass/grass/trunk/INSTALL.

1. Download GRASS sources.

2. Configure it.
This is an example of configure paramethers:

```
./configure \
  --prefix="/home/local/RUSSELL/USERNAME/GRASSBIN" \
  --enable-macosx-app=no \
  --enable-largefile=yes \
  --enable-shared          \
  --enable-w11=no \
  --with-postgres=yes \
  --with-readline=yes \
  --with-gdal \
  --with-blas=yes \
  --with-postgres-includes=/usr/include/postgresql \
  --with-freetype-includes=/usr/include/freetype2 \
  --with-opengl=no \
  --with-fftw=no \
  --with-cairo=no \
  --with-freetype=no \
   --with-x=no \
  --with-wxwidgets=no \
  --enable-64bit
```
The directory of installation is configured by prefix paramether, change USERNAME to appropriate value.

*NOTE.* This configuration doesn't use some important features of GRASS (for example GRASS GUI based on wxWidgets), 
but this configuration is enough to run the smoothing procedure. Also you can disable postgres and freetype dependencies.

3. Navigate do directory contained the configure script. Save this configuration in a file, for example 'myconfigure' and run it:
```
echo "
./configure \
  --prefix="/home/local/RUSSELL/USERNAME/GRASSBIN" \
  --enable-macosx-app=no \
  --enable-largefile=yes \
  --enable-shared          \
  --enable-w11=no \
  --with-postgres=yes \
  --with-readline=yes \
  --with-gdal \
  --with-blas=yes \
  --with-postgres-includes=/usr/include/postgresql \
  --with-freetype-includes=/usr/include/freetype2 \
  --with-opengl=no \
  --with-fftw=no \
  --with-cairo=no \
  --with-freetype=no \
   --with-x=no \
  --with-wxwidgets=no \
  --enable-64bit
" > myconfigure
chomod +x myconfigure
./myconfigure
```

Be carefull about error messages. If they appear, check the configuration paramethers, fix them and run the configuration  again.

4. Make and install
```
make
make install
```


#### r.series.filter

The module can be installed using g.extestion.

1. Run GRASS GIS.
2. Install the module:
```
g.extension r.series.filter
```

