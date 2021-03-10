## sample calculations for Aug 3, 2020 images

library(raster)
library(rgdal)
library(sf)
library(dplyr)

## load nir and red images (change file paths to the image location on your computer)
nir_refl_03aug20 <- raster("C:/Users/micha/Documents/pix4d/whittier_03aug20_pix4d/4_index/reflectance/whittier_03aug20_pix4d_transparent_reflectance_nir.tif")
nir_no_refl_03aug20 <- raster("C:/Users/micha/Documents/pix4d/whittier_03aug20_ppk_without_refl_cal/4_index/reflectance/whittier_03aug20_ppk_without_refl_cal_transparent_reflectance_nir.tif")
red_refl_03aug20 <- raster("C:/Users/micha/Documents/pix4d/whittier_03aug20_pix4d/4_index/reflectance/whittier_03aug20_pix4d_transparent_reflectance_red.tif")
red_no_refl_03aug20 <- raster("C:/Users/micha/Documents/pix4d/whittier_03aug20_ppk_without_refl_cal/4_index/reflectance/whittier_03aug20_ppk_without_refl_cal_transparent_reflectance_red.tif")

## it may occur that the reflectance and non-reflectance processed images...
## have slightly different extents. If this is the case,
## then you will need to project the non-reflectance versions to the CRS...
## of the projected version.
# crs_refl_calibration <- crs(nir_refl_03aug20)
# nir_no_refl_03aug20 <- projectRaster(nir_no_refl_03aug20, crs = crs_refl_calibration)
# red_no_refl_03aug20 <- projectRaster(red_no_refl_03aug20, crs = crs_refl_calibration)
# 

## assign crs of drone imagery to variable
crs_drone <- (crs(nir_refl_03aug20))

## load and reproject whittier shapefile (update file path)
whittier_poly <- st_read("C:/Users/micha/Downloads/whittier_shapefile/whittier_shapefile/whittier.shp")
whittier_poly_rpj <- st_transform(whittier_poly, crs = crs_drone)


## calculate ndvi images
# ndvi with reflectance correction
ndvi_refl_03aug20 <- (nir_refl_03aug20 - red_refl_03aug20)/(nir_refl_03aug20 + red_refl_03aug20)
# ndvi without reflecance correction
ndvi_no_refl_03aug20 <- (nir_no_refl_03aug20 - red_no_refl_03aug20)/(nir_no_refl_03aug20 + red_no_refl_03aug20)


## NIR difference
# calculate difference of nir surface reflectance, with and without reflectance calibration
diff_nir_03aug20 <- nir_refl_03aug20 - nir_no_refl_03aug20
# plot the difference image
plot(diff_nir_03aug20, zlim = c(-0.5, 0.5))
plot(whittier_poly_rpj, add = TRUE)
# calculate the mean difference over the field polygons
nir_mean_diff_03aug20 <- extract(diff_nir_03aug20, whittier_poly_rpj) %>% first() %>% mean(., na.rm = TRUE)

## NDVI difference
# calculate difference of ndvi surface reflectance, with and without reflectance calibration
diff_ndvi_03aug20 <- ndvi_refl_03aug20 - ndvi_no_refl_03aug20
# plot the difference image
plot(diff_ndvi_03aug20, zlim = c(-0.5, 0.5))
plot(whittier_poly_rpj, add = TRUE)
# calculate the mean difference over the field polygons
ndvi_mean_diff <- extract(diff_ndvi_03aug20, whittier_poly_rpj) %>% first() %>% mean(., na.rm = TRUE)




