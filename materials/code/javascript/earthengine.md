# EarthEngine Code Examples

Copy and paste any of these into a new script in EarthEngine. 

## TOC
- [In-class examples](#in-class-examples)
    - [Working with SRTM data](#working-with-srtm-data)
    - [Landsat Image Collections](#landsat-image-collections)
- [More Advanced Examples](#more-advanced-examples)

## In-class examples

From October 1, 2018

### Working with SRTM data

How to do basic image displays, and then calculate terrain features and statistics within a region of interest. Adapted from two of EarthEngine's own tutorials, found [here](https://developers.google.com/earth-engine/tutorial_api_02) and [here](https://developers.google.com/earth-engine/tutorial_api_03). 

```js
// AOI for our exercise. Draw your own with the polygon tool, or copy and paste
// this into code editor, and select option to convert this into an imported 
// object
var myaoi = ee.Geometry.Polygon(
        [[[-71.80623866004942, 42.12009489915099],
          [-71.80593825263975, 42.120254059230284],
          [-71.80542326850889, 42.12063604178958],
          [-71.80484391136167, 42.120779284655654],
          [-71.80505848808286, 42.12190930035651],
          [-71.80619574470518, 42.12175014443487],
          [-71.80636740608213, 42.12297563471934],
          [-71.80814839286802, 42.12286422749111],
          [-71.808684834671, 42.122482258364315],
          [-71.80808401985166, 42.12108168519837],
          [-71.80748320503233, 42.119649248802105]]]);
// ####################################################

// #### Load datasets
// ## imagery
// Load SRTM 
var srtm = ee.Image('CGIAR/SRTM90_V4');

// ## vectors
// # Zambia
var zambia = ee.Feature(
  ee.FeatureCollection("USDOS/LSIB/2013")
  .filterMetadata('cc', 'equals', 'ZA')
  .first());

// # Clip boundaries (generous margin around Zambia)
var zambia_bb = ee.Feature(ee.Geometry.Rectangle(21, -19, 34.5, -7.5));

// ## Calculations
// Slope
var slope = ee.Terrain.slope(srtm);
// Aspect
var aspect = ee.Terrain.aspect(srtm);
// Convert to radians, compute the sin of the aspect.
var sinImage = aspect.divide(180).multiply(Math.PI).sin();

// # Statistics
// Mean elevation My AOI
var meanDict = srtm.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: myaoi,
  scale: 90,
  maxPixels: 1e8
  // bestEffort: true
});
var mean = meanDict.get('elevation');
print('Mean elevation of My AOI', mean);

// Mean elevation Zambia
var meanDict = srtm.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: zambia.geometry(),
  scale: 90,
  maxPixels: 1e8
  // bestEffort: true
});
var mean = meanDict.get('elevation');
print('Mean elevation of Zambia', mean);

// Mean elevation bounding box
var meanDict = srtm.reduceRegion({
  reducer: ee.Reducer.mean(),
  geometry: zambia_bb.geometry(),
  scale: 90,
  maxPixels: 1e9
  // bestEffort: true
});
var mean = meanDict.get('elevation');
print('Mean elevation bounding box', mean);


// ### Maps
// Zoom to a location.
Map.setCenter(-112.8598, 36.2841, 9); // Center on the Grand Canyon.
// Map.setCenter(-71.8067, 42.1214, 14); // Sutton, MA
// Map.setCenter(28, -13, 4); // Zambia
// Display the image on the map.
// Map.addLayer(srtm, {min: 0, max: 2500}, 'Height (m)');
Map.addLayer(srtm, {min: 0, max: 3000, palette: ['blue', 'orange', 'red']},
            'custom palette');
// Map.addLayer(slope, {min: 0, max :60}, 'slope');
// Map.addLayer(aspect, {min: 0, max: 360, palette: ['blue', 'green', 'red']}, 'aspect');
// Map.addLayer(sinImage, {min: -1, max: 1, palette: ['blue', 'green', 'red']}, 
//             'sin');
// Map.addLayer(region);
// Map.addLayer(zam);
```

[Back to TOC](#toc)

### Landsat Image Collections

Loading in TOA reflectance collection, filtering it down to a location and time period of interest, finding the least cloudy scene, making a median composite image, clipping and masking, calculating NDVI over a filtered collection, and making a time series chart for a region of interest. 

Adapted from EarthEngine tutorials [here](https://developers.google.com/earth-engine/tutorial_api_04), [here](https://developers.google.com/earth-engine/tutorial_api_05), [here](https://developers.google.com/earth-engine/tutorial_api_06), and [here](https://developers.google.com/earth-engine/tutorial_api_07).
```js
// AOI for our exercise. Draw your own with the polygon tool, or copy and paste
// this into code editor, and select option to convert this into an imported 
// object
var myaoi = ee.Geometry.Polygon(
        [[[-71.80623866004942, 42.12009489915099],
          [-71.80593825263975, 42.120254059230284],
          [-71.80542326850889, 42.12063604178958],
          [-71.80484391136167, 42.120779284655654],
          [-71.80505848808286, 42.12190930035651],
          [-71.80619574470518, 42.12175014443487],
          [-71.80636740608213, 42.12297563471934],
          [-71.80814839286802, 42.12286422749111],
          [-71.808684834671, 42.122482258364315],
          [-71.80808401985166, 42.12108168519837],
          [-71.80748320503233, 42.119649248802105]]]);
// ####################################################

// #### Load imagery
var l8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_TOA');
var srtm = ee.Image('CGIAR/SRTM90_V4');

// ## Filter imagery (spatial)
var spatialFiltered = l8.filterBounds(myaoi);
print('spatialFiltered', spatialFiltered);

// ## Filter imagery (temporal)
var temporalFiltered = spatialFiltered.filterDate('2018-05-01', '2018-09-15');
print('temporalFiltered', temporalFiltered);

// ## Cloud filtering
// Sort from least to most cloudy.
var sorted = temporalFiltered.sort('CLOUD_COVER');
// Get least cloudy image
var scene = ee.Image(sorted.first());

// Compositing
var median = temporalFiltered.median();

// clip
var whittier_median = median.clip(myaoi);

// mask
var elevmask = srtm.gt(100);
var maskedMedian = median.updateMask(elevmask);

// NDVI
var addNDVI = function(image) {
  var ndvi = image.normalizedDifference(['B5', 'B4']).rename('NDVI');
  return image.addBands(ndvi);
};

// Apply function to single image
var image = temporalFiltered.first()
var ndvi = addNDVI(image).select('NDVI');

// Map onto a collection
var withNDVI = temporalFiltered.map(addNDVI);

// ##### Charts
// Create chart
var chart = ui.Chart.image.series({
  imageCollection: withNDVI.select('NDVI'),
  region: myaoi,
  reducer: ee.Reducer.first(),
  scale: 30
}).setOptions({title: 'NDVI over time'});

// Display the chart in the console.
print(chart);

// ##### Maps
// Comment or uncomment to display different outputs
Map.setCenter(-71.8067, 42.1214, 14); // Where is this?
var visParams = {bands: ['B4', 'B3', 'B2'], max: 0.3};
//var visParams = {bands: ['B5', 'B4', 'B3'], max: 0.3};
// Map.addLayer(scene, visParams, 'true-color composite');
// Map.addLayer(temporalFiltered, visParams, 'Whittier L8 collection');
// Map.addLayer(whittier_median, visParams, 'Clip');
// Map.addLayer(maskedMedian, visParams, 'Mask');
// Map.addLayer(withNDVI, {min: -1, max: 1}, 'NDVI');
Map.addLayer(ndvi, {min: 0, max: 0.5}, 'NDVI');
```

[Back to TOC](#toc)


## More Advanced Examples
### Filtering and exporting images

An example using CHIRPs daily rainfall data in a region over Zambia. Adapted from code developed by Sitian Xiong for downloading and filtering MODIS data. Includes more complex date filtering (subset a range of dates that span two years [start of rainy season in Zambia], for multiple years), clipping, and exporting to Google Drive.   
```js
// Download multiband stacks of CHIRPS data masked to Zambia.
// Modifying approaches developed by Sitian Xiong for MODIS imagery.

// 1. Clip boundaries (generous margin around Zambia)
var zam = ee.Feature(ee.Geometry.Rectangle(21, -19, 34.5, -7.5));  

// 2. Functions 
// Stacking function
var STACK = function(collection){
    var first = ee.Image(collection.sort('system:index').first()).select([]);
    var appendBands = function(image, previous){
        return ee.Image(previous).addBands(image);
    };
    return ee.Image(collection.iterate(appendBands,first))
};  

// Get Function
var CHIRPS_GET = function(img){
  var rain = img.select(['precipitation'])  // select rainfall
  var rainclip = rain.clip(zam);  
  //rename the band as rain_ + its Date, e.g.,"rain_2008_10_01"
  var text = ee.String('rain_').cat(ee.String(img.get('system:index'))); 
  return rainclip.rename(text);
};

// 3. Create multiband stacks for 2007-2017 for October 1-January 10 (yr:yr+1)
var yrs = ee.List.sequence(2007,2017); // list years
print(yrs)
var chirps_multibands = ee.ImageCollection(yrs.map(function(yr){
  var end_yr = ee.Number(yr).add(ee.Number(1));
  
  // select data within date ranges
  var imgs = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
            .filterDate(ee.String(ee.Number(yr).int()).cat(ee.String('-10-01')),
            ee.String(ee.Number(end_yr).int()).cat(ee.String('-01-11')));  
  var imgs_yr = ee.ImageCollection(imgs.map(CHIRPS_GET));  // clip each date
  return STACK(imgs_yr)   // stack and return
}));

// 4. Export to Drive
var imgs_4export = chirps_multibands.getInfo()['features'];  
//see https://gis.stackexchange.com/questions/236707/
//how-can-i-export-a-set-of-images-from-google-earth-engine
//print(imgs_4export) 
for (var i = 0; i<imgs_4export.length;i++) {
  var imgs_list = chirps_multibands.toList(chirps_multibands.size());
  var img_4export =ee.Image(imgs_list.get(i));    
  
  //rename the multi-bands image using its year and export
  var img_name = 'chirps_'+img_4export.get('system:index').getInfo().slice(0,4);
  //print('exporting'+img_name)
  Export.image.toDrive({
      image: img_4export, 
      description: img_name, 
      folder:  'chirps',
      region: zam, 
      scale: 5000,
      maxPixels: 1000000000
  });
}
```
[Back to TOC](#toc)

### Calculating NDVI amplitude

Calculate the NDVI amplitude over a single growing season for Zambia, after first removing cloudy pixels, and masking to cropland areas. 

```js
// This example demonstrates the use of the pixel QA band to mask
// clouds in surface reflectance (SR) data.  It is suitable
// for use with any of the Landsat SR datasets.

//Load Zambia 
var zambia = ee.FeatureCollection('ft:10YdSHdN3XgDoRFDyPLecjjyV_5iQqGEymorahxMD', 'geometry');
// Load Landsat 8 surface reflectance data
var l8sr = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR');

// cropland (SERVIR Type II Landcover for Zambia)
var lc = ee.Image('https://code.earthengine.google.com/?asset=users/lyndonestes/africa/zambia_lc_2010_II');

// cropland mask
// select out cropland from landcover map and clip to Zambia
var cropland = lc.eq(8).clip(zambia);

// aggregate to ~1 km
var cropland250 = cropland.reduceNeighborhood({
  reducer: ee.Reducer.mean(),
  kernel: ee.Kernel.square(250,"meters"),
}).reproject(cropland.projection().atScale(250));
//print(cropland250);

// pixels with cropland gt 75%
var croplandgt75 = cropland250.gt(0.75);  

// NDVI cloud filter
// Function to cloud mask from the Fmask band of Landsat 8 SR data.
function maskL8sr(image) {
  // Bits 3 and 5 are cloud shadow and cloud, respectively.
  var cloudShadowBitMask = ee.Number(2).pow(3).int();
  var cloudsBitMask = ee.Number(2).pow(5).int();

  // Get the pixel QA band.
  var qa = image.select('pixel_qa');

  // Both flags should be set to zero, indicating clear conditions.
  var mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0)
      .and(qa.bitwiseAnd(cloudsBitMask).eq(0));

  // Return the masked image, scaled to [0, 1].
  return image.updateMask(mask).divide(10000);
}

// Clip Landsat collection to Zambia and apply cloud mask
var ls8mask = l8sr.filterDate('2017-01-01', '2017-05-31');
var ls8mask2 = l8sr.filterDate('2016-10-01', '2016-12-31');
//print(ls8zam);

// calculate NDVI from masked dataset for Zambia
var zamndvi = ls8mask.map(function(image) {
    var img = image.clip(zambia);
    return img.normalizedDifference(['B5', 'B4'])
});

// calculate NDVI from masked dataset for Zambia, early growing season
var zamndvi2 = ls8mask2.map(function(image) {
    var img = image.clip(zambia);
    return img.normalizedDifference(['B5', 'B4'])
});

// max and NDVI for the season
var maxndvi = zamndvi.max();
var minndvi = zamndvi2.min();

var ampndvi = maxndvi.subtract(minndvi);
//var maxndvicrop = maxndvi.mask(croplandgt75);
var ampndvicrop = ampndvi.mask(croplandgt75);

// Map
Map.setCenter(29.0, -13.5, 5);
//Map.addLayer(maxndvicrop, {min:0, max:1},'Max NDVI in cropland');
//Map.addLayer(maxndvi, {min:0, max:1},'Max NDVI');
//Map.addLayer(ampndvicrop, {min:0, max:1},'NDVI amplitude in cropland');
Map.addLayer(ampndvicrop, {min:0, max:1},'NDVI amplitude');
// Map.addLayer(points)
```

[Back to TOC](#toc)