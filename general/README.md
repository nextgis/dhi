# dhi
Collection of scripts to create DHI data. Scripts are written in Python and are simple wrappers for GDAL and GRASS functions. Some of them are Windows-dependent, but should be adapted easily to Linux.

add_colortable.py - assign new colortable to a TIF

calc_all.py - apply a raster math calculation to series of TIFs

colortable_all.py - assign new colortable to series of TIFs

create_combined_dhi.py - produce combined DHI product from source data

create_yearly_dhi.py - produce yearly DHI product from source data

download_modis_data.py - download yearly MODIS data

get_unique.py - create a list of unique values

hdf2tif.py - convert series of HDFs to TIFs

landcovers_majority.py - create aggregated landcovers by using majority rule

landcovers_stable.py - create aggregated landcovers by using absolute majority rule

merge_all.py - merge series of rasters

prepare_data.py - convert all HDFs to TIFs (hdf2tif.py), mosaic all together (merge_all.py) and reproject to EPSG:4326

qa_all.py - create QA binary mask and apply them to raster data to produce filtered data.