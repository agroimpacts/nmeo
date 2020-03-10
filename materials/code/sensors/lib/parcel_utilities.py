import json
import requests
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

def clu_from_latlong(lat, long, clu_key, f='json'):
    url = 'https://ag-analytics.azure-api.net/CommonLandUnitBoundary/get'

    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': clu_key
    }

    geometry = {
            "xmin":long,
            "ymin":lat,
            "xmax":long+0.00001,
            "ymax":lat+0.00001,
            "spatialReference":{"wkid":4326}
        }

    params = {'geometry': json.dumps(geometry),
              'f': f
             }
    
    r = requests.get(url, params=params, headers=headers)
    
    return r.json()


def cdl_from_clu(year, clu, cdl_key):
    
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': cdl_key
    }

    year = 2018
    inputShape = {'geometryType': 'esriGeometryPolygon',
         'features': [{'geometry': clu['features'][0]['geometry']}],
         'spatialReference': {'wkid': 4326}         
         }
    env = 4326
    f = "json"

    baseurl = "https://ag-analytics.azure-api.net/CroplandDataLayers/get?"
    suffix = "year={}&inputShape={}&env:outSR={}&f={}".format(year,inputShape,env,f)
           
    r = requests.get(baseurl+suffix, headers=headers)
           
    return r.json()

def latlon_list_to_polygon(latlon_list):
    """points must be [lon, lat] order"""
    
    lons = [c[0] for c in latlon_list[0]]
    lats = [c[1] for c in latlon_list[0]]
    
    return Polygon(zip(lons, lats))

def cdl_to_gpd(cdl):
    """Convert CDL json to geopandas dataframe"""
    
    crs = cdl['results'][0]['value']['spatialReference']['wkid']
    crs_str = 'epsg:{}'.format(crs)
    
    atts = [{**k['attributes'], **k['geometry']} for k in cdl['results'][0]['value']['features']]
    
    df = pd.DataFrame(atts)
    df.rename(columns={'rings': 'geometry'}, inplace=True)
    df['geometry'] = df['geometry'].apply(latlon_list_to_polygon)
    
    return gpd.GeoDataFrame(df, crs=crs_str, geometry='geometry')


def aoi_from_clu(clu):
    aoi = clu['features'][0]['geometry']
    return aoi