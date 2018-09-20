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
import datetime


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

download = False
cloud_filter = False

# pclient init
pclient = PClientV1(api_key, config)

# # build a valid dt string from a month number
# def dt_construct(month, day = 1, year = 2018, t = "00:00:00.000Z"):
#     return "{}-{:02d}-{:02d}T{}".format(year, month, day, t)

aoi = GeoUtils.define_aoi(x, y, cellSize)  # aoi by a cell grid x, y
# print(aoi)

geom = {}
scene_id = ''
output_file = ''
output_localfile = ''
# tms_uri = ''

# start_date = dt_construct(month = mo_start, day = day_start, year = yr_start)
# end_date = dt_construct(month = mo_end, day = day_end, year = yr_end)
# step = datetime.timedelta(days=1)
start = datetime.datetime(yr_start, mo_start, day_start, 0, 0, 0)
# start2 = datetime.datetime(yr_start, mo_start, day_start, 23, 59, 59)
end = datetime.datetime(yr_end, mo_end, day_end, 0, 0, 0, 0)
# step = datetime.timedelta(days=1)
start_date = start.strftime('%Y-%m-%dT%H:%M:%SZ')
end_date = end.strftime('%Y-%m-%dT%H:%M:%SZ')

# 
planet_filters = pclient.set_filters_sr(aoi, start_date, end_date)
# # print(planet_filters)
res = pclient.request_intersecting_scenes(planet_filters)
# # print(res)
# 
# # pick up scene id and its geometry
for item in res.items_iter(pclient.maximgs):
    # each item is a GeoJSON feature
     geom = shape(geojson.loads(json.dumps(item["geometry"])))
     scene_id = item["id"]
     print("Matching scene ID: " + scene_id)
     
     if download:
        print("...Downloading " + scene_id)
        # output_file = pclient.download_localfs_analytic_sr(scene_id)
     
     if cloud_filter:
        bbox_local = GeoUtils.define_BoundingBox(x, y, cellSize)
        # print(bbox_local)
        
       # nodata percentage
       # nodata_perc = nodata_stats(output_file, bbox_local)
       
       # use custom cloud detection function to calculate clouds and shadows
       # cloud_perc, shadow_perc = cloud_stats(output_file, bbox_local, cloud_config)
       # check if cell grid is good enough
       # if (cloud_perc <= pclient.max_clouds and nodata_perc <= pclient.max_nodata):
           # break
     # else:
           # scene_id = ''
                                      
                                        
# # For each day, find the corresponding scene ids that pass filters
# while start <= end:
#     # print(start)
#     s  = start.strftime('%Y-%m-%dT%H:%M:%SZ')
#     s2  = start2.strftime('%Y-%m-%dT%H:%M:%SZ')
#     # print(s)
#     # print(s2)
#     start += step
#     start2 += step
#     planet_filters = pclient.set_filters_sr(aoi, s, s2)
#     res = pclient.request_intersecting_scenes(planet_filters)
#     
#     print("Querying scenes for " + start.strftime('%Y-%m-%d'))
#     print(str(res))
    
    # loop through all scenes for day
    # for item in res.items_iter(pclient.maximgs):
    #     geom = shape(geojson.loads(json.dumps(item["geometry"])))
    #     scene_id = item["id"]
    #     print(item)
        # if scene_id:
        #     print(scene_id)
        # else: 
        #     print("...no scene")
                                        
