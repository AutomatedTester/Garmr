#!/usr/bin/python

import httplib
import urllib2
from optparse import OptionParser

class Reporter(object):
    pass
        

class Garmr(object):

    def __init__(self, urls):
        self.urls = urls

    def xframe_checks(self):
        try:
            response = urllib2.urlopen(self.urls) 
            response_headers = response.headers.headers
            headers = self._clean_header(response_headers)
            print "Checking x-frame-options"
            try:
                assert headers["x-frame-options"] == "DENY" or \
            	    headers["x-frame-options"] == "SAMEORIGIN", \
                	"x-frame-options were: %s" % headers["x-frame-options"]

                print "x-frame-options were correct"
            except KeyError:
                print "x-frame-options were not found in headers"
        except AssertionError, e:
            print str(e)
        finally:
            print "\n"
        
    def trace_checks(self):
    	try:
            print "Checking TRACE is not valid"
            http_urls = self._clean_url(self.urls) 
            request = httplib.HTTPConnection(http_urls[0])
            if len(http_urls) > 1:
                request.request("TRACE", http_urls[1])
            else:
                request.request("TRACE", "/")
                
            request.getresponse()
            raise Exception("TRACE is a valid HTTP call")
        except httplib.BadStatusLine, e:
            print "TRACE is not valid"
        except Exception, e:
            print str(e)
        finally:
            print "\n"


    def redirect_checks(self):
        response = urllib2.urlopen(self.urls)
        try:
            print "Checking for HTTPS"
            assert "https://" in response.geturl(), "Have not been redirected to HTTPS"
            print "Redirected to HTTPS version of site"
        except AssertionError, e:
            print str(e)
        finally:
            print "\n"

        
    def _clean_header(self, response_headers):
    	headers = {}
    	for head in response_headers:
        	lst = head.strip(" \r\n").split(":")
	        headers[lst[0]] = lst[1].strip()
    	return headers

    def _clean_url(self, urls):
        import re
        mtch = re.search("https?://([^/]*?)(/.*)?", urls)
        split = []
        for matches in mtch.groups():
            split.append(matches)
        return split

def main():
    usage = "Usage: %prog [option] arg"
    parser = OptionParser(usage=usage, version="%prog 0.1")
    parser.add_option("-u", "--url", action="store", type="string",
                    dest="aut", help="Url to be tested")
    parser.add_option("-f", "--file", action="store", type="string",
                    dest="file_name", 
                    help="File name with URLS to test, Currently not available")

    (options, args) = parser.parse_args()
    
    garmr = Garmr(options.aut)
    garmr.trace_checks()
    garmr.xframe_checks()
    garmr.redirect_checks()


if __name__ == "__main__":
    
    

    main()
