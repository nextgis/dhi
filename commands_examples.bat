gdal_translate -a_srs EPSG:4326 rgb_2003.tif prj/rgb_2003.tif

for %i in (*.tif) DO gdal_translate -a_srs EPSG:4326 %i prj/%i

for %i in (*.tif) DO gdalwarp -cutline ../../us-bnd/us_low48_2010_dd.shp -crop_to_cutline -t_srs "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=23 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs" -dstnodata nan %i ../usa/%~ni_us.tif
gdalwarp -cutline e:\users\maxim\maps\yakutia.shp -crop_to_cutline dhi_med_fpar8qa_f.tif dhi_med_fpar8qa_f_yakut.tif

for /L %i in (1,1,46) DO gdal_translate -b %i giant.tif giant_%i.tif

gdalwarp -t_srs EPSG:4326 -srcnodata "249,250,251,252,253,254,255" -dstnodata nan 2006.01.01.tif 2006.01.01_.tif

for %i in (*.tif) DO gdal_calc.bat -A %i --outfile=calc/%i --calc="A*(A<249)" --NoDataValue=0

gdal_merge -separate -ps 0.0083 0.0083 -o giant.tif 2014.01.01.tif 2014.01.09.tif 2014.01.17.tif 2014.01.25.tif 2014.02.02.tif 2014.02.10.tif 2014.02.18.tif 2014.02.26.tif 2014.03.06.tif 2014.03.14.tif 2014.03.22.tif 2014.03.30.tif 2014.04.07.tif 2014.04.15.tif 2014.04.23.tif 2014.05.01.tif 2014.05.09.tif 2014.05.17.tif 2014.05.25.tif 2014.06.02.tif 2014.06.10.tif 2014.06.18.tif 2014.06.26.tif 2014.07.04.tif 2014.07.12.tif 2014.07.20.tif 2014.07.28.tif 2014.08.05.tif 2014.08.13.tif 2014.08.21.tif 2014.08.29.tif 2014.09.06.tif 2014.09.14.tif 2014.09.22.tif 2014.09.30.tif 2014.10.08.tif 2014.10.16.tif 2014.10.24.tif 2014.11.01.tif 2014.11.09.tif 2014.11.17.tif 2014.11.25.tif 2014.12.03.tif 2014.12.11.tif 2014.12.19.tif 2014.12.27.tif

for %i in (*.tif) DO  c:\tools\7z\7z.exe a %~n.7z %i

for %i in (*.tif) DO  gdalwarp -tr 8000 8000 -r average %i 8km\%i

for %i in (*.tif) DO gdal_edit -a_srs "EPSG:4326" %i

for /L %i in (2003,1,2014) DO mkdir %i

for /L %i in (2005,1,2014) DO e:\users\maxim\thematic\dhi\scripts\lc_prepare.py %i

for /L %i in (2003,1,2012) DO python lc_prepare.py %i 2 y:\source\MCD12Q1\%i.01.01\hdf\ y:\source\MCD12Q1\%i.01.01\tif-umd\

for /L %i in (2005,1,2014) DO python dhi_prepare.py %i 2 y:\source\MCD15A2\%i\hdf\ y:\source\MCD15A2\%i\tif-lai\

for /L %i in (2005,1,2014) DO python download_modis_data.py %i http://e4ftl01.cr.usgs.gov/MOTA/MCD15A3.005/ x:\MCD15A3\%i\
for /L %i in (2000,1,2014) DO python download_modis_data.py %i 46 http://e4ftl01.cr.usgs.gov/MOLT/MOD17A2.055/ x:\MOD17A2\%i\ no
for /L %i in (2002,1,2014) DO python download_modis_data.py %i 23 http://e4ftl01.cr.usgs.gov/MOLT/MOD13A1.006/ x:\MOD13A1\%i\ no
for /L %i in (2000,1,2014) DO python download_modis_data.py %i 23 http://e4ftl01.cr.usgs.gov/MOLT/MOD13A2.006/ x:\MOD13A2\%i\ no

