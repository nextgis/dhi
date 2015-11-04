import os
import sys

gisbase = os.environ['GISBASE'] = "c:/tools/NextGIS_QGIS/apps/grass/grass-6.4.4/"
gisdbase = os.environ['GISDBASE'] = "e:/users/maxim/thematic/dhi/"
location = "dhi_grass"
mapset   = "PERMANENT"

sys.path.append(os.path.join(gisbase, "etc", "python"))
 
import grass.script as grass
import grass.script.setup as gsetup
gsetup.init(gisbase, gisdbase, location, mapset)
print grass.gisenv()