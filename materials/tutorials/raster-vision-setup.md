# Setting up and Running raster-vision

This requires an install of `docker` 18 and an AWS Batch account set-up

## Set-up AWS Batch

These are updated instructions relative to what is available in the existing docs. First, you have to git clone the Azavea repo for raster-vision-aws. So, find a nice folder location somewhere.  I use my own designated directory for projects: ~/Dropbox/projects/, so from a terminal I run 

```
cd ~/Dropbox/projects
git clone git@github.com:azavea/raster-vision-aws.git
```

That creates a local clone of that repo.  I then have to install the AWS CLI tools, if I haven't already, and then run the following:

```
aws --profile raster-vision-airg configure
AWS Access Key ID [****************F2DQ]:
AWS Secret Access Key [****************TLJ/]:
Default region name [us-east-1]: us-east-1
Default output format [None]:
```

Make the packer image.
```
make packer-image
```

In Ubuntu/Linux, you probably will need to run sudo


The next step is not clear from the documentation, which is that you have to do this:
```
cd raster-vision-aws
cp settings.mk.template settings.mk
```

Next, you need to edit settings.mk, the contents of which look like this:

```
# Settings for create-ami
AWS_BATCH_BASE_AMI := ami-XXXXXXXX
AWS_ROOT_BLOCK_DEVICE_SIZE := 50

# Settings for create-batch
#  AMI_ID is derived from the packer step.
AMI_ID := ami-XXXXXXX
KEY_PAIR_NAME := airg-key-pair.pem
AWS_REGION := us-east-1

# Settings for ECR
RASTER_VISION_IMAGE := raster-vision-gpu
ECR_IMAGE := rastervision
ECR_IMAGE_TAG := latest
```

You will need to initially get values for the AWS_BATCH_BASE_AMI by following [these steps here on the README](https://github.com/azavea/raster-vision-aws#find-the-base-ami). Use a text editor to replace the ami-XXXXXXXX with the ami-id you find following those steps. 

Next run: 

```
make create image
```

However, we need to make some changes first, based on feedback at Azavea, in packer/scripts/configure-gpu.sh, change this line:

```
sudo docker run --privileged --runtime=nvidia --rm nvidia/cuda nvidia-smi
```

To this:

```
sudo docker run --privileged --runtime=nvidia --rm nvidia/cuda:9.0 nvidia-smi
```

Based on comments by @martham93 on Azavea's [gitter channel](https://gitter.im/azavea/raster-vision?at=5bd52c646e5a401c2ddfefc3).

You then wait for the process to finish, and at the end, it will spit out the AMI ID. Reopen the 

## Getting a container running

We will use the class folder structure for this. According to Azavea's [Quickstart documentation](the first step) to running a docker-ized version of `raster-vision` is to set up some target folders. For our purposes, and for the sake of consistency, make a folder under our existing  materials/code/ directory named "raster-vision". And then under that make sub-folder "code" and "rv_root"

Here are the terminal commands for doing that, which you can run out of Rstudio's terminal. If you are on Windows and want a different terminal environment, you will have to install something like `cygwin` or `GitBash`.  

```
mkdir materials/code/raster-vision

```

Now we have to run the following commands, also in our terminal
```
cd materials/code/raster-vision
export RV_QUICKSTART_CODE_DIR=`pwd`/code
export RV_QUICKSTART_EXP_DIR=`pwd`/rv_root
mkdir -p ${RV_QUICKSTART_CODE_DIR} ${RV_QUICKSTART_EXP_DIR}
```

Now we can run a docker container
