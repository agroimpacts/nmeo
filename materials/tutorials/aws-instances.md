# AWS Virtual Machines

The following provides a set instructions for how to set up and use an AWS virtual machine running Windows Server 16, which can be used to install software on a machine that provides processing/memory/storage capacity you need for a particular job, accessed as a remote desktop. 

It assumes you already have a regular amazon.com account, and that you have gone through the process of requesting an AWS account associated with that account. 

Instructions, or links to other online instructions, are provided for various steps along the way, which includes setting up a user group, giving permissions, etc. Some or most of these you might not need, but are provided here for the sake of completeness.

### TOC
- [Administration](#administration)
    - [Setting up IAM user group](#setting-up-iam-user-group)
    - [Controlling access to the console](#controlling-access-to-the-console)
    - [Creating an IAM policy](#creating-an-iam-policy)
    - [Setting up an AWS Windows Server](#setting-up-an-aws-windows-server)
- [Using an AWS Virtual Windows Server](#using-an-aws-virtual-windows-server)

## Administration
### Setting up IAM User Group

*Under construction*

### Controlling access to the console
*Under construction, but [see here](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_controlling-access.html)*

#### Creating an IAM policy
These control how users can access and use a range of AWS resources. An administrator must assign policies to a specific user or user group. Here's a good example of [a policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_examples_ec2_tag-owner.html) that allows a user to start and stop EC2 instances that list that user's name as an Owner in the resource tag. To create this policy, you:

1. Go To IAM > Policies > Create Policy
2. Paste the copied policy into the JSON tab
3. Replace the *:* in this part `arn:aws:ec2:*:*:instance/*` with availability zone (e.g. us-east-1) and account number, e.g. us-east-1:511111111111
4. Hit Review Policy, name it something meaningful, and finish up
5. Go to Users or Groups under IAM, and then assign that policy to the user or group. 

#### Assigning an IAM Role to an Instance
You might need your AWS instance to be able to access other AWS resources, for example S3, so you have to assign an IAM role to it. 

To do that, you have to create an IAM role:

1. Got to IAM console > Roles > Create Role
2. Choose the IAM service you want to create the role for, in this case EC2
3. Click Next:Permissions, and you can either choose to create a policy, or select an existing one.  In this case, as an example, type in S3 into the filter window and choose AmazonS3ReadOnlyAccess
4. Click Next:Review, and then name it. 

Now go back to the EC2 console, find the instance you want to give those permissions to, and in the Instance Settings choose Attach/Replace IAM Roles. Find the policy you just made and assign it.  You will now have permissions. 

I used this approach to give permissions to a GPU instance on which I installed PIX4D. In this case, we needed to upgrade the GPU drivers to allow PIX4D's raycloud to be used, following [these instructions](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/install-nvidia-driver-windows.html), following all but steps 4-6, which seem out of date.  

### Setting up an AWS Windows Server

A pretty detailed overview is [here](https://aws.amazon.com/getting-started/tutorials/launch-windows-vm/). We are going to follow that, but I will note deviations and provide further context.

These instructions assume you are the administrator of the account, or a user who has sufficient permissions on EC2 to create a new "instance".   

1. Enter the EC2 Dashboard
2. Create your virtual machine, by selecting "Launch Instance"
    - These instructions are old, so we are going to select a _Microsoft Windows Server 2016 Base_, since there are newer versions.
    - Next in here we need to select an instance type. We are going to choose something beefier than a t2.micro, since we want to do some real work with this. So let's try a *c5.2xlarge*, which gives 8 virtual CPUs and 16 GB RAM.  
    - Click the "Next:Configure Instance" Button at the bottom of the Screen, leave the settings as is, and then click "Next:Add Storage"
    - On the storage page, leave setting as is, but make the hard drive equal to the size you want it. For this example, which arises out of creating an instance for processing a bunch of MODIS imagery, I am going to choose 100 GB.  
    - Click "Next:Add Tags", and on that page add a key ("Name") and value ("timesat", for this example--a VM for running timesat). 
    - Click "Next:Configure Security Group", and on that page you can choose to "Create a new *security* group", or "Select an *existing* security group" assign an existing security group.  I am going to select an existing group associated with another Windows Server instance I alread have, in this case *launch-wizard-21*. What this does is shown here: 

    ![](figures/ecs_sec_group.png?raw=true)
    
    - It is setting up an inbound rule to allow outside connections from the Clark University IP range to instance we are setting up.  Connections from other IPs will not be possibe. If you don't have access to an existing security group, you can mimic the settings you see for the IP ranges you want in the image above under the new security group option.  
    - Click "Review and Launch", followed by "Launch". That will first pop-up a dialog called "Select an existing or create a new key pair". Choose to create one if you haven't already done this, or point it to the name of one you already own.  Follow the instructions in the linked doc about how to set up a key pair for different OSs.  
    - After that, launch your instance.  It will take a few minutes to be ready to go. To monitor the status, go to the EC2 Dashboard and click the "Running Instance Link". You will see that an instance named "timesat" (this example) is getting ready. Once it has started, the status checks will show a green checkmark. It will look this: 
    
    ![](figures/ec2_dashboard.png?raw=true)
    
4. Now your instance is running, let's start Windows: 
    - Following the linked setup doc (step 4a), choose "Connect" at the top of the page, making sure you have checked the box next to your instance.  
    - Follow steps 4b-d), get and decrypt your administrator password (copy it somewhere safe--I use a password manager, so copy it in there where it is protected). 
    - Download the remote desktop file. Click to open it, and it will open on the remote desktop client you have chosen to use.  I use a Mac, so use Microsoft Remote Desktop. If you use Windows, they recommend Microsoft RDP I believe.  
    - That will open the Windows Server as a remote desktop, once you insert the admin password you just decrypted.  


5. Let's make this usable for a non-admin account
    - Once logged into the Windows Server, go to Control Panel > Users
    - Select "Manage another account", and then click to "Add a user account". 
    - Add a user name and password that is useful.
    - Next find the Computer Management dialog, then go to "Local Users and Groups" within it, and double-click on the "Users" folder, and select the "Member of" tab. Type in "Remote Desktop Users" into the "Enter Object Names to Select" dialog, click "Check Names" to verify you got the group name right, and finish by clicking "Okay". 
    - You should be all set up. Sign out of the Windows session, which will close down the VM

6. Log back in as the user you just created, using the same Remote Desktop Connection. It should work. 

[Back to TOC](#toc)

## Using an AWS Virtual Windows Server

1. First start up the virtual machine: 
    - If you have EC2 console permissions, what you will do is use your console sign-in link, e.g. https://551111111111.signin.aws.amazon.com/console, and then enter your admin-assigned user name and password.  
    - Go to EC2 > Instance, and then browse the list of available instances. Choose the one you need, and then Actions > Instance State > Start. It will spin up, taking a few minutes before ready. If you don't have permissions for this instance, you will not be able to start it. 
    - If you don't have permissions, ask the admin to start it. 
    
2. Install the right remote desktop client, and open it. Choose create a new connection. If you are using Microsoft Remote Desktop it will look like this: 

    ![](figures/rdc_conn.png?raw=true)

    - Enter a memorable name for the connection
    - PC name is the AWS Public DNS for the instance, which you will either be provided by the Admin or get from the Instance dialog in the Management Console, if you have permissions. Important: you will have to put in a new DNS each time you start the instance up again, as it doesn't stay fixed (unless we buy a fixed IP for the instance).  
    - If you want to transfer files from your local computer to the VM, then you select the "Redirection" tab, and then point the dialog to the local folder you want to mount on the VM. You can mount multiple folders this way. 
    - Then connect. If you chose a local folder to mount, you should see it appear in the "This PC" section of the Windows Explorer. 
    - Start installing your software as needed. 
    
3. Stop the instance when you done.
    - Log out
    - If you have permissions, go to the EC2 console and either stop or terminate the instance.  If you terminate the instance, it means all the set up will be destroyed, and all the data you uploaded will be lost.  Stopping is safest if you plan to keep using that instance. If you terminate the instance, and want to save all the installs, you can choose to make an image of the instance.  To do that:
        - Under Actions > Instance State, click Stop
        - Once the machine has stopped completely (it takes a bit), go to Actions > Image > Create Image. Name it something memorable, choose a size for the output disk, and then "Create Image"
        - You can then terminate the instance once the image is created, (it might take a little while to create). 
        - The beauty of this is that you can create a new instance, either bigger or smaller, using this image, and it will have everything you installed on it from the get go.  This helps if you decide the original instance size/type you chose wasn't the right one for the job. 

### Even better, use the CLI

Controlling instances can be even easier if use the AWS Command Line Interface (CLI), which allows you to start and stop an instance and describe it from the command line on your local computer.  

First, you have to install the CLI.  Directions on how to do that are [here](https://docs.aws.amazon.com/cli/latest/userguide/installing.html) 

For Windows users, there are also a few ways you can go with respect to using the command line. This is taken from our wiki for the active learning project: 

> One good way to go on Windows...is to install Cygwin on your desktop or laptop: https://www.cygwin.com. The latest version, 2.10.0 was released 2/2018. Cygwin provides a large collection of GNU and Open Source tools which provide functionality similar to a Linux distribution on Windows.

> Another alternative - that requires no knowledge of Linux - is to install a Windows terminal emulator, such as PuTTY, available here: https://www.chiark.greenend.org.uk/~sgtatham/putty and https://www.ssh.com/ssh/putty/download.

If you have the CLI installed and working, and have set your path to find the tools (instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#awscli-install-windows-path)) then it becomes fairly easy to use it. 

For example, start an instance with the id `i-0c138e67140b7e65`:

```
aws ec2 start-instances --instance-ids i-0c138e67140b7e65
```

Retrieve its public DNS name once it is spinning (note you might not have permissions to do this if the admin hasn't given it to you):

```
aws ec2 describe-instances --instance-ids i-0c138e67140b7e650 --filters --query "Reservations[].Instances[].PublicDnsName"
```

Stop it when you are done: 

```
aws ec2 stop-instances --instance-ids i-0c138e67140b7e65
```

### Expand the volume

Perhaps you need more EBS storage space.  If so, follow [these instructions](https://aws.amazon.com/premiumsupport/knowledge-center/expand-ebs-root-volume-windows/). [These](https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ebs-modify-volume.html ) are also helpful.

[Back to TOC](#toc)        
    


    
