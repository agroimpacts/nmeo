from planet import api
from planet.api import filters
from geo_utils import GeoUtils
from pprint import pprint
from requests.auth import HTTPBasicAuth
from fixed_thread_pool_executor import FixedThreadPoolExecutor

import os
import ssl
import requests
import time
import urllib.request
import shutil
import boto3
from boto3.s3.transfer import S3Transfer, TransferConfig
import botocore
import concurrent
import logging
import configparser
import json
import multiprocessing
from retry import retry

# PClientV1, class to simplify querying & downloading planet scenes using planet API V1
# We need to consider usage of a new API
class PClientV1():
    # def __init__(self, api_key):
    #     self.api_key = api_key
    #     self.max_clouds = 0.25
    #     self.max_bad_pixels = 0.25
    #     self.max_nodata = 0.25
    #     self.maximgs = 1
    #     self.catalog_path = "catalog/"
    #     self.s3_catalog_bucket = "azavea-africa-test"
    #     self.s3_catalog_prefix = "planet/images"
    #     self.products = {
    #         'analytic_sr': {
    #             'item_type': 'PSScene4Band',
    #             'asset_type': 'analytic_sr',
    #             'ext': 'tif'
    #         },
    #         'analytic': {
    #             'item_type': 'PSScene4Band',
    #             'asset_type': 'analytic',
    #             'ext': 'tif'
    #         },
    #         'analytic_xml': {
    #             'item_type': 'PSScene4Band',
    #             'asset_type': 'analytic_xml',
    #             'ext': 'xml'
    #         },
    #         'visual': {
    #             'item_type': 'PSScene3Band',
    #             'asset_type': 'visual',
    #             'ext': 'tif'
    #         }
    #     }
    #     self.client = api.ClientV1(api_key = api_key)
    #     self.output_filename = "output.csv"
    #     self.output_encoding = "utf-8"
    #     self.s3client = boto3.client('s3')
    #     self.with_analytic = False
    #     self.with_analytic_xml = False
    #     self.with_visual = False
    #     self.local_mode = False
    #     self.s3_only = False
    #     self.transfer = S3Transfer(self.s3client, TransferConfig(use_threads = False))
    #     self.transfer_config = TransferConfig(use_threads = False)
    #     self.logger = logging.getLogger(__name__)
    #     self.logger.setLevel(logging.INFO)
    #     self.secondary_uploads_executor = FixedThreadPoolExecutor(size = 5)
    #     self.with_immediate_cleanup = False

    def __init__(self, api_key, config):
        imagery_config = config['imagery']
        self.api_key = api_key
        self.max_clouds_initial = float(imagery_config['max_clouds_initial'])
        self.max_clouds = float(imagery_config['max_clouds'])  # max proportion of pixels that are clouds
        self.max_bad_pixels = float(imagery_config['max_bad_pixels']) # max proportion of bad pixels (transmission errors, etc.)
        self.max_nodata = float(imagery_config['max_nodata']) # max nodata values per cellgrid
        self.maximgs = int(imagery_config['maximgs'])  # 15 #10 #20
        self.output_encoding = imagery_config['output_encoding']
        # self.output_filename = imagery_config['output_filename']
        # self.output_filename_csv = imagery_config['output_filename_csv']
        self.catalog_path = imagery_config['catalog_path']
        # self.s3_catalog_bucket = imagery_config['s3_catalog_bucket']
        # self.s3_catalog_prefix = imagery_config['s3_catalog_prefix']
        self.products = {
            'analytic_sr': {
                'item_type': 'PSScene4Band',
                'asset_type': 'analytic_sr',
                'ext': 'tif'
            },
            'analytic': {
                'item_type': 'PSScene4Band',
                'asset_type': 'analytic',
                'ext': 'tif'
            },
            'analytic_xml': {
                'item_type': 'PSScene4Band',
                'asset_type': 'analytic_xml',
                'ext': 'xml'
            },
            'visual': {
                'item_type': 'PSScene3Band',
                'asset_type': 'visual',
                'ext': 'tif'
            }
        }
        self.client = api.ClientV1(api_key = self.api_key)
        self.s3client = boto3.client('s3')
        # self.with_analytic = json.loads(imagery_config['with_analytic'].lower())
        # self.with_analytic_xml = json.loads(imagery_config['with_analytic_xml'].lower())
        # self.with_visual = json.loads(imagery_config['with_visual'].lower())
        # self.with_immediate_cleanup = json.loads(imagery_config['with_immediate_cleanup'].lower())
        # self.local_mode = json.loads(imagery_config['local_mode'].lower())
        # self.s3_only = json.loads(imagery_config['s3_only'].lower())
        # self.transfer = S3Transfer(self.s3client, TransferConfig(use_threads = False))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # planet has limitation 5 sec per key (search queries)
        threads_number = imagery_config['threads']
        if threads_number == 'default':
            threads_number = multiprocessing.cpu_count() * 2 + 1
        else:
            threads_number = int(threads_number)

        self.secondary_uploads_executor = FixedThreadPoolExecutor(size = threads_number)

    # there are start_date and end_date present as it should be the part of a row retrieved from psql / tiff file
    def set_filters_sr(self, aoi, start_date='2017-12-15T00:00:00.000Z', end_date = '2018-03-15T00:00:00.000Z', id=''):
        # add an asset_filter for only those scenes that have an analytic_sr asset available
        date_filter = {
            'type': 'DateRangeFilter',
            'field_name': 'acquired',
            'config': {
                'gte': start_date,
                'lte': end_date
            }
        }

        cloud_filter = {
            'type': 'RangeFilter',
            'field_name': 'cloud_cover',
            'config': {
                'lte': self.max_clouds_initial
            }
        }

        bad_pixel_filter = {
            'type': 'RangeFilter',
            'field_name': 'anomalous_pixels',
            'config': {
                'lte': self.max_bad_pixels
            }
        }

        location_filter = api.filters.geom_filter(aoi)

        geometry_filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": aoi
        }

        asset_filter = {
            "type": "PermissionFilter",
            "config": ["assets.analytic_sr:download"]
        }

        string_filter = {
            "type": "StringInFilter",
            "field_name": "id",
            "config": [id]
        }

        filters_list = [date_filter, cloud_filter,geometry_filter, bad_pixel_filter, asset_filter]
        if (id != ''): 
            filters_list.append(string_filter)

        # combine filters:
        query = {
            'type': 'AndFilter',
            'config': filters_list
        }

        return query

    # there are start_date and end_date present as it should be the part of a row retrieved from psql / tiff file
    def set_filters_id(self, id=''):
        asset_filter = {
            "type": "PermissionFilter",
            "config": ["assets.analytic_sr:download"]
        }

        string_filter = {
            "type": "StringInFilter",
            "field_name": "id",
            "config": [id]
        }

        filters_list = [asset_filter, string_filter]

        # combine filters:
        query = {
            'type': 'AndFilter',
            'config': filters_list
        }

        return query

    @retry(tries = 10, delay = 2, backoff = 2)
    def request_intersecting_scenes(self, query):
        # build the request
        item_types = ['PSScene4Band']  # params["lst_item_types"]
        request = api.filters.build_search_request(query, item_types)

        # post the request
        results = self.client.quick_search(request)
        return results

    # returns a full URI here
    def download_localfs_generic(self, scene_id, season = '', asset_type = 'analytic_sr', ext = 'tif', item_type='PSScene4Band'):
        output_file = "{}{}/{}/{}.{}".format(self.catalog_path, asset_type, season, scene_id, ext)

        if not os.path.exists(output_file): 
            # activation & download
            session = requests.Session()
            session.auth = (self.api_key, '')
            assets_uri = ("https://api.planet.com/data/v1/item-types/{}/items/{}/assets/").format(item_type, scene_id)
                    
            assets_query_result = session.get(assets_uri)

            self.logger.info(assets_query_result.status_code)
            item_activation_json = assets_query_result.json()
            # self.logger.info(item_activation_json)
            item_activation_url = item_activation_json[asset_type]["_links"]["activate"]
            response = session.post(item_activation_url)
            self.logger.info(response.status_code)
            while response.status_code!=204:
                time.sleep(30)
                response = session.post(item_activation_url)
                response.status_code = response.status_code
                self.logger.info(response.status_code)

            item_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets/'.format(item_type, scene_id)
            result = requests.get(item_url, auth = HTTPBasicAuth(self.api_key, ''))
            
            if result.status_code != 200:
                self.logger.info(result.content.decode('utf-8'))

            download_url = result.json()[asset_type]['location']

            # download
            with urllib.request.urlopen(download_url) as response, open(output_file, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

        return output_file

    # TODO: lots of copy pasting happens there, abstract over it?
    # returns a full S3 URI here
    def download_s3_generic(self, scene_id, season = '', asset_type = 'analytic_sr', ext = 'tif', item_type='PSScene4Band'):
        output_key = "{}/{}/{}/{}.{}".format(self.s3_catalog_prefix, asset_type, season, scene_id, ext)
        result_path = 's3://{}/{}'.format(self.s3_catalog_bucket, output_key)

        try:
            self.s3client.head_object(Bucket = self.s3_catalog_bucket, Key = output_key)
        except botocore.exceptions.ClientError:
            self.logger.exception('Error Encountered')
            self.logger.info("Downloading {}...".format(scene_id))

            # activation & download
            session = requests.Session()
            session.auth = (self.api_key, '')
            assets_uri = ("https://api.planet.com/data/v1/item-types/{}/items/{}/assets/").format(item_type, scene_id)
                    
            assets_query_result = session.get(assets_uri)

            self.logger.info(assets_query_result.status_code)
            item_activation_json = assets_query_result.json()
            # self.logger.info(item_activation_json)
            item_activation_url = item_activation_json[asset_type]["_links"]["activate"]
            response = session.post(item_activation_url)
            self.logger.info(response.status_code)
            while response.status_code!=204:
                time.sleep(30)
                response = session.post(item_activation_url)
                response.status_code = response.status_code
                self.logger.info(response.status_code)

            item_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets/'.format(item_type, scene_id)
            result = requests.get(item_url, auth = HTTPBasicAuth(self.api_key, ''))

            if result.status_code != 200:
                self.logger.info(result.content.decode('utf-8'))

            download_url = result.json()[asset_type]['location']

            # upload on s3 directly from the response
            with urllib.request.urlopen(download_url) as response:
                self.s3client.put_object(Body = response.read(), Bucket = self.s3_catalog_bucket, Key = output_key)

            # finished
            self.logger.info("Downloaded {}".format(scene_id))

        return result_path

    # returns a full URI here
    def download_localfs_product(self, product_type, scene_id, season = ''):
        cfg = self.products[product_type]
        return self.download_localfs_generic(
            scene_id = scene_id, 
            season = season, 
            asset_type = cfg['asset_type'], 
            ext = cfg['ext'], 
            item_type= cfg['item_type']
        )

    # returns a full URI here
    def download_s3_product(self, product_type, scene_id, season = ''):
        cfg = self.products[product_type]
        return self.download_s3_generic(
            scene_id = scene_id, 
            season = season, 
            asset_type = cfg['asset_type'], 
            ext = cfg['ext'], 
            item_type= cfg['item_type']
        )

    def download_localfs_analytic_sr(self, scene_id, season = ''):
        return self.download_localfs_product('analytic_sr', scene_id, season)

    def download_s3_analytic_sr(self, scene_id, season = ''):
        return self.download_s3_product('analytic_sr', scene_id, season)

    def download_localfs_analytic(self, scene_id, season = ''):
        return self.download_localfs_product('analytic', scene_id, season)

    def download_s3_analytic(self, scene_id, season = ''):
        return self.download_s3_product('analytic', scene_id, season)

    def download_localfs_analytic_xml(self, scene_id, season = ''):
        return self.download_localfs_product('analytic_xml', scene_id, season)

    def download_s3_analytic_xml(self, scene_id, season = ''):
        return self.download_s3_product('analytic_xml', scene_id, season)

    def download_localfs_visual(self, scene_id, season = ''):
        return self.download_localfs_product('visual', scene_id, season)

    def download_s3_visual(self, scene_id, season = ''):
        return self.download_s3_product('visual', scene_id, season)

    def upload_s3_csv(self):
        result = ''
        if not self.local_mode:
            output_key = "{}/{}".format(self.s3_catalog_prefix, self.output_filename.split('/')[-1])
            result = 's3://{}/{}'.format(self.s3_catalog_bucket, output_key)
            self.transfer.upload_file(self.output_filename, self.s3_catalog_bucket, output_key)
        else:
            result = self.output_filename
        
        return result

    def upload_s3_csv_csv(self):
        output_key = "{}/{}".format(self.s3_catalog_prefix, self.output_filename_csv.split('/')[-1])
        result = 's3://{}/{}'.format(self.s3_catalog_bucket, output_key)
        self.transfer.upload_file(self.output_filename_csv, self.s3_catalog_bucket, output_key)
        return result

    def download_localfs_s3_product(self, scene_id, season = '', product_type = 'analytic_sr'):
        cfg = self.products[product_type]
        asset_type = cfg['asset_type'] 
        ext = cfg['ext']
        item_type = cfg['item_type']

        filepath = ''
        output_key = "{}/{}/{}/{}.{}".format(self.s3_catalog_prefix, asset_type, season, scene_id, ext)
        s3_result = 's3://{}/{}'.format(self.s3_catalog_bucket, output_key)
        local_result = "{}{}/{}/{}.{}".format(self.catalog_path, asset_type, season, scene_id, ext)

        if not self.s3_only:
            if not os.path.exists(local_result):
                if not self.local_mode:
                    try:
                        # if we have file in our s3 bucket, let's pull it down from the S3 (faster)
                        self.s3client.head_object(Bucket = self.s3_catalog_bucket, Key = output_key)
                        filepath = s3_result
                        # self.logger.info("Downloading {} from the internal S3 storage...".format(scene_id))
                        # self.transfer.download_file(self.s3_catalog_bucket, output_key, local_result)
                        # filepath = local_result # filepath = s3_result
                    except botocore.exceptions.ClientError:
                        self.logger.exception('Error Encountered')
                        filepath = self.download_localfs_product(product_type, scene_id, season)
                        self.logger.info("Uploading {}...".format(scene_id))
                        self.s3client.put_object(Bucket = self.s3_catalog_bucket, Key = output_key, Body = open(filepath, 'rb'))
                        # self.transfer.upload_file(filepath, self.s3_catalog_bucket, output_key)
                else:
                    filepath = self.download_localfs_product(product_type, scene_id, season)
                    s3_result = local_result
            else:
                filepath = local_result
                if self.local_mode:
                    s3_result = local_result
                else:
                    try:
                        self.s3client.head_object(Bucket = self.s3_catalog_bucket, Key = output_key)
                    except botocore.exceptions.ClientError:
                        self.logger.exception('Error Encountered')
                        self.logger.info("Uploading {}...".format(scene_id))
                        self.s3client.put_object(Bucket = self.s3_catalog_bucket, Key = output_key, Body = open(filepath, 'rb'))
                        # self.transfer.upload_file(filepath, self.s3_catalog_bucket, output_key)
        else:
            s3_result = self.download_s3_product('analytic_sr', scene_id, season)
            filepath = s3_result

        return filepath, s3_result

    def download_localfs_s3(self, scene_id, season = ''):
        sub_products = []
        if self.with_analytic:
            sub_products.append('with_analytic')

        if self.with_analytic_xml:
            sub_products.append('with_analytic_xml')

        if self.with_visual:
            sub_products.append('with_visual')

        for sub_product in sub_products:
            self.secondary_uploads_executor.submit(self.download_localfs_s3_product, scene_id, season, sub_product)

        return self.download_localfs_s3_product(scene_id, season)


    def drain(self):
        self.secondary_uploads_executor.drain()

    # def cleanup_catalog(self):
    #     self.logger.info("Catalog cleanup...")
    #     if self.with_immediate_cleanup & (not self.s3_only):
    #         for product_type in ['analytic', 'analytic_sr', 'analytic_xml', 'visual']:
    #             for season in ['OS', 'GS']:
    #                 lpath = "{}{}/{}".format(self.catalog_path, product_type, season)
    #                 try:
    #                     shutil.rmtree(lpath, ignore_errors = False)
    #                     os.makedirs(lpath)
    #                 except:
    #                     self.logger.exception('Error Encountered')
    #                     self.logger.info("Could not remove a folder: {}".format(lpath))


    def close(self):
        self.secondary_uploads_executor.close()
        self.cleanup_catalog()


if __name__ == "__main__":
    # disable ssl
    ssl._create_default_https_context = ssl._create_unverified_context

    # read config
    config = configparser.ConfigParser()
    config.read('cfg/config.ini')
    planet_config = config['planet']
    imagery_config = config['imagery']

    # logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.basicConfig(format = '%(message)s', datefmt = '%m-%d %H:%M')

    api_key = planet_config['api_key']

    # pclient init
    pclient = PClientV1(api_key, config)

    # planet_filters = pclient.set_filters_id('20170828_092138_0f4b')

    # res = pclient.request_intersecting_scenes(planet_filters)
    # pick up scene id and its geometry
    # for item in res.items_iter(1):
        # each item is a GeoJSON feature
        # scene_id = item["id"]
        # print(item)
        # activation & download
        # it should be sync, to allow async check of neighbours
        # output_localfile = pclient.download_localfsV2(scene_id, asset_type = 'visual', item_type='PSScene3Band')
        # output_localfile = pclient.download_localfsV2(scene_id, asset_type = 'visual_xml', item_type='PSScene3Band', ext = 'xml')
        # output_localfile = pclient.download_localfsV2(scene_id, asset_type = 'analytic')
        # output_localfile = pclient.download_localfsV2(scene_id, asset_type = 'analytic_xml', ext = 'xml')
        # use custom cloud detection function to calculate clouds and shadows
    
