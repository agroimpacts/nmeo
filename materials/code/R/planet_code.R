# Companion script for class 5: see 5-droning_on_3.Rmd

##### Path variables
## You have to replace the paths within the quotes to match: 
# 1. the directory path where you put the PIX4D outputs 
img_path <- "~/Dropbox/data/imagery/planet/whittier/"

# the directory where you want your outputs to be written 
out_dir <- "materials/data/08"  

library(raster)
img <- brick(file.path(img_path, "20180616_145931_0f4d_aoi.tif"))
img2 <- img / cellStats(img, max)
plotRGB(img2[[c(4, 3, 2)]], scale = 1)
gcvi <- (img1[[1]] / img1[[3]]) - 1

