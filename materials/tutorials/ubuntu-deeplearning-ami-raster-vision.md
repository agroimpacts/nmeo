# Configuring an AWS Ubuntu Deep Learning AMI for `raster-vision-examples`

This assumes that you have the following steps already done: 

- An AWS profile set up on your local machine with the necessary permissions. 
- A security group set up with permissions that allow access to port 8888 from your relevant IP addresses. 

This approach has been tested and successfully run on the Potsdam semantic segmentation example. 

## Configure an on-demand instance

Working through the EC2 console, launch an instance and select AWS's Ubuntu Deep Learning AMI, and use a p2.xlarge (cheaper). Assign the security group you already have that has port 8888 open to relevant IPs. Give it a tag with a Name that is meaningful to you. 

### Add your ssh public keys

Copy and paste your public ssh key into ~/.ssh/authorized_keys.  You can then log in to the instance simply as: 

```bash
ssh ubuntu@<new-public-ip>
```

### setup `jupyter notebooks`

Followed instructions here, starting with [this](https://docs.aws.amazon.com/dlami/latest/devguide/setup-jupyter-configure-server.html). Didn't need it because already had port 8888 open. 

Then moved to [here](https://docs.aws.amazon.com/dlami/latest/devguide/setup-jupyter-start-server.html) to active the python3, and then [here](https://docs.aws.amazon.com/dlami/latest/devguide/setup-jupyter-configure-client-mac.html) to configure the Mac/Linux client. Note that the directions they give for that are the same for Mac and Linux, and I think they would be the same for cygwin on Windows.  Also note that I did them a bit differently, since I already had installed my public key on the instance's authorized_keys: 

```bash
ssh -L 8157:127.0.0.1:8888 ubuntu@<new-public-ip>
```

That logs us in, and we are then able to get the running `jupyter notebook` server token from the instance we are already ssh'd into (launched step before this), and then log in to the server through a browser as follows:

```bash
http://127.0.0.1:8157/?token=token-string-here
```
The ssh connection established right above this has to be live still.  

### nvidia-docker, etc

These are all already installed on this AMI, which is generally confirmed by running: 
```bash
cat /proc/driver/nvidia/version
```

Which reveals:
```bash
NVRM version: NVIDIA UNIX x86_64 Kernel Module  396.44  Wed Jul 11 16:51:49 PDT 2018
GCC version:  gcc version 5.4.0 20160609 (Ubuntu 5.4.0-6ubuntu1~16.04.10) 
```

### Install raster-vision-examples

```bash
git clone https://github.com/azavea/raster-vision-examples.git
```

We need to make a few changes to have this work: 

```bash
cd raster-vision-examples
vim scripts/console
```
Edit line 42 to look like this: 

```bash
IMAGE=raster-vision-examples-gpu
```

Previously it ended in "-cpu"", and thus it would foil us by launching a CPU container. Next, we have to edit line 34 to look like this: 

```bash
docker run --runtime=nvidia ${NAME} --rm -it ${TENSORBOARD} ${AWS} ${RV_CONFIG}
```
It currently looks [like this](https://github.com/azavea/raster-vision-examples/blob/bbccd79ab6fc2b43378557ab87b4919a504f88ee/scripts/console#L34): 


### Create an AMI from it
Now it's basically all configured, so we can turn it into an AMI that we can use to launch a much cheaper and more capable spot instance. 

These commands will work, when applied to an instance that we gave the name "airg_ubuntu_dl_ami", when run from the linux command line. 
```bash
# get the instance ID
INAME=airg_ubuntu_dl_ami
IID=`aws ec2 describe-instances --filters 'Name=tag:Name,Values='"$INAME"'' \
--output text --query 'Reservations[*].Instances[*].InstanceId'`

# Create the AMI
AMIID=`aws ec2 create-image --instance-id $IID --name "$INAME image" \
--description "AMI of $INAME 30Nov2018"`
```

## Launch a spot instance

Once the AMI is ready, we can launch a spot instance. The command below will use the stored AMI id in the bash variable above, then launch a p3.2xlarge in our availability zone (us-east-1) with a volume size of 110GB, under a persistent spot request that will pay up $1.25/hour and the request will be valid until December 16 at 11 pm. 
```bash
aws ec2 run-instances --image-id $AMIID --count 1 --instance-type p3.2xlarge --key-name airg-key-pair --security-groups airg-security --monitoring Enabled=true --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=airg_ubuntu_gpu_dl2}]' --instance-market-options 'MarketType=spot,SpotOptions={MaxPrice=1.25,SpotInstanceType=persistent,ValidUntil=2018-12-06T23:00:00,InstanceInterruptionBehavior=hibernate}' --block-device-mappings file://mapping.json
```
Note that this command uses information stored in the file mapping.json, which has the following contents: 
```
[{
  "DeviceName": "/dev/sda1",
  "Ebs": {
    "VolumeSize": 110
  }
}]
```

We execute the command from the same directory that json is stored in.  It specifies the volume size of the instance. 

Once that is running, ssh into the image, using just:
```bash
ssh ubuntu@<new-public-ip>
```

Then we will do some cleaning up of docker containers that might already have been on the AMI we created above (while testing this out we ran scripts/build and ended up with a CPU container on the instance. 
```bash
docker system prune -a
```

This removes and CPU containers that were previously installed during the image creation process, and then we can get a fresh new GPU container. To do that, we execute: 

```bash
cd raster-vision-examples
scripts/build --gpu
```

Then we should be ready to follow the examples.  We have tested this on the Potsdam segmentation example, which we can follow from [here](https://github.com/azavea/raster-vision-examples#isprs-potsdam-semantic-segmentation)

First download the data to a relevant S3 bucket, and then execute the command: 

```bash
rastervision run local -e potsdam.semantic_segmentation -a root_uri s3://agroimpacts/raster-vision/potsdam/lde -a data_uri s3://agroimpacts/raster-vision/Data
```

It should run, although the ssh connection is likely to be lost part way through. If that happens, it does not necessarily kill the run, but you won't be able to log back into the container. However, you can see what is going on if, upon ssh'ing back in, you run:

```bash
docker ps
```

If the container is still running, it will show you something like this
```bash
CONTAINER ID  IMAGE                       COMMAND CREATED     STATUS      
31565774305f  raster-vision-examples-gpu  "bash"  5 hours ago Up 5 hours  
PORTS                              NAMES
0.0.0.0:6006->6006/tcp, 8888/tcp   laughing_bartik
```

Copy the container ID, and then run

```bash
docker logs 31565774305f
```

That will show you where the container is in its run, e.g. 

```bash
INFO:tensorflow:global step 53690: loss = 0.2710 (0.321 sec/step)
INFO:tensorflow:global step 53700: loss = 0.4517 (0.320 sec/step)
INFO:tensorflow:global step 53710: loss = 0.3777 (0.317 sec/step)
INFO:tensorflow:global step 53720: loss = 0.3549 (0.318 sec/step)
INFO:tensorflow:global step 53730: loss = 0.4178 (0.322 sec/step)
INFO:tensorflow:global step 53740: loss = 0.5255 (0.323 sec/step)
INFO:tensorflow:global step 53750: loss = 0.3123 (0.324 sec/step)
INFO:tensorflow:global step 53760: loss = 0.4218 (0.320 sec/step)
```

