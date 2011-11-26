# I NO LONG MAINTAIN THIS. Please follow [Yvan's Fork](https://github.com/ygjb/Garmr)



# Garmr

Garmr is a checking that a site meets the basic requirements from a security point of view. 
It checks what the correct HTTP calls are allowed and others are blocked. It is installable from PyPi.

## Installation

To install it is a simple case of 
  sudo pip install garmr

## Usage

garmr -u http://application.under.test/path

This will create a file called garmr-results.xml which will have the results of the 
tests stored in it.

### Options

* "-u", "--url": Url to be tested 
* "-f", "--file": File name with URLS to test, Currently not available 
* "-x", "--xunit": Name of file that you wish to write to. Defaults to garmr-results.xml


## Tasks

If you want to see what is currently being worked on you can see it on the 
[Pivotal Tracker](https://www.pivotaltracker.com/projects/285905)
