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