for /L %i in (2009,1,2014) DO python create_yearly_dhi.py %i x:\MCD15A3\%i\tif-fpar-qa\ y:\dhi\global\fpar_4\ fpar4qa
for /L %i in (2003,1,2014) DO python create_yearly_dhi.py %i x:\MCD15A3\%i\tif-lai-qa\ y:\dhi\global\lai_4\ lai4qa
for /L %i in (2005,1,2014) DO python create_yearly_dhi.py %i x:\MCD15A2\%i\tif-fpar-qa\ y:\dhi\global\fpar_8\ fpar8qa
for /L %i in (2003,1,2014) DO python create_yearly_dhi.py %i x:\MOD17A2\%i\tif-gpp-qa\ y:\dhi\global\gpp\ gppqa

python create_yearly_dhi.py 2003 x:\MOD13Q1\2003\tif-ndvi\ y:\dhi\global\ndvi\ ndvi
python create_combined_dhi.py x:\MCD15A3\ x:\MCD15A3\combined\fpar4\ y:\dhi\global\fpar_4\combined-v3\ fpar4qa
python create_combined_dhi.py x:\MCD15A3\ x:\MCD15A3\combined\lai4\ y:\dhi\global\lai_4\combined-v3\ lai4qa lai
python create_combined_dhi.py x:\MCD17A2\ x:\MCD17A2\combined\gpp\ y:\dhi\global\gpp\combined-v3\ gppqa gpp
python create_combined_dhi.py x:\MOD13A2\ x:\MOD13A2\combined\gpp\ y:\dhi\global\ndvi\1000\combined-v3\ ndviqa ndvi

python extract_values.py -g e:\users\maxim\thematic\dhi\random_points\other\fpar8.shp  -d y:\dhi\global\fpar_8\ -e tif

python prepare_data.py 2003 MODIS_Grid_16DAY_250m_500m_VI:"250m 16 days NDVI" x:\MOD13Q1\2003\hdf\ x:\MOD13Q1\2003\tif-ndvi\ 0.002
python prepare_data.py 2003 "MOD_Grid_MOD15A2:FparLai_QC" x:\MCD15A2\2003\hdf\ x:\MCD15A2\2003\tif-fpar\qa\ 0.0083
python prepare_data.py 2003 "MODIS_Grid_16DAY_250m_500m_VI:250m 16 days NDVI" x:\MOD13Q1\2003\hdf\ x:\MOD13Q1\2003\tif-ndvi-sin\ 250

for /L %i in (2003,1,2014) DO python prepare_data.py MOD_Grid_MOD15A2:Lai_1km x:\MCD15A2\%i\hdf\ x:\MCD15A2\%i\tif-lai\ 0.0083
for /L %i in (2003,1,2014) DO python prepare_data.py MOD_Grid_MOD15A2:FparLai_QC x:\MCD15A3\%i\hdf\ x:\MCD15A2\%i\qa\ 0.0083
for /L %i in (2000,1,2014) DO python prepare_data.py MOD_Grid_MOD17A2:Gpp_1km x:\MOD17A2\%i\hdf\ x:\MOD17A2\%i\tif-gpp\ 0.0083
for /L %i in (2000,1,2014) DO python prepare_data.py MOD_Grid_MOD17A2:Psn_QC_1km x:\MOD17A2\%i\hdf\ x:\MOD17A2\%i\qa\ 0.0083
for /L %i in (2001,1,2014) DO python prepare_data.py "MODIS_Grid_16DAY_500m_VI:500m 16 days NDVI" x:\MOD13A1\%i\hdf\ x:\MOD13A1\%i\tif-ndvi\ 0.00416
for /L %i in (2003,1,2014) DO python prepare_data.py "MODIS_Grid_16DAY_1km_VI:1 km 16 days NDVI" x:\MOD13A2\%i\hdf\ x:\MOD13A2\%i\tif-ndvi\ 0.0083
for /L %i in (2003,1,2014) DO python prepare_data.py "MODIS_Grid_16DAY_1km_VI:1 km 16 days EVI" x:\MOD13A2\%i\hdf\ x:\MOD13A2\%i\tif-evi\ 0.0083
for /L %i in (2003,1,2014) DO python prepare_data.py "MODIS_Grid_16DAY_1km_VI:1 km 16 days VI Quality" x:\MOD13A2\%i\hdf\ x:\MOD13A2\%i\qa\ 0.0083
for /L %i in (2003,1,2014) DO python prepare_data.py "MODIS_Grid_16DAY_500m_VI:500m 16 days VI Quality" x:\MOD13A1\%i\hdf\ x:\MOD13A1\%i\qa\ 0.00416


