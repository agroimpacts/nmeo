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
import rasterio
from rasterio.mask import mask
from rasterio.coords import BoundingBox
from rasterio import transform
from rasterio.warp import transform_bounds
from rasterio.windows import Window
# from subprocess import call

# read configuration
config = configparser.ConfigParser()
config.read('config.ini')
planet_config = config['planet']
imagery_config = config['imagery']
cloud_config = config['cloud_shadow']
aoi_config = config['aoi']
date_config = config['dates']
processing_config = config['processing']

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
# download = processing_config['download']
cloud_filter = processing_config['cloud_filter']
crop = processing_config['crop']
max_clouds = float(imagery_config['max_clouds'])
max_shadows = float(imagery_config['max_shadows'])
max_nodata = float(imagery_config['max_nodata'])
output_path = imagery_config['catalog_path']

# logger
# logger = logging.getLogger(__x name__)
# logger.setLevel(logging.INFO)
# logging.basicConfig(format = '%(message)s', datefmt = '%m-%d %H:%M')

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
     print(".Downloading " + scene_id)
     output_file = pclient.download_localfs_analytic_sr(scene_id)
     
     if cloud_filter:
        bbox_local = GeoUtils.define_BoundingBox(x, y, cellSize)
        # print(bbox_local)
        
        # nodata percentage
        nodata_perc = nodata_stats(output_file, bbox_local)
        print("..No data pixels in image: " + str(nodata_perc))
       
        # use custom cloud detection function to calculate clouds and shadows
        cloud_perc, shadow_perc = cloud_stats(output_file, bbox_local, 
                                              cloud_config)
        print("..Cloudy pixels in AOI: " + str(cloud_perc) + 
              "; Shadow pixels in AOI: " + str(shadow_perc))
        
        # check if cell grid is clear enough
        if (cloud_perc <= max_clouds and shadow_perc <= max_shadows and 
            nodata_perc <= max_nodata):
            print("...Scene is clear for your AOI")
        
            if crop:
                src = rasterio.open(output_file)
                bounds = transform_bounds("EPSG:4326", src.crs, *bbox_local)
            
                bounds_window = src.window(*bounds)
                bounds_window = bounds_window.intersection(Window(
                    0, 0, src.width, src.height))

                # Get the window with integer height
                # and width that contains the bounds window.
                out_window = bounds_window.round_lengths(op='ceil')
                height = int(out_window.height)
                width = int(out_window.width)
            
                out_kwargs = src.profile
                out_kwargs.update({
                  'driver': "GTiff",
                  'height': height,
                  'width': width,
                  'transform': src.window_transform(out_window)})
               # out_kwargs.update(**creation_options)

                if 'blockxsize' in out_kwargs and out_kwargs['blockxsize'] > width:
                     del out_kwargs['blockxsize']
                if 'blockysize' in out_kwargs and out_kwargs['blockysize'] > height:
                     del out_kwargs['blockysize']
                   
                output = output_path + scene_id + "_aoi.tif"
                with rasterio.open(output, 'w', **out_kwargs) as out:
                     out.write(src.read(window=out_window,
                               out_shape=(src.count, height, width)))
                print("....Finished writing AOI " + output)
                print(" ")

               # gdal variant, depends on bounds_ext
               # bnds = "%s %s %s %s" % (bounds_ext["xmin"], bounds_ext["ymin"], bounds_ext["xmax"], 
               #         bounds_ext["ymax"])
               # output = output_path + scene_id + "_aoi.tif"
               # input = output_file
               # call("gdalwarp -te " + ' ' + bnds + ' ' + input + ' ' + output, 
               #       shell = True)
               # call()

        else:
            print("...Scene " + scene_id + " is not usable!!!") #scene_id = ''
            print(" ")                          
