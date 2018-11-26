# Companion script for class 5: see 5-droning_on_3.Rmd

##### Path variables
## You have to replace the paths within the quotes to match: 
# 1. the directory path where you put the PIX4D outputs 
img_path <- "~/Dropbox/data/imagery/uas/pix4d"

# 2. The folder names for each of the projects. 
# !!!NOTE!!!: this assumes you put all four PIX4D project folders in one common # directory. Please move them into one if you didn't do so.
project1 <- "whittier_demo_24August2018"
project2 <- "whittier_demo_24August2018_noreftarget"
project3 <- "whittier_demo_24August2018_noppk"
project4 <- "whittier_demo_31August2018_noreftarget"

# 3. the directory where you want your outputs to be written 
out_dir <- "materials/data/05"  

# 4. the directory containing reflectance images in your projects. 
# If you only created tile outputs, your results will live in 
# .../4_index/reflectance/tiles/". If so, set the value to "tiles". If you have # merged outputs, they you will images in 4_index/reflectance/, so set the variable to "merged". In my case, they are merged, so I chose "merged"
ref_dir <- "merged"

# 5. path to companion class5_functions.R script
script_path <- "materials/code/R/external/scripts/class5_functions.R"

## The following variables are optional to change. These are the name roots for 
#  each of the images will we be creating. 
mband1 <- "aug24_ngb"
mband2 <- "aug24_ngb_noreftarget"
# mband3 <- "aug24_ngb_noppk"
# mband4 <- "aug31_ngb_noreftarget"

# Output names for warped and stretched
out1 <- "aug24_ngb_cog"
out2 <- "aug24_ngb_noreftarget_cog"
# out3 <- "aug24_ngb_noppk_cog"
# out4 <- "aug31_ngb_noreftarget_cog"


# Load packages and functions
library(gdalUtils)
library(raster)
source(script_path)  # this loads the companion scripts

##### Processing
## 1st look
# Look at August 24th orthomosaic: reflectance targets + PPK correction  
fp <- file.path(img_path, project1)
img_nms <- refl_paths(fp)

# This creates a stack of the NIR, Red, Green bands, and then plots them in R
s <- stack(lapply(img_nms[c(2, 4, 1)], raster))
plotRGB(s, scale = 1, zlim = c(0, 1))

## Making multi-band images
# Make a multi-band stack of the images, drawing on a customized function that 
# uses gdal to make stack 
nms <- img_nms[c(2, 4, 1)]  
b1 <- multi_band_stack(nms = nms, out_dir = out_dir, out_name = mband1)
plotRGB(b1, scale = 1, colNA = "transparent", zlim = c(0, 1))

# Convert the other images to multi-band stacks
# August 24, PPK, no reflectance target
fp <- file.path(img_path, project2)
img_nms <- refl_paths(fp)
nms <- img_nms[c(2, 4, 1)]  
b2 <- multi_band_stack(nms = nms, out_dir = out_dir, out_name = mband2)
plotRGB(b2, scale = 1, colNA = "transparent", zlim = c(0, 1))

# # August 24, no PPK, no reflectance target
# fp <- file.path(img_path, project3)
# img_nms <- refl_paths(fp)
# nms <- img_nms[c(2, 4, 1)]
# b3 <- multi_band_stack(nms = nms, out_dir = out_dir, out_name = mband3)
# plotRGB(b3, scale = 1, colNA = "transparent", zlim = c(0, 1))
# 
# # August 31, PPK, no reflectance target
# fp <- file.path(img_path, project4)
# img_nms <- refl_paths(fp)
# nms <- img_nms[c(2, 4, 1)]
# b4 <-  multi_band_stack(nms = nms, out_dir = out_dir, out_name = mband4)
# plotRGB(b4, scale = 1, colNA = "transparent", zlim = c(0, 1))
# 
## Processing for band math, using custom function that calls gdalwarp
# Common extent for all images
ext <- c(-71.8101, 42.1193, -71.8041, 42.1242)

# Process the first image stack
b1a <- img_align(img = b1@file@name, out_dir = out_dir, out_name = out1, 
                 ext = ext)
plotRGB(b1a, scale = 1, colNA = "transparent", zlim = c(0, 1))  # have a look

# Process the rest
b2a <- img_align(img = b2@file@name, out_dir = out_dir, out_name = out2, 
                 ext = ext)
# b3a <- img_align(img = b3@file@name, out_dir = out_dir, out_name = out3, 
#                  ext = ext)
# b4a <- img_align(img = b4@file@name, out_dir = out_dir, out_name = out4, 
#                  ext = ext)

####### Comparisons
## Reflectance calibration strategy
ref_diff <- b1a - b2a  # subtract no ref target from ref target

# plot the difference maps, per band
nms <- c("NIR", "Red", "Green")
plot(ref_diff, main = nms, axes = FALSE, zlim = c(-0.5, 0.5))  

# How much difference in stats?
stats <- cellStats(ref_diff, summary)
colnames(stats) <- nms
round(stats, 3)

# ## PPK versus not
# ref_diff <- b2a - b3a  # subtract no ref target from ref target
# plot(ref_diff, main = nms, axes = FALSE, zlim = c(-0.5, 0.5))
# stats <- cellStats(ref_diff, summary)
# colnames(stats) <- nms
# round(stats, 3)
# 
# ## Two different dates
# ref_diff <- b2a - b4a  # subtract no ref target from ref target
# plot(ref_diff, main = nms, axes = FALSE, zlim = c(-0.5, 0.5))
# stats <- cellStats(ref_diff, summary)
# colnames(stats) <- nms
# round(stats, 3)
# 
# ## Effective Resolution
# ## How much shift between PPK strategies?
# ext <- c(-71.80825, 42.120780, -71.807550, 42.121566)
# pt <- cbind(mean(ext[c(1, 3)]), mean(ext[c(2, 4)]))
# par(mar = c(0, 0, 0, 0), mfrow = c(1, 2))
# plot(as(extent(ext[c(1, 3, 2, 4)]), "SpatialPolygons"), lty = 0)
# plotRGB(b2a, scale = 1, colNA = "transparent", zlim = c(0, 1), add = TRUE)
# points(pt[, 1], pt[, 2], col = "cyan", pch = "+")
# plot(as(extent(ext[c(1, 3, 2, 4)]), "SpatialPolygons"), lty = 0)
# plotRGB(b3a, scale = 1, colNA = "transparent", zlim = c(0, 1), add = TRUE)
# points(pt[, 1], pt[, 2], col = "cyan", pch = "+")
# 
# 