python hdf2tif.py MODIS_Grid_16DAY_250m_500m_VI:"250m 16 days NDVI" x:\MOD13Q1\2003\hdf\2003.01.01\ x:\MOD13Q1\2003\tif-ndvi\\

python vcf_prepare.py 2000 1 y:\source\MOD44B\2000.03.05\hdf\ y:\source\MOD44B\2000.03.05\tif_vcf1\

gdal_translate HDF4_EOS:EOS_GRID:"MCD12Q1.A2001001.h00v08.051.2014287161513.hdf":MOD12Q1:Land_Cover_Type_1 1.tif
gdal_translate HDF4_EOS:EOS_GRID:"MOD13Q1.A2003001.h00v08.005.2007266192255.hdf":MODIS_Grid_16DAY_250m_500m_VI:"250m 16 days NDVI" 1.tif

REM extract QA data for 2003
for %i in (2003.01.01,2003.01.09,2003.01.17,2003.01.25,2003.02.02,2003.02.10,2003.02.18,2003.02.26,2003.03.06,2003.03.14,2003.03.22,2003.03.30,2003.04.07,2003.04.15,2003.04.23,2003.05.01,2003.05.09,2003.05.17,2003.05.25,2003.06.02,2003.06.10,2003.06.18,2003.06.26,2003.07.04,2003.07.12,2003.07.20,2003.07.28,2003.08.05,2003.08.13,2003.08.21,2003.08.29,2003.09.06,2003.09.14,2003.09.22,2003.09.30,2003.10.08,2003.10.16,2003.10.24,2003.11.01,2003.11.09,2003.11.17,2003.11.25,2003.12.03,2003.12.11,2003.12.19,2003.12.27) DO (
    python hdf2tif.py MOD_Grid_MOD15A2:FparLai_QC x:\MCD15A2\2003\hdf\%i\ x:\MCD15A2\2003\hdf\%i\
    python merge_all.py %i.vrt no 0 x:\MCD15A2\2003\hdf\%i\ x:\MCD15A2\2003\hdf\%i\
    gdalwarp -t_srs EPSG:4326 -tr 0.0083 0.0083 x:\MCD15A2\2003\hdf\%i\%i.vrt x:\MCD15A2\2003\tif-fpar\before-nodata\qa\%i.tif
)

REM extract fire data for 2014 from MCD45A1
for %i in (2014.01.01,2014.02.01,2014.03.01,2014.04.01,2014.05.01,2014.06.01,2014.07.01,2014.08.01,2014.09.01,2014.10.01,2014.11.01,2014.12.01) DO (
    python hdf2tif.py MOD_GRID_Monthly_500km_BA:burndate x:\MCD45A1\2014\hdf\%i\ x:\MCD45A1\2014\hdf\%i\
    python merge_all.py %i.vrt no 0 x:\MCD45A1\2014\hdf\%i\ x:\MCD45A1\2014\hdf\%i\
    gdalwarp -t_srs EPSG:4326 -tr 0.0046 0.0046 x:\MCD45A1\2014\hdf\%i\%i.vrt x:\MCD45A1\2014\tif\%i.tif
)
for /L %i in (2003,1,2014) DO python prepare_data.py %i MOD_GRID_Monthly_500km_BA:burndate x:\MCD45A1\%i\hdf\ x:\MCD45A1\%i\hdf\ 0.0046 4326

for %i in (*.tif) DO (
    gdal_calc.bat -A %i --outfile=%~ni_b.tif --calc="A*(A<366)" --NoDataValue=0
)

REM calculate version patched with QA
for %i in (*.tif) DO (
    gdal_calc.bat -A %i --outfile=%~ni_b.tif --calc="1*(A<50)" --NoDataValue=0
    gdal_calc.bat -A %~ni_b.tif -B ..\%i --outfile=..\..\..\tif-fpar-qa\%i --calc="A*B" --NoDataValue=0
)

