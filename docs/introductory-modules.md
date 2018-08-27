[Course Home](../README.md) | [General Info](general-information.md) | [Syllabus](syllabus.md) | [Projects](projects.md)

## Introductory Modules

An overview of each of the modules that we will cover in the first 8 weeks or so.

Return to [syllabus](syllabus.md) or the course [home page](../README.md).

### TOC
- [Drones](#drones)
- [Small Sats](#small-sats)
- [Cloud-based Processing](#cloud-based-processing)
- [Real-time _In Situ_ Sensors](#real-time-in-situ-sensors)
- [Human and Machine Intelligence](#human-and-machine-intelligence)

___

### Drones
#### Material covered

- Overview of our use case: drones as scaling tools
- Science:
    - Geometric corrections
    - Radiometric corrections
    - Uncorrectable geometric and radiometric aspects 
- Practice:
    - Flying
        - Flight planning
        - Simulation
        - Safety and [checklists](https://www.dropbox.com/s/u0eu5qvqcisjge5/eBee_plus_checklist-5.pdf?dl=0)
        - Collecting images (field excursion to [Whittier Farms](http://www.whittiers.com), specifically [here](https://goo.gl/maps/fFhJ25cRDXz))
    - Data processing:
        - Mosaicking
        - Preliminary analyses

#### Reading
- Manfreda et al [(2018)](http://www.mdpi.com/2072-4292/10/4/641)
- [Pix4D Academy](https://support.pix4d.com/hc/en-us/articles/214483743-Video-academy) videos, watch:
    - _Getting Started with Your First Project_
    - _Georeferencing_
    - _Tie Points_
    - _Multispectral camera (Parrot Sequoia)_
- A[n optional] useful [comparison](https://imagininc.wildapricot.org/resources/SPPC/2015/papers/john_gross_paper.pdf) of different SfM software


#### Tools
- eMotion3: Flight control software for Ebee.  Download and install from [here](https://www.dropbox.com/s/a8m1254bhous1v1/eMotion_3.5.0.msi?dl=0) 
- PIX4D mapper: 30 day trial version available from [here](https://cloud.pix4d.com/signup/?sol=pro). If interested in longer-term use, annual paid licenses are available at a discount through my academic license.  

[Back to TOC](#toc)

___

### Small Sats
#### Material covered

- Overview of our use cases: mapping land cover dynamics and productivity
- Science:
    - Radiometrics: atmospheric correction and cloud detection
    - Spatial and temporal resolution and how these affect analytics
- Practice:
    - The Planet API
    - Selecting cloud-free imagery
    - Ingestion into cloud-based processing engines
    
#### Reading
- Planet white paper on [surface reflectance](https://assets.planet.com/marketing/PDF/Planet_Surface_Reflectance_Technical_White_Paper.pdf)
- McCabe et al [(2017)](https://doi.org/10.1002/2017WR022240) (tentative)

#### Tools
- Dockerized agroimpacts/mapper Planet-query [function](https://github.com/agroimpacts/mapperAL/tree/feature/planet-query/spatial/python/planet) (update link)
- Sign-up for Planet 14-day [trial](https://www.planet.com/trial/)

[Back to TOC](#toc)

___

### Cloud-based Processing
#### Material covered
- Overview of our use case: assembling time series
- Science:
    - Impact on spatial and temporal scales of analysis
    - Multi-sensor fusion
- Practice:
    - Using EarthEngine and RadiantEarth
        - Collect cloud-free image time series, Landsat, MODIS, Planet
        - Calculate GNDVI and from that LAI
    
#### Reading
- Read the docs at [RadiantEarth](https://help.radiant.earth)
- An introduction to [COGs](https://medium.com/planet-stories/cloud-native-geospatial-part-2-the-cloud-optimized-geotiff-6b3f15c696ed)
- Gorelick et al [(2017)](https://doi.org/10.1016/j.rse.2017.06.031)

#### Tools
- Sign up for accounts on [RadiantEarth's app](https://radiantearth.auth0.com/login?state=6LlsOI74Hgbl6bmX57uZx9sBzwxzjFKM&client=xqRq3Jr8ePFd0FTqb6jIEw8t5kK2lF4W&protocol=oauth2&response_type=code&redirect_uri=https%3A%2F%2Fraster-foundry.auth0.com%2Flogin%2Fcallback&scope=openid%20email%20profile) and [EarthEngine](https://signup.earthengine.google.com/#!/)

[Back to TOC](#toc)

___

### Real-time _In Situ_ Sensors
#### Material covered
- Our use cases: estimating LAI from downward looking sensors, developing surface reflectance conversions, running crop models
- Science:
    - LAI, its measurement, and significance
    - Sensors and spatial and temporal variability
- Practice:
    - Accessing the Arable API
    - Calculating key variables at different temporal resolutions

#### Reading
- TBD

#### Tools
- R and [RStudio](https://www.rstudio.com/products/rstudio/download/#download) (both should be on classroom computers), and Arable's R client package (to be distributed separately). 

[Back to TOC](#toc)

___

### Human and Machine Intelligence
#### Material covered
- Our use case: Land cover mapping using active learning--machine learning guiding humans to collect most informative training data
- Science:
    - The nature of training data, its quality, and potential impact on maps
    - Consensus labelling
    - Active learning and complementary intelligence
- Practice:
    - Crowdsourced mapping
    - Accessing S3 buckets
    - Programmatic access to postgres/postgis databases
    - Spinning up AWS virtual machines

#### Reading
-TBD 

#### Tools
- Logon credentials to active learning project (to be provided)

[Back to TOC](#toc)

[Course Home](../README.md) | [General Info](general-information.md) | [Syllabus](syllabus.md) | [Projects](projects.md)