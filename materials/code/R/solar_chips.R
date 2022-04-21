
library(sf)
library(dplyr)
library(terra)


# read in solar vectors
solar <- st_read(
  "../coursework/2022S/projects/solar/SolarYear_Mass/SolarYear_Mass.shp"
)

# reproject to US Albers equal areas
solar_proj <- st_transform(solar, crs = "ESRI:102003")

# create template raster from the bounding box of the solar vectors, setting
# resolution to 10 m
r <- terra::rast(ext(solar_proj), crs = "ESRI:102003", res = 10)
values(r) <- 1:ncell(r)

# aggregate by factor of X to give chip extent
x <- 224
r2 <- aggregate(r, fact = x)
values(r2) <- 1:ncell(r2)
v2 <- st_as_sf(as.polygons(r2))  # convert to polygons

# convert the solar_proj vectors to terra::vect format (another spatial vector)
# format
solar_projv <- vect(solar_proj)
solar_projr <- rasterize(solar_projv, r)  # then rasterize at x m resolution
# solar_projr2 <- rasterize(solar_projv, r2, fun = min)
# plot(solar_projr2)

# set all pixels with solar cells in them to 1, and all without solar pixels to
# 0
solar_projr[!is.na(solar_projr)] <- 1
solar_projr[is.na(solar_projr)] <- 0

# aggregate the rasterized dataset by summing to x X x resolution, counting
# how many 10 m cells have panels in them. 
solar_projr_sum <- crop(aggregate(solar_projr, fact = x, fun = sum), r2)

# zonal statistics will give you a data.frame having count of solar cells per 
# larger tile grid
zones <- zonal(solar_projr_sum, z = r2)
zones

# you can select cells having counts greater than a certain amount, e.g. 100 
ind <- data.frame(zones) %>% filter(layer > 100)  # index

# join filtered cell count onto tile grid vector
v2 <- inner_join(v2, ind)  
plot(v2, border = "transparent")  

# you can write out the vectors to collect satellite imagery from Earth Engine
# set your output path and file name here
# f <- "materials/data/solar/s2_solar_tile_grid_144.geojson"
###! set file name here
f <- "materials/data/solar/s2_solar_tile_grid_224.geojson"
st_write(v2, dsn = f, delete_dsn = TRUE)

# to create label chips at coarser (10 m) resolution set the following variable 
# to "coarse", or if at finer (1 m) resolution set "fine". 
# the "fine" option uses the coarser tile grid and solar raster to identify
# cells within each tile that have solar panels, and then converts those into 
# a chips at a resolution scaled as a factor of the coarser resolution.  So, if
# you want chips that are 224X224 from a 1 m resolution image, then start with a
# a tile grid that it is 224 at 10 m (see x variable near top of script)
resolution <- "coarse"

# if selecting the "fine" option specify the threshold number of cells 
# in the finer chip that should contain solar panels, e.g. 20, in this next 
# variable
nfinecells <- 20

# set the test variable to TRUE if you want to test a few cells first before 
# running the whole thing, otherwise FALSE will commence the whole loop
test <- TRUE

shh <- function(x) suppressMessages(suppressWarnings(x))
if(test) {
  l <- 1:5  # will run first 5 rows
} else if(!test) {
  l <- 1:nrow(v2)
}
if(resolution == "coarse") {
  for(i in l) {  # i <- 1
    tile <- v2[i, ]
    tiler <- crop(solar_projr, tile)
    fnm <- file.path("materials/data/solar/chips", 
                     paste0("tile_", tile$lyr.1, ".tif")) 
    print(paste("Chipping", basename(fnm)))
    writeRaster(tiler, filename = fnm)
  }
} else if(resolution == "fine") {
  vfine <- list()
  y <- res(r2)[1] / x  # calculate resolution for tiling
  for(i in l) {  # i <- 1
    tile <- v2[i, ]
    tiler <- rast(ext(tile), nrow = y, ncol = y)
    values(tiler) <- 1:ncell(tiler)
    tilev <- st_as_sf(as.polygons(tiler)) %>% st_set_crs(st_crs(tile))
    
    print(paste("Processing tile", tile$lyr.1))
    solar_in_tile <- crop(solar_projr, tiler)
    # plot(solar_in_tile_agg)
    aggfact <- floor(res(tiler)[1] / res(solar_in_tile)[1])
    solar_in_tile_agg <- resample(
      aggregate(solar_in_tile, fact = aggfact, fun = sum), 
      tiler, method = "near"
    )
    
    zones <- zonal(solar_in_tile_agg, z = tiler)
    ind <- data.frame(zones) %>% filter(layer > nfinecells)  # index
    
    # join filtered cell count onto tile grid vector
    v2tile <- shh(inner_join(tilev, ind))
    # plot(v2tile, border = "transparent")  
    solar_tile <- shh(st_crop(solar_proj, v2tile))
    v2tile <- v2tile %>%  # check to make sure actually intersects
      filter(st_intersects(., solar_tile, sparse = FALSE))
    # plot(tilev$geometry)
    # plot(solar_tile$geometry, add = TRUE)
    # plot(v2tile$geometry, add = TRUE, border = "red")
    
    vfine[[i]] <- v2tile  # append vectors
    resfine <- res(r2)[1] / res(r2)[1]
    # rasterize
    for(j in 1:nrow(v2tile)) {  # j <- 1
      solar_subtile <- shh(st_intersection(solar_tile, v2tile[j, ]))
      # plot(v2tile[j, ]$geometry)
      # plot(solar_tile$geometry, add = TRUE)
      
      rsubtile <- rast(ext(v2tile[j, ]), res = resfine)
      solar_subtiler <- rasterize(vect(solar_subtile), rsubtile)
      solar_subtiler[is.na(solar_subtiler)] <- 0
      # plot(solar_subtiler)
      
      fnm <- file.path("materials/data/solar/chips", 
                       paste0("tile_", tile$lyr.1, "_", j, ".tif"))
      print(paste("...chipping", basename(fnm)))
      writeRaster(tiler, filename = fnm, overwrite = TRUE)
    }
  }
  # combine and save out vector grid providing boundaries of finer chips
  vfine0 <- do.call(rbind, vfine)
  
  ###! set file name here
  f <- "materials/data/solar/s2_solar_tile_grid_224.geojson"
  st_write(vfine0, dsn = f, delete_dsn = TRUE)
}


# or you can downscale the chips further, say to a 1 m resolution, e.g. NAIP, 
# by downscaling in loop
# convert tile into subtile using factor of y

# inttiles <- extract(solar_projr, v2)