python qa_all.py x:\MCD15A2\2003\tif-fpar\qa\ x:\MCD15A2\2003\tif-fpar\ x:\MCD15A2\2003\tif-fpar-qa\
for /L %i in (2003,1,2014) DO python qa_all.py x:\MCD15A2\%i\qa\ x:\MCD15A2\%i\tif-fpar\ x:\MCD15A2\%i\tif-fpar-qa\
for /L %i in (2003,1,2014) DO python qa_all.py x:\MCD15A2\%i\qa\ x:\MCD15A2\%i\tif-lai\ x:\MCD15A2\%i\tif-lai-qa\
for /L %i in (2003,1,2014) DO python qa_all.py x:\MCD15A3\%i\qa\ x:\MCD15A3\%i\tif-lai\ x:\MCD15A3\%i\tif-lai-qa\
for /L %i in (2003,1,2014) DO python qa_all.py x:\MOD17A2\%i\qa\ x:\MOD17A2\%i\tif-gpp\ x:\MOD17A2\%i\tif-gpp-qa\
for /L %i in (2003,1,2014) DO python qa_all.py -iq x:\MOD17A2\%i\qa\ -ir x:\MOD17A2\%i\tif-gpp\ -o x:\MOD17A2\%i\tif-gpp-qa\ -s yes
for /L %i in (2003,1,2014) DO python qa_all.py -iq x:\MOD15A2\%i\qa\ -ir x:\MOD15A2\%i\tif-evi\ -o x:\MOD15A2\%i\tif-evi-qa\ -s yes
for /L %i in (2003,1,2014) DO python qa_all.py x:\MOD13A2\%i\qa\ x:\MOD13A2\%i\tif-ndvi\ x:\MOD13A2\%i\tif-ndvi-qa\

for /L %i in (2003,1,2014) DO python calc_all.py 32761 x:\MOD17A2\%i\tif-gpp\ x:\MOD17A2\%i\tif-gpp\
for /L %i in (2003,1,2014) DO python calc_all.py -3000 x:\MOD13A2\%i\tif-evi\ x:\MOD13A2\%i\tif-evi\
    

for %i in (2000.03.05,2001.03.06,2002.03.06,2003.03.06,2004.03.05,2005.03.06,2006.03.06,2007.03.06,2008.03.05,2009.03.06,2010.03.06,2011.03.06,2012.03.05,2013.03.06,2014.03.06) DO (
    python hdf2tif.py MOD44B_250m_GRID:Percent_Tree_Cover y:\source\MOD44B\%i\hdf\ y:\source\MOD44B\%i\tif_vcf1\
    python hdf2tif.py MOD44B_250m_GRID:Percent_NonTree_Vegetation y:\source\MOD44B\%i\hdf\ y:\source\MOD44B\%i\tif_vcf2\
    python hdf2tif.py MOD44B_250m_GRID:Percent_NonVegetated y:\source\MOD44B\%i\hdf\ y:\source\MOD44B\%i\tif_vcf3\
    python merge_all.py %i.vrt no 0 y:\source\MOD44B\%i\tif_vcf1\ y:\source\MOD44B\%i\tif_vcf1\
    python merge_all.py %i.vrt no 0 y:\source\MOD44B\%i\tif_vcf2\ y:\source\MOD44B\%i\tif_vcf2\
    python merge_all.py %i.vrt no 0 y:\source\MOD44B\%i\tif_vcf3\ y:\source\MOD44B\%i\tif_vcf3\
    gdalwarp -t_srs EPSG:4326 y:\source\MOD44B\%i\tif_vcf1\%i.vrt y:\vcf\global\vcf_%i_tree.tif
    gdalwarp -t_srs EPSG:4326 y:\source\MOD44B\%i\tif_vcf2\%i.vrt y:\vcf\global\vcf_%i_shrub.tif
    gdalwarp -t_srs EPSG:4326 y:\source\MOD44B\%i\tif_vcf3\%i.vrt y:\vcf\global\vcf_%i_bare.tif
)

