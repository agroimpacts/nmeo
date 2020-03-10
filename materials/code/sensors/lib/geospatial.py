import numpy as np
import pandas as pd
import descarteslabs as dl

LS = "landsat:LC08:01:RT:TOAR"
S2 = "sentinel-2:L1C"

def get_bands_from_platform(platform):
    if platform == S2:
        bands=["blue","green","red", "red-edge-2","nir","water-vapor","ndvi", "alpha"]
        scales=[[0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 65535, -1, 1], 
                None]
    elif platform == LS:
        bands=["blue","green","red","nir","ndvi", "alpha"]
        scales=[[0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 10000, 0, 1], 
                [0, 65535, -1, 1], 
                None]
        
    return bands, scales

def aoi_from_latlon(ylat, xlong):
    """
    Example:
    lat = 38.459702
    long = -122.438332

    aoi = aoi_from_latlon(lat, long)
    
    """

    # Intent is for an AOI of a single pixel
    
    # Approx 12 cm, ie <1m
    dx = 0.000001 
    dy = 0.000001

    aoi = {
        "type": "Polygon",
        "coordinates": [
            [
                [xlong, ylat],
                [xlong, ylat+dy],
                [xlong+dx, ylat+dy],
                [xlong+dx, ylat],
                [xlong, ylat],
            ]
        ],
    }
    
    return aoi


def fc_from_latlong(lat, long, start="2018-01-01", end="2018-12-31", platform="sentinel-2:L1C"):
    
    """
    Platforms:
    landsat = "landsat:LC08:01:RT:TOAR"
    sentinel2 = "sentinel-2:L1C"
    """

    aoi = aoi_from_latlon(lat, long)
    
    metadata_client = dl.Metadata()

    # Image Search
    fc = metadata_client.search(
        products=platform,
        geom=aoi,
        start_datetime=start,
        end_datetime=end,
        limit=365,
    )

    return fc
    
    
def meta_from_fc(fc, fmt="dict"):
    
    """
    Collects key parameters of the scenes in a feature collection
    
    j = meta_from_fc(fc, fmt="dict")
    
    """

    fid = [""] * nk
    datestring = [""] * nk

    cirrus_fraction = [np.nan] * nk
    cloud_fraction = [np.nan] * nk
    opaque_fraction = [np.nan] * nk
    solar_azimuth_angle = [np.nan] * nk
    solar_elevation_angle = [np.nan] * nk
    view_angle = [np.nan] * nk
    azimuth_angle = [np.nan] * nk

    raa = [np.nan] * nk
    sza = [np.nan] * nk
    vza = [np.nan] * nk

    for k in range(nk):

        fid[k] = fc[k]['id']
        datestring[k] = fc[k]['properties']['acquired']

        image = images[k]
        ndvi[k] = image[10,10,0]

        azimuth_angle[k] = fc[k]['properties']['azimuth_angle']*np.pi/180.
        cirrus_fraction[k] = fc[k]['properties']['cirrus_fraction']
        cloud_fraction[k] = fc[k]['properties']['cloud_fraction']
        degraded_fraction_0[k] = fc[k]['properties']['degraded_fraction_0']
        opaque_fraction[k] = fc[k]['properties']['opaque_fraction']
        solar_azimuth_angle[k] = fc[k]['properties']['solar_azimuth_angle']*np.pi/180.
        solar_elevation_angle[k] = fc[k]['properties']['solar_elevation_angle']
        view_angle[k] = fc[k]['properties']['view_angle']
        raa[k] = np.sin(solar_azimuth_angle[k] - azimuth_angle[k])
        sza[k] = np.cos((90. - solar_elevation_angle[k])*np.pi/180.)
        vza[k] = np.cos((view_angle[k])*np.pi/180.)

    data = {
            'fid': fid,
            'utc': datestring, 
            'ndvi': ndvi,
            'cirrus_fraction': cirrus_fraction,
            'cloud_fraction': cloud_fraction,
            'opaque_fraction': opaque_fraction,
            'raa': raa,
            'cossza': sza,
            'cosvza': vza,
           }

    df = pd.DataFrame(data=data)
    df['utc'] = pd.to_datetime(df['utc'])
    df['date'] = df['utc'].dt.date
    df = df.sort_values('utc')

    columns = ['date','utc','fid', 'cossza', 'cosvza', 'raa', 
       'cirrus_fraction', 'cloud_fraction', 'opaque_fraction']
    df = df[columns]

   
    if fmt == "dict":
        j = df.to_dict(orient='split')
        
        # df = pd.DataFrame.from_records(data=j['data'], columns = j['columns'])
    elif fmt == "json":
        j = df.to_json(orient='split', date_format='iso', double_precision=4, date_unit='s')
        
        # j = json.loads(jstring)
        # df = pd.DataFrame.from_records(data=j['data'], columns = j['columns'])
    else:
        j = df
        
    return j    

