from planet_client import PClientV1
from filter_callable import cloud_shadow_stats_config_wraped as cloud_stats
from filter_callable import nodata_stats_wraped as nodata_stats
from geo_utils import GeoUtils
import configparser
from shapely.geometry import shape
from geojson import Polygon, MultiPolygon
import geojson
import json
import logging


# read configuration
config = configparser.ConfigParser()
config.read('config.ini')
planet_config = config['planet']
imagery_config = config['imagery']
cloud_config = config['cloud_shadow']
aoi_config = config['aoi']
date_config = config['dates']

# specific variables
api_key = planet_config['api_key']
# catalog_path = imagery_config['catalog_path'] # EPSG:4326
x = float(aoi_config['x'])
y = float(aoi_config['y'])
cellSize = [0.0025, 0.0025]
mo_start = int(date_config['month_start'])
mo_end = int(date_config['month_end'])
day_start = int(date_config['day_start'])
day_end = int(date_config['day_end'])
yr_start = int(2018)
yr_end = yr_start

# logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(format = '%(message)s', datefmt = '%m-%d %H:%M')

# print(api_key)
# print(image_path)

# pclient init
pclient = PClientV1(api_key, config)
# print(pclient)

# build a valid dt string from a month number
def dt_construct(month, day = 1, year = 2018, t = "00:00:00.000Z"):
    return "{}-{:02d}-{:02d}T{}".format(year, month, day, t)

aoi = GeoUtils.define_aoi(x, y, cellSize)  # aoi by a cell grid x, y
# print(aoi)

geom = {}
scene_id = ''
output_file = ''
output_localfile = ''
# tms_uri = ''

start_date = dt_construct(month = mo_start, day = day_start, year = yr_start)
end_date = dt_construct(month = mo_end, day = day_end, year = yr_end)
# print(start_date)
# print(end_date)
planet_filters = pclient.set_filters_sr(aoi, start_date, end_date)
# print(planet_filters)
res = pclient.request_intersecting_scenes(planet_filters)
# print(res)

# pick up scene id and its geometry
for item in res.items_iter(pclient.maximgs):
    # each item is a GeoJSON feature
     geom = shape(geojson.loads(json.dumps(item["geometry"])))
     scene_id = item["id"]
     print(scene_id)
     # print(geom)
     
     # output_file = pclient.download_localfs_analytic_sr(scene_id)

     # cleanup local catalog to remove previous iterations files
     # pclient.cleanup_catalog()
     # # activation & download
     # # it should be sync, to allow async check of neighbours
     # output_localfile, output_file = pclient.download_localfs_s3(scene_id, season = season_type)
     # 
     # bbox_local = GeoUtils.define_BoundingBox(x, y, cellSize)
     # print(bbox_local)
     # nodata percentage
     # nodata_perc = nodata_stats(output_file, bbox_local)
     # use custom cloud detection function to calculate clouds and shadows
     # cloud_perc, shadow_perc = cloud_stats(output_file, bbox_local, cloud_config)
     # # check if cell grid is good enough
     # if (cloud_perc <= pclient.max_clouds and nodata_perc <= pclient.max_nodata):
     #     break
     # else: 
     #     scene_id = ''
         
                                        
                                        
                                        
                                        