REM process all landcovers
for %i in (2003.01.01,2004.01.01,2005.01.01,2006.01.01,2007.01.01,2008.01.01,2009.01.01,2010.01.01,2011.01.01,2012.01.01) DO (
    python hdf2tif.py MOD12Q1:Land_Cover_Type_1 x:\MCD12Q1\%i\hdf\ x:\MCD12Q1\%i\tif-igbp\
    python hdf2tif.py MOD12Q1:Land_Cover_Type_2 x:\MCD12Q1\%i\hdf\ x:\MCD12Q1\%i\tif-umd\
    python hdf2tif.py MOD12Q1:Land_Cover_Type_3 x:\MCD12Q1\%i\hdf\ x:\MCD12Q1\%i\tif-fpar\
    python hdf2tif.py MOD12Q1:Land_Cover_Type_4 x:\MCD12Q1\%i\hdf\ x:\MCD12Q1\%i\tif-npp\
    python hdf2tif.py MOD12Q1:Land_Cover_Type_5 x:\MCD12Q1\%i\hdf\ x:\MCD12Q1\%i\tif-pft\
    python merge_all.py %i.vrt no 0 x:\MCD12Q1\%i\tif-igbp\ x:\MCD12Q1\%i\tif-igbp\
    python merge_all.py %i.vrt no 0 x:\MCD12Q1\%i\tif-umd\ x:\MCD12Q1\%i\tif-umd\
    python merge_all.py %i.vrt no 0 x:\MCD12Q1\%i\tif-fpar\ x:\MCD12Q1\%i\tif-fpar\
    python merge_all.py %i.vrt no 0 x:\MCD12Q1\%i\tif-npp\ x:\MCD12Q1\%i\tif-npp\
    python merge_all.py %i.vrt no 0 x:\MCD12Q1\%i\tif-pft\ x:\MCD12Q1\%i\tif-pft\
    gdalwarp -t_srs EPSG:4326 x:\MCD12Q1\%i\tif-igbp\%i.vrt y:\landcover\global\igbp\new\lc_%i_igbp.tif
    gdalwarp -t_srs EPSG:4326 x:\MCD12Q1\%i\tif-umd\%i.vrt y:\landcover\global\umd\new\lc_%i_umd.tif
    gdalwarp -t_srs EPSG:4326 x:\MCD12Q1\%i\tif-fpar\%i.vrt y:\landcover\global\fpar-lai\new\lc_%i_fpar.tif
    gdalwarp -t_srs EPSG:4326 x:\MCD12Q1\%i\tif-npp\%i.vrt y:\landcover\global\npp\new\lc_%i_npp.tif
    gdalwarp -t_srs EPSG:4326 x:\MCD12Q1\%i\tif-pft\%i.vrt y:\landcover\global\pft\new\lc_%i_pft.tif
    python add_colortable.py y:\landcover\global\igbp\new\lc_%i_igbp.tif y:\landcover\global\igbp\new\lc_%i_igbp.tif e:\users\maxim\thematic\dhi\scripts\colortables\igbp.txt
    python add_colortable.py y:\landcover\global\umd\new\lc_%i_umd.tif y:\landcover\global\umd\new\lc_%i_umd.tif e:\users\maxim\thematic\dhi\scripts\colortables\umd.txt
    python add_colortable.py y:\landcover\global\fpar-lai\new\lc_%i_fpar.tif y:\landcover\global\fpar-lai\new\lc_%i_fpar.tif e:\users\maxim\thematic\dhi\scripts\colortables\fpar.txt
    python add_colortable.py y:\landcover\global\npp\new\lc_%i_npp.tif y:\landcover\global\npp\new\lc_%i_npp.tif e:\users\maxim\thematic\dhi\scripts\colortables\npp.txt
    python add_colortable.py y:\landcover\global\pft\new\lc_%i_pft.tif y:\landcover\global\pft\new\lc_%i_pft.tif e:\users\maxim\thematic\dhi\scripts\colortables\pft.txt 
)

REM extract QA for LC
for %i in (2003.01.01,2004.01.01,2005.01.01,2006.01.01,2007.01.01,2008.01.01,2009.01.01,2010.01.01,2011.01.01,2012.01.01) DO (
    python hdf2tif.py MOD12Q1:Land_Cover_Type_QC W:\MCD12Q1\%i\hdf\ W:\MCD12Q1\%i\qa\
)

REM this doesn't work because of stupidity of Windows command prompt
for /L %y in (2003,1,2014) DO (
    cd %y\hdf
    for /D %i DO (
        cd %i
        python e:\users\maxim\thematic\dhi\scripts\hdf2tif.py MOD_Grid_MOD15A2:Lai_1km x:\MCD15A2\%y\hdf\%i\ x:\MCD15A2\%y\hdf\%i\
        python e:\users\maxim\thematic\dhi\scripts\merge_all.py %i.vrt no 0 x:\MCD15A2\%y\hdf\%i\ x:\MCD15A2\%y\hdf\%i\
        gdalwarp -t_srs EPSG:4326 -tr 0.0083 0.0083 x:\MCD15A2\%y\hdf\%i\%i.vrt x:\MCD15A2\%y\tif-lai\lai_%i.tif
    )
    python e:\users\maxim\thematic\dhi\scripts\calc_all.py 249 x:\MCD15A2\%y\tif-lai\ x:\MCD15A2\%y\tif-lai\
)


