# Linux/Unix/OSX shell commands and scripting

## Working with the command line

Working with open source software, large datasets, and many cloud
resources is greatly aided by an understanding of how to use shell
commands and/or scripts in a [Unix-like operating
system](https://en.wikipedia.org/wiki/Unix-like), e.g. Linux
distributions, MacOS, etc. They can make your life much easier for
tedious, repetitive tasks (manipulating large numbers of files,
executing many small jobs, etc). These commands do not require you to
have a \*nix-based OS, you can instead install programs such as git-bash
(available [here](https://git-scm.com/download/win)) that provide a
linux terminal emulator for Windows machines.

The following document provides some standard Linux commands and a few
tasks that you can use to get familiar with shell commands. What is a
shell (a good answer is
[here](https://en.wikipedia.org/wiki/Shell_%28computing%29),
specifically the section on command-line shells)? Many if not most
\*nix-based systems use the `Bash` shell, so we will work with that
(although I have set `zsh` as the default shell on my Macbook).

## Basic commands

``` bash
# What directory am I in?
pwd 

#-----------------------------------------------------------------#
# What files/folders are in the directory I am in?
ls 

# What files/folders are in some other directory?
ls ../some/other/directory

# What are the details (e.g. file size, permissions, dates) 
# of the files/folders in some other directory
ls -l ../some/other/directory

# The above, but summarize file sizes in MB
ls -lh ../some/other/directory

# How many files and folders are in the current directory?
ls | wc -l

# How many files and folders are in the current directory 
# and all its sub-folders (-R means recursive)
ls -R | wc -l

#-----------------------------------------------------------------#
# Change from your current directory to some other directory
cd ../some/other/directory

#-----------------------------------------------------------------#
# Copy a file from one directory to some other directory
# Note: if you don't want to change the file name, you can 
# just leave off the "somefile.txt" after the 
# ../some/other/directory/. You can specify a different name
# if you want the file to be named differently in the new location
cp somefile.txt ../some/other/directory/somefile.txt

# copy all files (but not sub-folders) in directory 
# to some other directory
cp * ../some/other/directory/

# the above, including sub-folders
cp -R * ../some/other/directory/

# the above, but copying from a directory different to the one 
# you are in to some other directory
cp -R ../yet/another/directory/* ../some/other/directory/

#-----------------------------------------------------------------#
# move some file to some other directory. As wth copy, you 
# don't have to specify the file name if you don't want to 
# rename it
mv somefile.txt ../some/other/directory/somefile.txt

# Move all files and sub-folders from your current directory to 
# some other directory--note with mv you don't have to specify -R 
# to move sub-folders
mv * ../some/other/directory/

#-----------------------------------------------------------------#
# Delete somefile from your current directory
# CAUTION!!!! Be very sure when you use rm, as there is no recycle 
# bin. It is permanent
rm somefile.txt

# Delete all files in the current directory (but not sub-folders)
rm *

# The above, including sub-folders
rm -r * 

# The above, including sub-folders, from some/other/directory
rm -r * 

# Delete some other directory and everything in it
rm -r ../some/other/directory

#-----------------------------------------------------------------#
# make a new directory on the same level are the directory you are in
# (that is what the .. means, which is explained more below)
mkdir ../new_dir

# make a new sub-directory in the new directory that is nested two 
# levels down
mkdir -p ../new_dir/sub1/sub2

#------------------------------------------------------------------#
# Print your path variables. These list the directories that the 
# shell searches for executables. If you install an executable in 
# a directory not listed here, you have to add that directory to 
# your path variable. 
echo $PATH

# Create and reuse a variable in your current shell session. 
# Here the example is a directory. 
SOMEOTHERDIR=/my/home/directory/some/other/directory
echo $SOMEOTHERDIR
ls $SOMEOTHERDIR | wc -l

# To be continued...
```

## Working with Paths

You will note in the examples above that there is often `..` preceding
the path to `some/other/directory`. The indicates that the directory you
are working in is on the same level as `some/other/directory`. The ..
tells the shell to back out of the directory you are in.

If, on the other hand, you had moved out of that directory back to its
parent directory, then the commands would change as follows, taking the
example given for copying some file to some other directory

``` bash
# original, commented out
# cp somefile.txt ../some/other/directory/somefile.txt
cd ..  # move out of the current directory
cp directory/I/just/left/somefile.txt some/other/directory/
```

You can always circumvent the uncertainty about the front part of paths
by specifying full paths, including the root. As you saw before `pwd`
gives the full path to your current location, including your home
directory. You can also find your home directory by running
`echo $HOME`, and if the folders you are working on are just below your
home directory, you can do something like this instead:

``` bash
ls $HOME/some/other/directory
cp $HOME directory/I/just/left/somefile.txt $HOME/some/other/directory/
```

Of course, if those directory are nested deeper than \$HOME, you have to
specify the sub-folders in between.
