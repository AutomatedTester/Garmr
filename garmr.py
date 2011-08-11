#!/usr/bin/python

import httplib
import urllib2
from optparse import OptionParser
import logging
from datetime import datetime
from corechecks import CoreChecks
from results import GarmrResult


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger("Garmr")
logger.setLevel(logging.DEBUG)

class Reporter(object):
    """
        This class formats and writes a xUnit style report on the results from
        the basic tests
    """
    

    suite_xml="""<?xml version="1.0" encoding="utf-8"?>
        <testsuite name="Garmr" errors="{error}" failures="{failure}" 
            skips="{skips}" tests="{numtests}" time="{timetaken}">
            {testresults}
        </testsuite>"""

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

        if results is not None:
            self.results = results

        formatted = self._format_results()
        suite_results = self.suite_xml.format(error=formatted["errors"], 
                                        failure=formatted["failed"],
                                        skips=formatted["skips"],
                                        numtests=formatted["tests"], 
                                        timetaken=formatted["time_taken"], 
                                        testresults=formatted["testcase"])
        file_results = open(file_name, "w")
        file_results.write(suite_results)
        file_results.close()


    def _format_results(self):
        testcase = """<testcase classname="" name="{testname}" time="{timetaken}" """
        errs = '><{errtype}>{message}</{errtype}></testcase>'
        formatted_results = ""
        results = {"time_taken":0,
                    "errors" : 0,
                    "failed" : 0,
                    "skips" : 0,
                    "tests" : 0}
        
        for res in self.results:
            try:
                results["tests"] += 1
                formatted_results +=  testcase.format(
                        testname = res["name"],timetaken=res["time_taken"])
                if res.has_key("errors"):
                    results["errors"] += 1
                    formatted_results +=  errs.format(errtype="error", message=res["message"])
                elif res.has_key("failed"):
                    results["failed"] += 1
                    formatted_results += errs.format(errtype="failure", message=res["message"])
                elif res.has_key("skips"):
                    results["skips"] += 1
                    formatted_results += errs.format(errtype="skipped", message=res["message"])
                else:
                    formatted_results += "/>"
                results["time_taken"] += res["time_taken"]
            except:
                logger.error("bad type, fix the reporter!")
        
        results["testcase"] = formatted_results
        return results


class Garmr(object):

    def __init__(self, urls, logger):
        self.urls = urls
        self._logger = logger
    
    def run_tests(self, tests, results):
        results.append(tests.trace_checks(self, self.urls))
        results.append(tests.xframe_checks(self, self.urls))
        results.append(tests.redirect_checks(self, self.urls))
        results.append(tests.xframe_checks2(self, self.urls))
        
    
    
    
    def logger(self):
        return self._logger

def main():
    usage = "Usage: %prog [option] arg"
    parser = OptionParser(usage=usage, version="%prog 0.2")
    parser.add_option("-u", "--url", action="store", type="string",
                    dest="aut", help="Url to be tested")
    parser.add_option("-f", "--file", action="store", type="string",
                    dest="file_name", 
                    help="File name with URLS to test, Currently not available")
    parser.add_option("-x", "--xunit", action="store", type="string",
                    dest="xunit", default='garmr-results.xml',
                    help="Name of file that you wish to write to")
    
    GarmrResult.logger = logger
    (options, args) = parser.parse_args()
    if options.aut is None and options.file_name is None:
        parser.error("Please supply an argument")

    test_results = []

    test_suite = CoreChecks()
    garmr = Garmr(options.aut, logger)
    garmr.run_tests(test_suite, test_results)
    reporter = Reporter(test_results)
    reporter.write_results(file_name=options.xunit)

if __name__ == "__main__":
    main()