def images_from_fids(aoi, fids):    
    
    raster_client = dl.Raster()

    images = list()
    for f in fids:
        feat_id = feat["id"]
        arr, meta = raster_client.ndarray(
            f,
            cutline=aoi,
            bands=["ndvi", "alpha"],
            scales=[[0, 65535, -1, 1], None],
            data_type="Float32",
        )
        images.append(arr)
        
    return images, meta['wgs84Extent']


def dims_from_images(images):
    nk = len(images)
    ni = len(images[0])
    nj = len(images[0][0])
    nb = len(images[0][0][0])
    
    dims = {
        'nk': nk,
        'ni': ni,
        'nj': nj,
        'nb': nb
    }
    
    return dims

def pixel_from_latlong(meta, dims, lat, long):
    
    xmeta, ymeta = zip(*meta['wgs84Extent']['coordinates'][0])

    dx = max(xmeta)-min(xmeta)
    dy = max(ymeta)-min(ymeta)

    nk = dims['nk']
    ni = dims['ni']
    nj = dims['nj']

    dxdP = dx/ni
    dydP = dy/nj

    ix = int((long - min(xmeta))/dxdP)
    jy = int((max(ymeta) - lat)/dydP)
    
    px = {
        'ix': ix,
        'jy': jy
    }
    
    return px

def images_to_timeseries(fc, images, platform, dims, px):
    
    nk = dims['nk']
    ix = px['ix']
    jy = px['jy']    

    blue = np.zeros((nk))
    green = np.zeros((nk))
    red = np.zeros((nk))
    nir = np.zeros((nk))
    ndvi = np.zeros((nk))
    datestring = [""] * nk

    if platform == S2:
        red_edge_2 = np.zeros((nk))
        water_vapor = np.zeros((nk))


    for k in range(nk):
        image = images[k]
        if platform == S2:
            blue[k] = image[ix,jy,0]
            green[k] = image[ix,jy,1]
            red[k] = image[ix,jy,2]
            red_edge_2[k] = image[ix,jy,3]
            nir[k] = image[ix,jy,4]
            water_vapor[k] = image[ix,jy,5]
            ndvi[k] = image[ix,jy,6]
        else:
            blue[k] = image[ix,jy,0]
            green[k] = image[ix,jy,1]
            red[k] = image[ix,jy,2]
            nir[k] = image[ix,jy,3]
            ndvi[k] = image[ix,jy,4]

        datestring[k] = fc["features"][k]['properties']['acquired']  

    if platform == S2:
        d = {'UTC': datestring, 
            'blue': blue,
            'green': green,
            'red': red,
            'red-edge-2': red_edge_2,
            'nir': nir,
            'water-vapor': water_vapor,
            'ndvi': ndvi}
    else:
        d = {'UTC': datestring, 
            'blue': blue,
            'green': green,
            'red': red,
            'nir': nir,
            'ndvi': ndvi} 
    
    df = pd.DataFrame(data=d)
    df['UTC'] = pd.to_datetime(df['UTC'])
    df = df.sort_values('UTC')    

    return df