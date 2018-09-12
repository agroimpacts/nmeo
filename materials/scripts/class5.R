# geog287287_class5.R - code for in-class exercises

# Besides changing a few parameters, the scripts should run when you execute 

# Script Block 1: Load in orthomosaic and present false color view 
multi_band_stack <- function(nms, out_dir, out_name, nodata = -10000) {
  vrt <- file.path(out_dir, paste0(out_name, ".vrt"))
  gtif <- file.path(out_dir, paste0(out_name, ".tif"))
  cog <- file.path(out_dir, paste0(out_name, "_cog.tif"))
  print("Creating vrt...")
  gdalbuildvrt(nms, output.vrt = vrt, separate = TRUE, srcnodata = nodata, 
               vrtnodata = nodata)
  print("Creating geotiff...")
  gdal_translate(src_dataset = vrt, dst_dataset = gtif, a_nodata = nodata,
                 co = list("TILED=YES", "COMPRESS=DEFLATE"))
  print("Creating overviews...")
  gdaladdo(gtif, r = "average", levels = c(2, 4, 8, 16))
  print("Creating cog...")
  gdal_translate(src_dataset = gtif, dst_dataset = cog,
                 co = list("TILED=YES", "COPY_SRC_OVERVIEWS=YES", 
                           "COMPRESS=DEFLATE"))
  file.remove(gtif, vrt)
  brick(cog)
}

img_align <- function(img, res = 0.11 / 100000, out_dir, out_name, 
                      ext, nodata = -10000) {
  img_out <- file.path(out_dir, paste0(out_name, "_gcs.tif"))
  gcs <- "+proj=longlat +datum=WGS84 +no_defs"
  r <- raster(img)
  gdalwarp(srcfile = img, dstfile = img_out, s_srs = proj4string(r), 
           t_srs = gcs, te = ext, tr = rep(res, 2), r = "bilinear", 
           overwrite = TRUE)
  b <- brick(img_out)
}














