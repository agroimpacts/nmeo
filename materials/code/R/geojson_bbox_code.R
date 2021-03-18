library(geojsonio)
library(sf)


##geojson from coordinats
coordinates_poly <- read.csv("/Users/michaelcecil/Rprojects/zamPods/makulu_coords.csv")
geojson_write(coordinates_poly,
              lat = "lat",
              lon = "lon",
              geometry = "polygon",
              group = "group",
              file = "myfile.geojson")


##geojson from shapefile
choma <- sf::read_sf("/Users/michaelcecil/Downloads/choma/choma.shp")
choma_geojson <- file_to_geojson("/Users/michaelcecil/Downloads/choma/choma.shp",
                                 method = 'local')


##bounding box from shapefil
choma_bbox <- sf::st_bbox(choma)

