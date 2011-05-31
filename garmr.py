#!/usr/bin/python

import httplib
import urllib2
from optparse import OptionParser
import logging


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger("Garmr")
logger.setLevel(logging.DEBUG)

class Reporter(object):
    """
        This class formats and writes a xUnit style report on the results from
        the basic tests
    """
    

    suite_xml="""
        <?xml version="1.0" encoding="utf-8"?>
        <testsuite name="Garmr" errors="{error}" failures="{failure}" 
            skips="{skips}" tests="{numtests}" time="{timetaken}">
            {testresults}
        </testsuite>
    """

    def __init__(self, results=None):
        """
            Initializes the reporter class
            Args:
                results - optional parameter to take the results. If results 
                        are not passed in here they need to be passed in
                        write_results method or an exception will be raised
        """
        logging.debug("Reporter class initialized")
        self.results = results

    def write_results(self, file_name='garmr-results.xml', results=None):
        """
            This writes the xml to disk.
            Args:
                file_name - optional parameter of the name of the file to create
                results - optional parameter of with the test results. If this is
                        empty and nothing was passed in during object initialization
                        an error will be raised. 
                        Note: if you pass in above and here the latest results will 
                        be used

        """
        if self.results is None and results is None:
            logging.exception("No test results have been passed Reporter")
            raise Exception("No results have been passed. Please pass in a result")

    def _format_results(self):
        testcase = """<testcase classname="" name="{testname}" time="{timetaken}">"""
        formatted_results = ""
        results = {"time_taken":0,
                    "errors" : 0,
                    "failed" : 0,
                    "skips" : 0}
        
        for res in self.results:
            formatted_results +=  testcase.format(
                    testname = res["name"],timetaken=res["time_taken"])
            if res.has_key("errors"):
                results["errors"] += 1
            if res.has_key("failed"):
                results["failed"] += 1
            if res.has_key("skips"):
                results["skips"] += 1
            results["time_taken"] += res["time_taken"]
        
        results["testcase"] = formatted_results
        return results

class Garmr(object):

    def __init__(self, urls):
        self.urls = urls

    def xframe_checks(self):
        try:
            response = urllib2.urlopen(self.urls) 
            response_headers = response.headers.headers
            headers = self._clean_header(response_headers)
            logger.info("Checking x-frame-options")
            try:
                assert headers["x-frame-options"] == "DENY" or \
            	    headers["x-frame-options"] == "SAMEORIGIN", \
                	"x-frame-options were: %s" % headers["x-frame-options"]

                logger.info("x-frame-options were correct")
            except KeyError:
                logger.error("x-frame-options were not found in headers")
        except AssertionError, e:
            logger.error(str(e))
        
    def trace_checks(self):
    	try:
            logger.info("Checking TRACE is not valid")
            http_urls = self._clean_url(self.urls) 
            request = httplib.HTTPConnection(http_urls[0])
            if len(http_urls) > 1:
                request.request("TRACE", http_urls[1])
            else:
                request.request("TRACE", "/")
                
            request.getresponse()
            raise Exception("TRACE is a valid HTTP call")
        except httplib.BadStatusLine, e:
            logger.error("TRACE is not valid")
        except Exception, e:
            logger.error(str(e))


    def redirect_checks(self):
        response = urllib2.urlopen(self.urls)
        try:
            logger.info("Checking for HTTPS")
            assert "https://" in response.geturl(), "Have not been redirected to HTTPS"
            logger.info("Redirected to HTTPS version of site")
        except AssertionError, e:
            logger.error(str(e))

        
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
    if not options:
        parser.error("Please supply an argument")

    garmr = Garmr(options.aut)
    garmr.trace_checks()
    garmr.xframe_checks()
    garmr.redirect_checks()


if __name__ == "__main__":
    main()
