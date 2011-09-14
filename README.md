# Garmr

Garmr is a checking that a site meets the basic requirements from a security point of view. 
It checks what the correct HTTP calls are allowed and others are blocked. It is installable from PyPi.

## Installation

This version of garmr :

* does not support pip.  grab the source from git
* requires Requests > 0.6.2-dev, which can be installed by following the instructions here:
** http://docs.python-requests.org/en/latest/user/install/#get-the-code



## Usage

usage: garmr.py [-h] [-u TARGETS] [-m MODULES] [-f TARGET_FILES] [-p] [-d]

Check urls for compliance with Secure Coding Guidelines

optional arguments:
  -h, --help            show this help message and exit
  -u TARGETS, --url TARGETS
                        add a target to test
  -m MODULES, --module MODULES
                        load a test suite
  -f TARGET_FILES, --file TARGET_FILES
                        File with urls to test
  -p, --force-passive   Force passives to be run for each active test
  -d, --dns             Skip DNS resolution when registering a target.

## Tasks

* Implement a way to provide supply parameters and specify which http verb to use
* Implement sequences (i.e. a set of ActiveTests that once invoked, maintains a cookie jar)
* Implement a proper reporter; currently a range of data is accumulated, but never reported.
