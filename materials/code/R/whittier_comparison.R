library(raster)
library(sf)
library(dplyr)
library(here)
library(lubridate)
library(ggplot2)

#test
s2_raster <- raster::stack("materials/data/whittier/sentinel_class_test_2018_08_26.tif")
l8_raster <- raster::stack("materials/data/whittier/landsat_class_test_2018_08_27.tif")
planet_raster <- raster::stack("materials/data/whittier/planet_class_test_2018_08_26.tif")
drone_raster <- raster::stack("materials/data/whittier/drone_2018_08_24/whittier_24aug18_pix4d_transparent_reflectance_green.tif",
                              "materials/data/whittier/drone_2018_08_24/whittier_24aug18_pix4d_transparent_reflectance_red.tif",
                              "materials/data/whittier/drone_2018_08_24/whittier_24aug18_pix4d_transparent_reflectance_nir.tif")

drone_crs = crs(drone_raster)
sentinel_crs = crs(s2_raster)
landsat_crs = crs(l8_raster)
planet_crs = crs(planet_raster)


## project all images to drone coordinate reference system
s2_raster_rpj <- projectRaster(s2_raster, crs = drone_crs )
l8_raster_rpj <- projectRaster(l8_raster, crs = drone_crs )
planet_raster_rpj <- projectRaster(planet_raster, crs = drone_crs )


## plot false color composite for each image
# RGB = (NIR, red, green) bands
# scale is used to determine how to map colors. 
# For Sentinel and Planet, surface reflectance is between 0 and 10000. 
# For Landsat and drone it is between 0 and 1. 
# However, we set the "scale" to half of the maximum value to make the colors brighter.
plotRGB(s2_raster_rpj, r =4, g = 3, b = 2, scale = 5000, colNA = "transparent", zlim = c(0, 5000) )
plotRGB(l8_raster_rpj, r =5, g = 4, b = 3, scale = 0.5, colNA = "transparent")
plotRGB(planet_raster_rpj, r =4, g = 3, b = 2, scale = 5000, colNA = "transparent")
plotRGB(drone_raster, r =3, g = 2, b = 1, scale = 0.5, colNA = "transparent", zlim = c(0, 0.5))


## add Mark sensor data 
# convert Mark sensor location to a spatial points object
pt_1 <- SpatialPoints(cbind(-71.806452,	42.121811)) %>% st_as_sf()
# set crs of point to lat/lon
st_crs(pt_1) <- 4326
# project to drone crs
pt_1_reproj  <- st_transform(pt_1, crs = drone_crs)

#overlay point location on sentinel image. use "add=TRUE" in second "plot" command
plotRGB(s2_raster_rpj, r =4, g = 3, b = 2, scale = 5000, colNA = "transparent", zlim = c(0, 5000) )
plot(pt_1_reproj, pch = 19, col = "blue", add = TRUE)

# load time-series of Mark sensor data
load(here("materials/data/whittier/", "A000680_daily.rda"))
# convert "time" field to a "date" data type (for plotting)
dev$date <- as_date(dev$time) 
# filter out single pod observation on Aug 26
dev_aug_26 <- dev %>% filter(date == as_date("2018-08-26")) 

# plot Mark time series data usnig ggplot
ggplot(dev) + 
  geom_point(aes (x = date, y = NDVI)) + 
  geom_line(aes (x = date, y = NDVI))

## show time-series with observation for Aug 26 highlighted
ggplot(dev) + 
  geom_point(aes (x = date, y = NDVI))+ 
  geom_point(data = dev_aug_26, aes (x = date, y = NDVI), color = "blue", size = 5)
