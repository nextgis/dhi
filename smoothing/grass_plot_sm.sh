#!/bin/sh

# grass_plot_sm.sh vector_points raster1,raster2,...  smrast1,smrast2,... myCSV_pref

POINTS=$1
RASTERS=$2
SMOOTHR=$3
PREFIX=$5

for PNT in $(v.out.ascii $POINTS sep=,)
do
	coord=$(echo $PNT  | cut -d, -f1,2)
	cat=$(echo $PNT |  cut -d, -f3)
	echo $coor
	CSVFILE=${PREFIX}${cat}.csv
	PICFILE=${PREFIX}${cat}.png
	
	r.what map=$SMOOTHR coord=$coord sep=, > $CSVFILE 
	r.what map=$RASTERS coord=$coord sep=, >> $CSVFILE 

	Rscript plot.R  $CSVFILE $PICFILE 
	rm $CSVFILE
done


