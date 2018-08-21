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
        - Set-up AWS virtual server (maybe)
        - Mosaicking
        - Preliminary analyses

#### Reading

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
#### Reading
#### Tools

[Back to TOC](#toc)

___

### Real-time _in situ_ sensors
#### Material covered
#### Reading
#### Tools

[Back to TOC](#toc)

___

### Human and Machine Intelligence
#### Material covered
#### Reading
#### Tools

[Back to TOC](#toc)
