[Course Home](../README.md) | [General Info](general-information.md) | [Syllabus](syllabus.md) | [Projects](projects.md)

## Introductory Modules

An overview of each of the modules that we will cover in the first 10 weeks or so.

Return to [syllabus](syllabus.md) or the course [home page](../README.md).

### TOC

- [Introduction](#Intro)
- [Drones](#drones)
- [Small Sats](#small-sats)
- [Cloud-based Processing](#cloud-based-processing)
- [Real-time _In Situ_ Sensors](#real-time-in-situ-sensors)
- [Human and Machine Intelligence](#human-and-machine-intelligence)
- [Data Visualization](#data-visualization)

___

### Intro
#### Material covered

- Key limitations to Earth Observation (EO) and recent advances to overcome these limitations.
- Software requirements for the course

#### Reading

- McCabe et al. [(2017)](https://agupubs.onlinelibrary.wiley.com/doi/epdf/10.1002/2017WR022240) 

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
        - Collecting images (virtual field excursion to [Whittier Farms](http://www.whittiers.com), specifically [here](https://goo.gl/maps/fFhJ25cRDXz))
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
- Jain et al [(2016)](https://doi.org/10.3390/rs8100860)
- Houborg et al [(2018)](https://doi.org/10.3390/rs10060890) Read abstract, Intro, Discussion, try to get a general idea of Methods/Results. Also [video here](https://www.youtube.com/watch?v=qCwAqWCGnI8), lecture on CESTEM starts at 12:50.

#### Tools
- Dockerized agroimpacts/mapper Planet-query [function](https://github.com/agroimpacts/mapperAL/tree/feature/planet-query/spatial/python/planet) (update link)
- Sign-up for Planet 14-day [trial](https://www.planet.com/trial/)
- NICFI free monthly [basemaps](https://www.planet.com/nicfi/)

[Back to TOC](#toc)

___

### Cloud-based Processing
#### Material covered
- Overview of our use case: assembling time series
- Science:
    - Impact on spatial and temporal scales of analysis
    - Multi-sensor fusion
- Practice:
    - Using EarthEngine and Astraea EarthAI notebook:
        - Collect cloud-free image time series, Landsat, MODIS, Planet
        - Calculate GNDVI and from that LAI
    
#### Reading
- An introduction to [COGs](https://medium.com/planet-stories/cloud-native-geospatial-part-2-the-cloud-optimized-geotiff-6b3f15c696ed)
- Gorelick et al [(2017)](https://doi.org/10.1016/j.rse.2017.06.031)
- Deines et al [(2019)](https://www.sciencedirect.com/science/article/pii/S0034425719304195?casa_token=Rjcq_FNmuKIAAAAA:Eky8pi4q96goyVdultkYvRBf0Ea_q-VYhsGtRMQXCUrLaJTrujNUuemkBjP1I_bmRaH9Do6KfQ). 

#### Tools
- Sign up for an account on [EarthEngine](https://signup.earthengine.google.com/#!/) 

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
- Antony et al [(2020)](https://doi.org/10.3390/su12093750)

#### Tools
- Python and [Jupyter Labs](https://jupyter.org/) (both should be on classroom computers), and Arable's Python client package (to be distributed separately). 

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
    - Implementing Mapping Africa platform
    - Fitting a deep learning model

#### Reading
- [Elmes et al, 2020](https://doi.org/10.3390/rs12061034)
- Deep learning readings tbd


#### Tools
- Deep learning tutorial (TBD)

[Back to TOC](#toc)

___

### Data Visualization
#### Material covered

- New developments in EO data visualization for different software

#### Reading

- TBD 

#### Tools
- Unfolded (https://docs.unfolded.ai/)


[Back to TOC](#toc)

[Course Home](../README.md) | [General Info](general-information.md) | [Syllabus](syllabus.md) | [Projects](projects.md)