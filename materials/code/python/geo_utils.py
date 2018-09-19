import math
from rasterio.coords import BoundingBox
from rasterio import transform
from shapely.geometry import box

class GeoUtils():
    @classmethod
    def window_inside_bounds(self, window, bounds):
        w, h = bounds
        ((start_row, stop_row), (start_col, stop_col)) = window
        return ((start_col <= w) and (stop_col <= w)) and ((start_row <= h) and (stop_row <= h))

    @classmethod
    def window_transform(self, window_min, window_max):
        start_row, stop_row = sorted([window_min[0], window_max[0]])
        start_col, stop_col = sorted([window_min[1], window_max[1]])
        return ((start_row, stop_row), (start_col, stop_col))

    @classmethod
    def extent_to_windows(self, extent, actual_transform):
        window_min = transform.rowcol(actual_transform, extent['xmin'], extent['ymin'])
        window_max = transform.rowcol(actual_transform, extent['xmax'], extent['ymax'])
        return self.window_transform(window_min, window_max)

    @classmethod
    def bounds_to_windows(self, bounds, grid):
        window_min = grid.index(bounds.left, bounds.bottom)
        window_max = grid.index(bounds.right, bounds.top)
        return self.window_transform(window_min, window_max)

    # returns extent by centroid and cellgrid resolution
    @classmethod
    def define_extent(self, x, y, cellSize):
        xSize, ySize = cellSize

        xmin = x - xSize
        xmax = x + xSize
        ymin = y - ySize
        ymax = y + ySize

        return {
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax
        }

    @classmethod
    def BoundingBox_to_extent(self, bbox):
        return {
            "xmin": bbox.left,
            "xmax": bbox.right,
            "ymin": bbox.bottom,
            "ymax": bbox.top
        }

    @classmethod
    def extent_to_BoundingBox(self, extent):
        return BoundingBox(extent['xmin'], extent['ymin'], extent['xmax'], extent['ymax'])

    @classmethod
    def define_BoundingBox(self, x, y, cellSize):
        return self.extent_to_BoundingBox(self.define_extent(x, y, cellSize))

    @classmethod
    def polygon_to_extent(self, polygon):
        # (minx, miny, maxx, maxy)
        # geom.bounds
        return {
            "xmin": polygon.bounds[0],
            "xmax": polygon.bounds[2],
            "ymin": polygon.bounds[1],
            "ymax": polygon.bounds[3]
        }

    @classmethod
    def extent_to_polygon(self, extent):
        return box(extent['xmin'], extent['ymin'], extent['xmax'], extent['ymax'])
 
    @classmethod
    def bounds_to_extent(self, bounds):
        return {
            "xmin": bounds[0],
            "xmax": bounds[2],
            "ymin": bounds[1],
            "ymax": bounds[3]
        }

    @classmethod
    def extents_intersects(self, ext1, ext2):
        return (not ((ext2['xmax'] < ext1['xmin']) | (ext2['xmin'] > ext1['xmax']))) & (not ((ext2['ymax'] < ext1['ymin']) | (ext2['ymin'] > ext1['ymax'])))

    @classmethod
    def extent_intersection(self, ext1, ext2):
        xminNew = ext1['xmin']
        yminNew = ext1['ymin']
        xmaxNew = ext1['xmax']
        ymaxNew = ext1['ymax']
        if(ext1['xmin'] < ext2['xmin']): 
            xminNew = ext2['xmin']
        if(ext1['ymin'] < ext2['ymin']):
            yminNew = ext2['ymin']
        if(ext1['xmax'] > ext2['xmax']):
            xmaxNew = ext2['xmax']
        if(ext1['ymax'] > ext2['ymax']):
            ymaxNew = ext2['ymax']

        return {
            "xmin": xminNew,
            "xmax": xmaxNew,
            "ymin": yminNew,
            "ymax": ymaxNew
        }

    @classmethod
    def define_polygon(self, x, y, cellSize):
        return self.extent_to_polygon(self.define_extent(x, y, cellSize))

    @classmethod
    def define_aoi(self, x, y, cellSize):
        extent = self.define_extent(x, y, cellSize)
        xmin = extent['xmin']
        xmax = extent['xmax']
        ymin = extent['ymin']
        ymax = extent['ymax']

        aoi = {
            'type': 'Polygon',
            'coordinates': [
                    [
                        [
                            xmin,
                            ymin
                        ],
                        [
                            xmax,
                            ymin
                        ],
                        [
                            xmax,
                            ymax
                        ],
                        [
                            xmin,
                            ymax
                        ],
                        [
                            xmin,
                            ymin
                        ]
                    ]
            ]
        }
        return aoi