python e:\users\maxim\Programming\python\extract_values\extract_values.py -g -f e:\users\maxim\thematic\dhi\random_points\biomes\pnt_wwf_globe_biome8_tempgrass_20k.shp -rl W:\AMPHIBIANS_global_IUCN_range_counts_int32_world.img,W:\BIRDS_global_IUCN_range_counts_int32_world.img,W:\MAMMTERR_global_IUCN_range_counts_int32_world.img,W:\REPTILES_global_IUCN_range_counts_int32_world.img,y:\landcover\global\fpar-lai\stable_landscapes_mj.tif,y:\dhi\global\fpar_8_qa\combined-v2\dhi_med_fpar8qa_f.tif

python e:\users\maxim\Programming\python\extract_values\extract_values.py -g -f e:\users\maxim\thematic\dhi\random_points\biomes-shp\pnt_wwf_globe_biome8_tempgrass_30k.shp -rl W:\AMPHIBIANS_global_IUCN_range_counts_int32_world.img,W:\BIRDS_global_IUCN_range_counts_int32_world.img,W:\MAMMTERR_global_IUCN_range_counts_int32_world.img,W:\REPTILES_global_IUCN_range_counts_int32_world.img,y:\landcover\global\igbp\majority_landcovers.tif,y:\dhi\global\fpar_8\combined-v3\dhi_fpar8qa_f.tif,y:\dhi\global\lai_8\combined-v3\dhi_lai8qa_f.tif

for %i in (*.shp) DO ogr2ogr -sql "SELECT * FROM %~ni WHERE majority_l NOT IN (0,12,13,15,16,254,255) AND dhi_fpar1 != -1 ORDER BY RANDOM() LIMIT 10000" -dialect SQLITE select\%i %i

python landcovers_majority.py y:\landcover\global\npp\ npp majority_landcovers.tif 9

python e:\users\maxim\Programming\python\extract_values\extract_values.py -g -f c:\temp\orrock\points-all.shp -rl y:\dhi\global\fpar_8\dhi_2003_fpar8.tif,y:\dhi\global\fpar_8\dhi_2004_fpar8.tif,y:\dhi\global\fpar_8\dhi_2005_fpar8.tif,y:\dhi\global\fpar_8\dhi_2006_fpar8.tif,y:\dhi\global\fpar_8\dhi_2007_fpar8.tif,y:\dhi\global\fpar_8\dhi_2008_fpar8.tif,y:\dhi\global\fpar_8\dhi_2009_fpar8.tif,y:\dhi\global\fpar_8\dhi_2010_fpar8.tif,y:\dhi\global\fpar_8\dhi_2011_fpar8.tif,y:\dhi\global\fpar_8\dhi_2012_fpar8.tif,y:\dhi\global\fpar_8\dhi_2013_fpar8.tif,y:\dhi\global\fpar_8\dhi_2014_fpar8.tif

for /L %i in (2003,1,2014) DO (
    xcopy test.* %i.*
    python e:\users\maxim\Programming\python\extract_values\extract_values.py %i.shp -g -d x:\MCD15A3\%i\tif-lai-qa\ -e tif
)
xcopy test.* combined.*
python e:\users\maxim\Programming\python\extract_values\extract_values.py combined.shp -g -rl y:\dhi\global\lai_4\combined-v3\dhi_lai4qa_f.tif

python get_unique.py fill-values-search\MCD15A3-lai-qa.txt -fs x:\MCD15A3\2003\tif-lai-qa\,x:\MCD15A3\2004\tif-lai-qa\,x:\MCD15A3\2005\tif-lai-qa\,x:\MCD15A3\2006\tif-lai-qa\,x:\MCD15A3\2007\tif-lai-qa\,x:\MCD15A3\2008\tif-lai-qa\,x:\MCD15A3\2009\tif-lai-qa\,x:\MCD15A3\2010\tif-lai-qa\,x:\MCD15A3\2011\tif-lai-qa\,x:\MCD15A3\2012\tif-lai-qa\,x:\MCD15A3\2013\tif-lai-qa\,x:\MCD15A3\2014\tif-lai-qa\