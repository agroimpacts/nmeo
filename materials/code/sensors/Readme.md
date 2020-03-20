# Geog 387 Lab
By Adam Wolf

Code from [here](https://github.com/wolfhelius/Clark_Geog387)

# Overview
There are three notebooks here for exploring ground data versus gridded products.  The goals here are to explore data, develop some interpretations, model these data in simple ways, gain exposure to REST APIs, and to use various functions in the PyData ecosystem (pandas, numpy, matplotlib, geopandas).  

You may need to install a couple libraries, e.g. geopandas.  You can do this on the command line as `pip3 install geopandas` or within the notebook as `!pip3 install geopandas`

Lyndon will pass along a file `config.yml` that has various API keys and passwords.  Put this in the same directory as these notebooks.

## Install notes (for GEOG287387 virtual machines)
To run this, you will need to install the following additional `python` packages. Open the Anaconda prompt, and then:

```bash
conda activate rstudio
conda install pandas
# conda install geopandas
conda install -c conda-forge geopandas
#pip install pyproj  # note this might be needed
conda install matplotlib
conda install joblib
conda install -c conda-forge descarteslabs
```



