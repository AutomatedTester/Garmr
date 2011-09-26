# Garmr

Garmr is a tool to inspect the responses from websites for basic security requirements.

Garmr includes a set of core test cases implemented in corechecks that are derived from
the Secure Coding Guidelines that can be found at [https://wiki.mozilla.org/WebAppSec/Secure_Coding_Guidelines]

## Installation

This version of Garmr :
* does not support pip.  Grab the source from git
* requires Requests > 0.6.2-dev, which can be installed by following the instructions here:
** http://docs.python-requests.org/en/latest/user/install/#get-the-code

## Usage

usage: garmr.py [-h] [-u TARGETS] [-m MODULES] [-f TARGET_FILES] [-p] [-d]

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
* Implement sequences (i.e. a series of ActiveTests that once invoked, maintains a cookie jar until the list of URLs is exhausted)
* Implement a proper detailed reporter; currently a range of data is accumulated, but never reported.
* Implement more checks