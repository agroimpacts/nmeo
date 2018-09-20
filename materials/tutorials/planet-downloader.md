# Running the Planet Downloader
## Install Anaconda and Dependencies 
### Windows
These instructions are based on installing everything new on a freshly started Windows Server 2016 instance.  Results will vary for already established machines, most likely. 

- On your Windows Box, download the latest Anaconda distribution from [here](https://www.anaconda.com/download/). Choose the Python 3.6 version
- You should be able to install without Admin privileges (Just Me option)
- On the Advanced Installation page, uncheck the "Add Anaconda to My Path..." option to prevent bad things happening to programs that depend on, say, Python 2.7. 
- You can then install. Skip the options that have you connect to the cloud, etc
- Install takes a while, but once down, you can search for `Anaconda Prompt` on your desktop and open that.  
- First, if you don't have it (but most of you do), install gdal.  I suggest installing [osgeo4w](http://download.osgeo.org/osgeo4w/osgeo4w-setup-x86_64.exe) - Run these commands from the Anaconda prompt


```bash
> pip install planet
> conda install -c conda-forge gdal
> conda install -c conda-forge rasterio
> pip install shapely
> pip install geojson
```

For an existing machine that already has gdal installed on it, I would try something like:
```bash
> pip install planet
> pip install rasterio
> pip install shapely
> pip install geojson
```

If rasterio gives you trouble, replace `pip install rasterio` with `conda install -c conda-forge rasterio`

A nice thing about installing conda is that it provides various libraries already, such as scipy, numpy, skimage, etc.  

A good way to verify that things are working is to get into the Anaconda shell and then run:
```bash
python
```

```python
>>> import rasterio
```

If that completes without complaining, the most difficult install is taken care of. 

### Mac
The same basic approach should also work for a Mac.  Except instead of using the Anaconda prompt, you will simply use Mac's Terminal. CMD-Space, type in "terminal", and you will be ready to live the command-line life. Before that, to get Python 3.X, I would also just go and download the Anaconda version for Mac. 

The same install instructions should work.  If you already have gdal, use the second sequence above. Remember the commands are entered in terminal. 

## Running the Downloader

After you have the steps above done, you should be able to run the downloader. 

Get the latest version of the GEOG287/387 repo. The easiest is to just clone it from GitHub or download it as a zipfile and unpack it somewhere where you want it. 

Next, make a folder where you want downloaded images to be sent. Make a sub-folder in that folder called "analytic_sr". 

Open the config.ini file in the materials/code/python folder that you got from the class repo. 

The top lines of the one I just ran in windows looks like this
```
[planet]
api_key: x9f35333xxxc4qdfb437ygh4fff44c2

[aoi]
x: -71.8071 
y: 42.12175
cell_size: 0.005

[dates]
month_start: 6
month_end: 6
day_start: 1
day_end: 30

[imagery]
catalog_path: C:\Users\airg\Desktop\images
```

You just need to replace the API key with your own Planet API key.  And you need to replace the catalog path with the directory to the folder where you want your images to go (**do not** include the "analytic_sr" in the path name).

Note, a Mac user will want to make the file path Unix-y, e.g. `/Users/airg/Desktop/images`.

Once you have made those two changes, you can run the downloader:

```
> python planet_downloader.py
```

Entered either into the Anaconda prompt (Windows) or terminal (Mac).

You should get these results:

```
Matching scene ID: 20180622_145904_1048
Matching scene ID: 20180622_145903_1048
Matching scene ID: 20180617_145943_0f2d
Matching scene ID: 20180617_150425_0f22
Matching scene ID: 20180617_150423_0f22
Matching scene ID: 20180616_145932_0f4d
Matching scene ID: 20180616_145931_0f4d
Matching scene ID: 20180612_150003_1043
```

If this doesn't work, please copy the complete error messages you get into our Slack channel.  


