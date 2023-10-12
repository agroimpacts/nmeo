Assignment 1, Fall 2023
================

The first class assignment consists of three exercises: two on colab
(one using Earth Engine, the other the Planet API), and the and the
other using your AWS instance. It will be due on Monday, October 18th by
the beginning of class. The assignments are provided below.

## colab

### Part 1 - Earth Engine

Create a colab notebook named with your initials followed by
`_nmeo_2022_ee_assn_part1`, e.g. mine would be
`lde_nmeo_2022_ee_assn_part1`.

- Use this block of code to define the area of interest:

  ``` python
  myaoi = ee.Geometry.Polygon(
      [[[-0.3436329956054607, 9.48094283485201],
        [-0.3436329956054607, 9.334622294426413],
        [-0.18707781982421068, 9.334622294426413],
        [-0.18707781982421068, 9.48094283485201]
      ]]
  )    
  ```

- Load in the Sentinel-2 surface reflectance (“COPERNICUS/S2_SR”)
  collections.  

- Filter the collection by the location of the AOI and by for the period
  2021-07-01 to 2021-12-31.

- Use the cloud masking functions to mask the collection, and crop them
  to the AOI.

- Map a VI band onto each cloudmasked collection. Previously we
  calculated NDVI. This time calculate EVI instead.

- Fit a harmonic regression to the EVI time series for the AOI from each
  image collection. To fit the harmonic regression, the following
  functions are required:

  - `construct_band_names`
  - `mask_clouds`
  - `add_evi` (see `add_ndvi`)
  - `add_dependents`
  - `add_harmonics`

- Create median composites of:

  - The Sentinel-2 NDVI series

- Then finally make some plots:

  - Create a time series chart of the Sentinel-2 harmonic fitted and
    original EVI series for the AOI.
  - Use `geemap` and the `display_image` function we developed to show
    the 10th images from the Sentinel collection. Use the correct
    `viz_params` to make a false color image. Set Band min and max
    values in the `viz_params` for each image collection to 0, 3000. Use
    meaningful titles in the `viz_params`, e.g. “30th Sentinel 2 image”.
  - Plot the median EVI image and the seasonality image from fitted
    harmonic model. Use a range of `{min: -0.5, max: 1}` to stretch the
    EVI images, and also add meaningful titles, e.g. “Sentinel-2 median
    EVI”.  

- Use the minimum code necessary to complete the task, i.e. do not
  maintain superfluous blocks that were previously there just to
  demonstrate components of the code, extra visualizations, etc.

### Part 2 - Planet API

Create a colab notebook named with your initials followed by
`_nmeo_2022_ee_assn_part2`, e.g. mine would be
`lde_nmeo_2022_ee_assn_part2`.

- Use the `maputil` package, together with the Malawi tiles dataset,
  adapting the code as needed from
  \`[planet_downloader_retiler.ipynb](https://github.com/agroimpacts/nmeo/blob/class/f2023/materials/code/notebooks/planet_downloader_retiler.ipynb).
- Select a new AOI in Malawi then the one you ran in the class exercise,
  making sure it only intersects about 10-20 tiles
- Query the Planet API to download the quads intersecting that new AOI,
  reproject and retile the quads into each tile polygon (as we did in
  class), making a COG of each.
- Use `leafmap` to show a randomly selected retiled sample against your
  selected tile grid.
- Create a STAC catalog of the retiled images on Google Drive, porting
  the procedures we used on SageMaker to colab (see
  `sagemaker-geo-demo.ipynb`).
  - Print the properties of the catalog items
- As above, use the minimum code necessary to complete the task.  
- **10 point bonus**: Instead of using `sklearn` to do the kmeans
  clustering, replace that workflow with one based on `ee` and `geemap`,
  so that the kmeans clustering is done on Google Earth Engine. That
  will require first transferring the processed Planet tiles to Earth
  Engine as assets first.

## AWS Sagemaker

In this exercise, you will process a Sentinel-2 image from the same
month as the Planet imagery (June, 2021) and over the same area of
Malawi covered by your new AOI from colab assignment part 2. The
assignment requires the following:

- Drawing on the examples provided in the
  [sagemaker-geo-demo.ipynb](https://github.com/agroimpacts/nmeo/blob/class/f2023/materials/code/notebooks/sagemaker-geo-demo.ipynb)
  notebook, use the STAC browser to query the Sentinel-2 catalog on AWS,
  using the boundaries of one of the tiles from
  `malawi_tiles_buf179.geojson` that intersect your AOI to provide the
  spatial dimensions of the query, and the period of June 1, 2021 to
  June 30, 2021 as the time period.
- Select the least cloudy image. Hint: you can use the STAC browser to
  filter available Sentinel images by cloud cover by adding an argument
  to `satsearch.Search.search`. See the “Complex Query” section
  [here](https://github.com/sat-utils/sat-search/blob/master/tutorial-1.ipynb)
  for how to do that.
- Collect Bands 3, 4 and 8 for the least cloudy image. You could do that
  by selecting any one of the filtered images that have \<1% cloud
  cover). Or you could use capture for each item in `sentinel_items` the
  `item.properties['eo:cloud_cover']` in a list, use that to find the
  index of least cloudy image, and then use that to select the three
  bands of the least cloudy image.
- Each band from the least cloudy image should be subset to the bounds
  of your selected tile (`read_subset`)
- Combine those three subset bands into a single 3 band image, with the
  dimensions (row, col, band). `np.dstack()` will do the job. Save out
  the 3 band image to a geotiff.
- Drawing on the
  [planet_basemap_cluster_segment.ipynb](https://github.com/agroimpacts/nmeo/blob/class/f2023/materials/code/notebooks/planet_basemap_cluster_segment.ipynb)
  notebook as a guide, use the `KMeans` function from `sklearn` to fit a
  7-cluster KMeans model to a sample of pixels from the 3 band image
  (don’t forget to flatten the image first).
- Use the model to classify the 3 band image. Save it out to geotiff.  
- Use `leafmap` to plot both the Sentinel 3-band image (as false color)
  and the kmeans-classified image in relation to the tile
  `GeoDataFrame`.
- As above, use the minimum code necessary to complete the task.

## Assessment

Each notebook is worth 50 points, which will be assessed as follows:

| Assignment tasks | Points | Style of code & presentation       | Points |
|------------------|--------|------------------------------------|--------|
| 0-25% correct    | 10     | Messy & undocumented               | 2.5    |
| 25-50% correct   | 15     | Fairly messy, lightly documented   | 5      |
| 50-75% correct   | 20     | Somewhat tidy, somewhat documented | 7.5    |
| 75-100% correct  | 25     | Tidy, well-documented              | 10     |

That makes the total worth 150 points. However, your grade will only be
100 points (plus any bonus points). That means the notebook with the
lowest grade is dropped.
