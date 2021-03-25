library(geojsonio)
library(sf)


##geojson from coordinats
coordinates_poly <- read.csv("/Users/michaelcecil/Rprojects/geog287387_s/materials/data/Zambia/boundaries/makulu_coords.csv")
geojson_write(coordinates_poly,
              lat = "lat",
              lon = "lon",
              geometry = "polygon",
              group = "group",
              file = "ZARI_makulu.geojson")


##geojson from shapefile
whittier_geojson <- file_to_geojson("/Users/michaelcecil/Rprojects/geog287387_s/materials/data/whittier/whittier_aoi/whittier_shp.shp",
                                 method = 'local')


##bounding box from shapefile
whittier <- sf::read_sf("/Users/michaelcecil/Rprojects/geog287387_s/materials/data/whittier/whittier_aoi/whittier_shp.shp")
whittier_bbox <- sf::st_bbox(whittier)

