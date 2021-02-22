Projects
================

[Course Home](../README.md) | [General Info](general-information.md) |
[Syllabus](syllabus.md) | [Intro Modules](introductory-modules.md)

# Team Projects

There are several potential projects that can be undertaken for this
class.

1.  [Multi-scale estimation of crop yield](#project-1)
2.  [Using cloud-based EO processing platforms to create multi-source
    image time series](#project-2)
3.  [Planet basemaps and imagery for crop productivity mapping](#project-3)
4.  [Crop type mapping with Radiant Earth machine learning data](#project-4)
5.  [Data Visualization](#project-5)
6.  [Google Earth Engine App](#project-6)

More detail on each follows:

## Project 1

### Maize Yield Estimates

We have been collecting data over the course of three summers in a
maize/corn field at Whittier Farms, in Sutton, MA. Data include:

  - Micro-meteorology and crop growth data collected by three Arable
    Mark sensors over three seasons (2018-2020)
  - Field measurements of leaf area index collected underneath each Mark
    (three seasons)
  - 10 cm multi-spectral imagery collected by a Sequioa+ camera mounted
    on an Ebee Plus UAS on several dates (three seasons)
  - Biomass and grain yield crop cuts near Mark sensors and at 12 other sample points (2020 only)
  
In addition to these, we can also acquire near-daily PlanetScope 3-4
RGBNIR imagery over the same fields for the same years.

In a previous version of this class, a group project estimated yield based on vegetation index time-series, Mark measurements of downwelling solar radiation, and a constant harvest index (that converts biomass to grain yield.). We'd like to improve this project in two ways.

  - Use the sample measurements of biomass and grain yield from 2020 to better understand how the harvest index varies over the fields (and incorporate this into yield prediction)
  - Use the Mark micro-meteorology estimates to run a mechanistic crop
    simulator to predict maize yields. (more challenging, but we can help you set up this part of the project)

Resources:

  - [Comparison of Earth Observing-1 Ali and Landsat Etm+ for Crop Identification and Yield Prediction in Mexico](https://doi.org/10.1109/TGRS.2003.812909) 
  - [A scalable satellite-based crop yield mapper](https://www.sciencedirect.com/science/article/pii/S0034425715001637?casa_token=NGW1f60fascAAAAA:9ueYxn6fxuSQ1dVlT7l9w9tetR7vtqPPwhTOpa5gyR1oemRMEsPM24NqqcFb6UyBXHXLpmEjuw)

## Project 2

### EO Platforms and High Resolution Image Time Series

One ongoing research need for estimating agricultural productivity is to
have a set of imagery that can consistently monitor crop growth under cloudy conditions. Ground sensors are one method to monitor crops "below the clouds", but these sensors have limited spatial footprint and may have issues with charging and cellular connectivity. Satellite-based radar sensors, like Sentinel-1, offer another option to monitor crop growth under cloud cover.

This project will use the Google Earth Engine (GEE) platform to compare time-series from Sentinel-1 (radar) and Sentinel-2 (multipsectral) with ground sensor time-series of maize fields in Zambia. The goal is to measure how well the satellite based time-series (Sentinel 1/2) correlate with the ground-based sensors and if the Sentinel-1 imagery can effectively monitor crop growth under cloudy conditions.

Resources:

  - [Understanding the temporal behavior of crops using Sentinel-1 and Sentinel-2-like data for agricultural applications](https://doi.org/10.1016/j.rse.2017.07.015)

## Project 3

### Planet basemaps and imagery for crop productivity mapping

Planet, the largest provider of CubeSat high-reolution imagery (3-4m), recently entered into an agreement to release monthly basemaps of tropical regions to monitor deforestation [linked here](https://www.planet.com/pulse/planet-ksat-and-airbus-awarded-first-ever-global-contract-to-combat-deforestation/)

This agreement includes monthly surface reflectance basemaps that should be of a higher quality than individual Planet images. 

This project will investigate how well these basemaps can be used to track crop growth in tropical regions, by comparing the basemaps to ground sensor measurements at maize fields in Zambia. 

This project can also investigate how well the basemaps compare to individual Planet images (to see if the basemaps provide more consistent measurements of crop growth)

Resources:

  - [Daily Retrieval of NDVI and LAI at 3 m Resolution via the Fusion of CubeSat, Landsat, and MODIS Data](https://doi.org/10.3390/rs10060890) This project won't use these methods per se, but this article gives a good overview of the radiometric inconsistencies in Planet CubeSats.
  - [NICFI User Guide](https://assets.planet.com/docs/NICFI_UserGuidesFAQ.pdf)
  - [NICFI FAQ](https://assets.planet.com/docs/NICFI_General_FAQs.pdf)

## Project 4

### Crop type mapping with Radiant Earth machine learning data 

Radiant Earth has recently made publicly available a set of high quality training data sets for machine learning (ML) applications [linked here](https://www.mlhub.earth/) . This project focuses on using one of the crop type data sets in Africa to develop a ML (or deep learning) model that can predict crop type from satellite imagery. 

Ideally, this machine learning model could be applied to other areas/countries to provide preliminary crop type maps (that would need to be validated). The initial machine learning model would be created using the RadiantEarth API in Jupyter notebooks, but it would be great to investigate if these models can be applied to other areas, perhaps by using the Google Earth Engine API. 

Resources:

  - [Sample data set, Kenya](http://registry.mlhub.earth/10.34911/rdnt.u41j87/)
  - [Sample data set, Tanzania](http://registry.mlhub.earth/10.34911/rdnt.5vx40r/)
  - [Radiant Earth, MLHub tutorials](https://github.com/radiantearth/mlhub-tutorials/blob/main/notebooks/radiant-mlhub-api-know-how.ipynb)
  - [Smallholder maize area and yield mapping at national scales with Google Earth Engine](https://doi.org/10.1016/j.rse.2019.04.016) (example of machine learning model used for crop type classification)
  
This project focuses on crop type classification, but there are a wide range of ML applications on Radiant Earth. [see here](https://medium.com/radiant-earth-insights/ml/home) . This project could also be adapted to other applications if your group is interested in them.

### Deep learning

Apply a deep learning model to develop a classification map. One
approach might be to try adapt this approach
[here](https://github.com/microsoft/landcover) to get it running on a
local or AWS server, and then point it at a new geography (e.g. Ghana).

## Project 5

### Data visualization for EO 

![](https://www.unfolded.ai/de1d7053da34883ecf43aa91b989f209/temp-variations-earth-engine.gif)

Take a data set from this course (or your own research) and explore the data visualization capabilities in Google Earth Engine (or other software, such as Python and R)

This project should still involve geoprocessing steps, but one focus of the project is on the capabilities to display spatial data in new ways. 

This project should outline what methods exist (and are lacking) for data visualization, and  propose (or create) new data visualization techniques.

Resources:

  - Elsevier (journal publisher) [data visualization](https://www.elsevier.com/authors/tools-and-resources/data-visualization)
  - [GEE Examples](https://developers.google.com/earth-engine/guides/ic_visualization)
  - [GEE Example - river animation](https://medium.com/google-earth/visualizing-changing-landscapes-with-google-earth-engine-b2d502dc02a8)
  - [GEE Example - pydeck](https://medium.com/google-earth/visualizing-geospatial-data-with-pydeck-and-earth-engine-8f77ce1fc8bb)
  - [Mapbox - 3D mapping of global population density](https://blog.mapbox.com/3d-mapping-global-population-density-how-i-built-it-141785c91107)

## Project 6

### Google Earth Engine App

![](https://developers.google.com/earth-engine/images/Demo_trendy_lights.png)

Interested in creating an interactive tool? You can use the processing of Google Earth Engine and allow the end-user to interact with the map in an app. 

We won't teach the application portion of GEE in the class, but there are examples available [here](https://medium.com/google-earth/share-your-analyses-using-earth-engine-apps-1ac29939903f)

Resources:

  - [Gallery of GEE Apps (Philipp Gärtner blog)](https://philippgaertner.github.io/2020/12/ee-apps-table-searchable/)
  - [GEE app guide](https://developers.google.com/earth-engine/guides/apps)
  - [sample app, Global Human Influence Mapping ](https://earthengineedu.users.earthengine.app/view/human-impact-explorer)
  - [sample app, changes in night lights](https://jhowarth.users.earthengine.app/view/lights-change-time-neighborhood)

[Course Home](../README.md) | [General Info](general-information.md) |
[Syllabus](syllabus.md) | [Intro Modules](introductory-modules.md)
