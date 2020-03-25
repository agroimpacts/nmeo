# Geog 387 Lab
By Adam Wolf

Code from [here](https://github.com/wolfhelius/Clark_Geog387)

# Overview
There are three notebooks here for exploring ground data versus gridded products.  The goals here are to explore data, develop some interpretations, model these data in simple ways, gain exposure to REST APIs, and to use various functions in the PyData ecosystem (pandas, numpy, matplotlib, geopandas).  

You may need to install a couple libraries, e.g. geopandas.  You can do this on the command line as `pip3 install geopandas` or within the notebook as `!pip3 install geopandas`

Lyndon will pass along a file `config.yml` that has various API keys and passwords.  Put this in the same directory as these notebooks.

## Install notes (for GEOG287387 virtual machines)
To run this, you will need to install the following additional `python` packages. Open the Anaconda Powershell prompt, and then run:

```bash
conda config --add channels conda-forge
conda config --set channel_priority strict
conda create -n sensorlab python=3.7 geopandas descarteslabs jupyterlab 
conda activate sensorlab
conda install matplotlib 
conda install joblib
conda install pyyaml
```

Follow the prompts to install the various packages as they arise. Once it completes, within the Powershell, run the following:

```bash
conda activate sensorlab
cd D:\Users\<user>\Documents\geog287387\materials\code\sensors\
jupyter lab
```

Where the <user> in the CD line is replaced by yout user name, and then amend the path as needed to get to where your geog287387 repo lives. This will open up a new `jupyterlab` environment in your browser, which will open right to where the notebooks are installed.  

