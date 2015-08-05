gdal_translate -a_srs EPSG:4326 rgb_2003.tif prj/rgb_2003.tif

for %i in (*.tif) DO gdal_translate -a_srs EPSG:4326 %i prj/%i

for %i in (*.tif) DO gdalwarp -cutline ../../us-bnd/us_low48_2010_dd.shp -crop_to_cutline -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" -dstnodata nan %i ../usa/%~ni_us.tif

for /L %i in (1,1,46) DO gdal_translate -b %i giant.tif giant_%i.tif

gdalwarp -t_srs EPSG:4326 -srcnodata "249,250,251,252,253,254,255" -dstnodata nan 2006.01.01.tif 2006.01.01_.tif

for %i in (*.tif) DO gdal_calc.bat -A %i --outfile=calc/%i --calc="A*(A<249)" --NoDataValue=0

gdal_merge -separate -ps 0.0083 0.0083 -o giant.tif 2014.01.01.tif 2014.01.09.tif 2014.01.17.tif 2014.01.25.tif 2014.02.02.tif 2014.02.10.tif 2014.02.18.tif 2014.02.26.tif 2014.03.06.tif 2014.03.14.tif 2014.03.22.tif 2014.03.30.tif 2014.04.07.tif 2014.04.15.tif 2014.04.23.tif 2014.05.01.tif 2014.05.09.tif 2014.05.17.tif 2014.05.25.tif 2014.06.02.tif 2014.06.10.tif 2014.06.18.tif 2014.06.26.tif 2014.07.04.tif 2014.07.12.tif 2014.07.20.tif 2014.07.28.tif 2014.08.05.tif 2014.08.13.tif 2014.08.21.tif 2014.08.29.tif 2014.09.06.tif 2014.09.14.tif 2014.09.22.tif 2014.09.30.tif 2014.10.08.tif 2014.10.16.tif 2014.10.24.tif 2014.11.01.tif 2014.11.09.tif 2014.11.17.tif 2014.11.25.tif 2014.12.03.tif 2014.12.11.tif 2014.12.19.tif 2014.12.27.tif

for %i in (*.tif) DO  gdalwarp -tr 8000 8000 -r average %i 8km\%i

for %i in (*.tif) DO gdal_edit -a_srs "EPSG:4326" %i

for /L %i in (2003,1,2014) DO mkdir %i

for /L %i in (2005,1,2014) DO e:\users\maxim\thematic\dhi\scripts\lc_prepare.py %i

for /L %i in (2003,1,2012) DO python lc_prepare.py %i 2 y:\source\MCD12Q1\%i.01.01\hdf\ y:\source\MCD12Q1\%i.01.01\tif-umd\

for /L %i in (2005,1,2014) DO python dhi_prepare.py %i 2 y:\source\MCD15A2\%i\hdf\ y:\source\MCD15A2\%i\tif-lai\

for /L %i in (2005,1,2014) DO python download_data.py %i http://e4ftl01.cr.usgs.gov/MOTA/MCD15A3.005/ x:\MCD15A3\%i\

python vcf_prepare.py 2000 1 y:\source\MOD44B\2000.03.05\hdf\ y:\source\MOD44B\2000.03.05\tif_vcf1\

gdal_translate HDF4_EOS:EOS_GRID:"MCD12Q1.A2001001.h00v08.051.2014287161513.hdf":MOD12Q1:Land_Cover_Type_1 1.tif

for %i in (2000.03.05,2001.03.06,2002.03.06,2003.03.06,2004.03.05,2005.03.06,2006.03.06,2007.03.06,2008.03.05,2009.03.06,2010.03.06,2011.03.06,2012.03.05,2013.03.06,2014.03.06) DO (
    python hdf2tif.py MOD44B_250m_GRID:Percent_Tree_Cover y:\source\MOD44B\%i\hdf\ y:\source\MOD44B\%i\tif_vcf1\
    python hdf2tif.py MOD44B_250m_GRID:Percent_NonTree_Vegetation y:\source\MOD44B\%i\hdf\ y:\source\MOD44B\%i\tif_vcf2\
    python hdf2tif.py MOD44B_250m_GRID:Percent_NonVegetated y:\source\MOD44B\%i\hdf\ y:\source\MOD44B\%i\tif_vcf3\
    python gdal-merge-all.py %i.vrt no 0 y:\source\MOD44B\%i\tif_vcf1\ y:\source\MOD44B\%i\tif_vcf1\
    python gdal-merge-all.py %i.vrt no 0 y:\source\MOD44B\%i\tif_vcf2\ y:\source\MOD44B\%i\tif_vcf2\
    python gdal-merge-all.py %i.vrt no 0 y:\source\MOD44B\%i\tif_vcf3\ y:\source\MOD44B\%i\tif_vcf3\
    gdalwarp -t_srs EPSG:4326 y:\source\MOD44B\%i\tif_vcf1\%i.vrt y:\vcf\global\vcf_%i_tree.tif
    gdalwarp -t_srs EPSG:4326 y:\source\MOD44B\%i\tif_vcf2\%i.vrt y:\vcf\global\vcf_%i_shrub.tif
    gdalwarp -t_srs EPSG:4326 y:\source\MOD44B\%i\tif_vcf3\%i.vrt y:\vcf\global\vcf_%i_bare.tif
)

for /L %y in (2003,1,2014) DO (
    cd %y\hdf
    for /D %i DO (
        cd %i
        python e:\users\maxim\thematic\dhi\scripts\hdf2tif.py MOD_Grid_MOD15A2:Lai_1km x:\MCD15A2\%y\hdf\%i\ x:\MCD15A2\%y\hdf\%i\
        python e:\users\maxim\thematic\dhi\scripts\gdal-merge-all.py %i.vrt no 0 x:\MCD15A2\%y\hdf\%i\ x:\MCD15A2\%y\hdf\%i\
        gdalwarp -t_srs EPSG:4326 -tr 0.0083 0.0083 x:\MCD15A2\%y\hdf\%i\%i.vrt x:\MCD15A2\%y\tif-lai\lai_%i.tif
    )
    python e:\users\maxim\thematic\dhi\scripts\gdal-calc-all.py 249 x:\MCD15A2\%y\tif-lai\ x:\MCD15A2\%y\tif-lai\
)