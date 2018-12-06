# Setting up AWS Ubuntu AMI to run Azavea's `rastervision`

The following provides an overview of setting up a resource on AWS that can be used to run `rastervision` deep learning framework.  

This entails setting up a smaller non-GPU Ubuntu instance, provisioning it with the software it needs, and then using that to create an AMI that can then be used to launch GPU capable spot instances (to save money). 

We are choosing this model due to initial difficulties with setting up the AWS Batch runner approach.  

## Instance selection

We start with t2.xlarge, which gives decent resources so that we can use this instance for somewhat larger computing if we only need CPUs. So we set up an Ubuntu 16.04 server AMI, give it a 70GB hard drive, and assign the airg security group. After that is started and running, we can log in and run via SSH.  

```bash
ssh -i ~/Desktop/my-key.pem ubuntu@11.222.333.444
```

To avoid having to use the .pem key, we can add our public keys to the authorize_keys file:

```bash
vim ~/.ssh/authorized_keys
```

And paste the key in at the bottom. 

### Configurations
#### Install Anaconda/Jupyter notebooks 

I followed these [directions](https://medium.com/@alexjsanchez/python-3-notebooks-on-aws-ec2-in-15-mostly-easy-steps-2ec5e662c6c6), but used their choice to get most recent download from [here](https://www.anaconda.com/download/#linux). 

#### Install `gcc`

```
sudo apt install gcc
```

#### Install Nvidia docker drivers

I followed this when I was trying to set up the AWS Batch capability for raster-vision.  Not 100% sure if it is necessary now, but retaining record of it here for the time being. 

Starting with directions [here](https://chunml.github.io/ChunML.github.io/project/Installing-NVIDIA-Docker-On-Ubuntu-16.04/), went to Nvidia's Cuda [install page](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#system-requirements), and worked through all steps. 

##### CUDA install

The t2.xlarge is not CUDA capable as one of the initial checks, but most of the install was fine.  

Followed through all the directions, getting local package manager install for CUDA-toolkit.  I didn't have a GPU capable instance, so couldn't verify the final Nvidia installation with the `cat /proc/driver/nvidia/version` command, but `nvcc -version` shows I have the driver installed. 

To make sure I had the cuda path permanently added to my path, I added this line to ~/.profile:
```bash
PATH=/usr/local/cuda-10.0/bin${PATH:+:${PATH}}
```

And then run `source ~/.profile`

##### `nvidia-docker2` install

After the CUDA stuff, I returned back to  [here](https://chunml.github.io/ChunML.github.io/project/Installing-NVIDIA-Docker-On-Ubuntu-16.04/) and continued with the docker install instructions. 

When I got to final step, I had problem with permissions:

```bash
> docker run --runtime=nvidia --rm nvidia/cuda nvidia-sm
docker: Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Post http://%2Fvar%2Frun%2Fdocker.sock/v1.39/containers/create: dial unix /var/run/docker.sock: connect: permission denied.
```

I solved that by doing this (from [here](https://techoverflow.net/2017/03/01/solving-docker-permission-denied-while-trying-to-connect-to-the-docker-daemon-socket/)):
```bash
sudo usermod -a -G docker $USER
# sudo usermod -a -G docker ubuntu
```

And then logging out and ssh'ing back in, I was able to run it, but then hit the bottleneck after here:

```bash
docker: Error response from daemon: OCI runtime create failed: container_linux.go:348: starting container process caused "process_linux.go:402: container init caused \"process_linux.go:385: running prestart hook 1 caused \\\"error running hook: exit status 1, stdout: , stderr: exec command: [/usr/bin/nvidia-container-cli --load-kmods configure --ldconfig=@/sbin/ldconfig.real --device=all --compute --utility --require=cuda>=10.0 brand=tesla,driver>=384,driver<385 --pid=926 /var/lib/docker/overlay2/ac5a4b3305282f28ec306e9da291bef7915dd09f0776cbe53a34ed4d5ceb9ece/merged]\\\\nnvidia-container-cli: initialization error: cuda error: no cuda-capable device is detected\\\\n\\\"\"": unknown.
```

So that is due to the fact that this is being set up on a non-GPU instance. I leave that here as is, because I was unable to get through AWS Batch set up described [here](https://github.com/azavea/raster-vision-aws).   I describe as far as I got in the next section:

#### Clone raster-vision-aws repo

```bash
git clone https://github.com/azavea/raster-vision-aws.git
```

#### Install aws-cli

```bash
sudo apt install awscli
```

Then set up aws configuration, as follows:

```bash
aws --profile airg configure
```

Entering in the key, secret key, zone (us-east-1), etc. 

To make sure I had my AWS_PROFILE permanently added to my path, I added this line to ~/.profile:
```bash
export AWS_PROFILE=airg
```

#### Install terraform

Following [instructions](https://www.terraform.io/intro/getting-started/install.html)

```
wget https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip
```

Unpacking terraform required installing zip
```
sudo apt install zip
unzip terraform_0.11.10_linux_amd64.zip 
```

Then move the `terraform` binary to /usr/local/bin
```
sudo mv terraform /usr/local/bin/
```

#### Then go through the steps:
```bash
make packer-image
make create-image
make plan
make apply
```

However, `make plan` is preventing me from running based on permissions, something about missing CreateRole permissions, for which I added a policy and attached to the airg user, but still no joy. So stopping here in favor of just running the instance directly as a p3.2xlarge, since we are on AWS already (in fact kind of dumb to use Batch) 

But first we will finish configuring the instance as needed. 

### Install docker-ce instead

Note the above was related to nvidia-cuda. Since we are not doing AWS Batch the above is skipped in favor of straight up install of docker-ce without nvidia drivers. We follow [these directions](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce-1), which exactly match the previous set, without the cuda part first. 

### Install raster-vision-examples

To start off running `rastervision`, we will try run one of the examples.  Therefore:

```bash
git clone https://github.com/azavea/raster-vision-examples.git
```

#### Allow jupyter/scripts to run

We need to be able to run jupyter notebooks from within the raster-vision-examples folder using their scripts, which requires doing the same steps described in our previous tutorial for setting up a jupyter capable Rstudio instance, which are [here](aws-rstudio-jupyter-setup.md#running-the-raster-vision-examples-jupyter-notebook). Once the configurations changes described there are made, the jupyter notebooks in the raster-vision-examples repo can be run using a local browser to log into the instance (see below and in previous tutorial). First we will set up the GPU instance. 

## Converting to GPU-capable spot instance
### Create image of running instance
This requires first stopping the instance, using the name we originally assigned to it within an AWS CLI command. 
```bash
INAME=airg_ubuntu2
IID=`aws ec2 describe-instances --filters 'Name=tag:Name,Values='"$INAME"'' \
--output text --query 'Reservations[*].Instances[*].InstanceId'`
echo Stopping instance named $INAME with id $IID
aws ec2 stop-instances --instance-ids $IID
```

Then we create the image from that instance. 
```bash
AMIID=`aws ec2 create-image --instance-id $IID --name "$INAME image" \
--description "AMI of $INAME 30Nov2018"`
```

### Set up new GPU spot instance
We can then launch a new instance from that AMI, once it is ready. We launch a p3.2xlarge with a Spot Request, where we set the instance maximum price we want to pay at 1.25. 
```bash
AMIID=ami-017f2bcbc0540a338
aws ec2 run-instances --image-id $AMIID --count 1 --instance-type p3.2xlarge --key-name airg-key-pair --security-groups airg-security --monitoring Enabled=true --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=airg_ubuntu_gpu_dl2}]' --instance-market-options 'MarketType=spot,SpotOptions={MaxPrice=1.25,SpotInstanceType=persistent,ValidUntil=2018-12-06T23:00:00,InstanceInterruptionBehavior=hibernate}'
```

Once that starts running, we can then ssh into our new instance, simply updating our last ssh command with the new public DNS for that instance.  Since our public key is already in the image, we can log right in without referring to the .pem. For this example, looking the "Spot Requests" tab in the ec2 console shows us that the zone our instance is running in (us-east-1f), the price hasn't exceeded about $1.22 in the past week, so we should be safe. 

## Run spacenet example

Having a running p3.2xlarge, we can run the spacenet example. So, working through the steps

### Run `scripts/jupyter` to set up datasets

```bash
scripts/jupyter
```

You get an output that looks so:
```bash
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(3bd8e26b6bfa or 127.0.0.1):8888/?token=a-long-token-string
```
Copy :8888 and everything to the right of it. Copy that to a bash variable as follows:

```bash
TOKEN=:8888/?a-long-token-string
```

Then, get the public DNS name for the instance. You can do that by going to the console and finding and copying that information, or from the command line notebook:
```bash
INAME=airg_ubuntu_gpu
IID=`aws ec2 describe-instances --filters 'Name=tag:Name,Values='"$INAME"'' \
--output text --query 'Reservations[*].Instances[*].InstanceId'`
DNSNAME=`aws ec2 describe-instances --instance-ids $IID --filters --query "Reservations[].Instances[].PublicDnsName"`

echo $DNSNAME$TOKEN
```

The output will be something like this:
```bash
ec2-000-11-222-333.compute-1.amazonaws.com:8888/?a-long-token-string
```

That can simply be pasted into your local browser and you will be in the jupyter notebook. Navigate to the spacenet notebook and run it. The only thing that needs changing in it is the s3 path in the very first notebook chunk, which we set to (for our example): s3://agroimpacts/raster-vision/spacenet

Once that is done, then:

### Run the spacenet example

First, we have to enter the docker image. 
```bash
scripts/console
```

Once in the image, we are going to run this as if it is local, so use this command. 
```bash
rastervision run local -e spacenet.rio_chip_classification -a root_uri ${RVROOT}
``` 

But replace ${RVROOT} with a relevant s3 directory name, in our example s3://agroimpacts/raster-vision/spacenet, which is the same directory we gave at the top of the jupyter notebook above. 

It will take about 3 hours on a p3.2xlarge to complete. 