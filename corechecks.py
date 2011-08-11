#!/usr/bin/python

from results import GarmrResult
import gadgets
import httplib
from datetime import datetime

class CoreChecks:
    def __init__(self):
        self.version = 1

    def xframe_checks2(self, garmr, url):
        result = GarmrResult("x-frame-checks")
        result.append("name", self.xframe_checks.__name__)
        try:
            response = gadgets.open_url(url) 
            response_headers = response.headers.headers
            headers = gadgets.clean_header(response_headers)
            
            result.info("Checking x-frame-options")
            try:
                assert headers["x-frame-options"] == "DENY" or \
                    headers["x-frame-options"] == "SAMEORIGIN", \
                    "x-frame-options were: %s" % headers["x-frame-options"]
                result.succeed("x-frame-options were correct")    
            except KeyError:
                message = "x-frame-options were not found in headers"
                result.fail(message)        
        except AssertionError as e:
            result.incomplete(str(e))
            
        result.append("time_taken", result.duration())
        result.debug("Time Taken: %s:" % result.duration)
        return result

    def xframe_checks(self, garmr, url):
        result = {}
        result["name"] = self.xframe_checks.__name__
        start = datetime.now()
        try:
            response = gadgets.open_url(url) 
            response_headers = response.headers.headers
            headers = gadgets.clean_header(response_headers)
            garmr.logger().info("Checking x-frame-options")
            try:
                assert headers["x-frame-options"] == "DENY" or \
            	    headers["x-frame-options"] == "SAMEORIGIN", \
                	"x-frame-options were: %s" % headers["x-frame-options"]

                garmr.logger().info("x-frame-options were correct")
            except KeyError:
                message = "x-frame-options were not found in headers"
                result["failed"] = True
                result["message"] = message
                garmr.logger().critical(message)
        except AssertionError as e:
            garmr.logger().error(str(e))
            result["errors"] = True
            result["message"] = str(e)
        finish = datetime.now()
        result["time_taken"] = gadgets.total_seconds(start, finish)
        garmr.logger().debug("Time Taken: %s:" % result["time_taken"])
        return result
        
    def trace_checks(self, garmr, url):
        result = {}
        result["name"] = self.trace_checks.__name__
        start = datetime.now()
        try:
            garmr.logger().info("Checking TRACE is not valid")
            http_urls = gadgets.clean_url(url) 
            request = httplib.HTTPConnection(http_urls[0])
            if len(http_urls) > 1:
                request.request("TRACE", http_urls[1])
            else:
                request.request("TRACE", "/")
                
            request.getresponse()
            raise Exception("TRACE is a valid HTTP call")
        except httplib.BadStatusLine, e:
            garmr.logger().info("TRACE is not valid")
        except Exception, e:
            garmr.logger().error(str(e))
            result["errors"] = True
            result["message"] = str(e)
        finish = datetime.now()
        result["time_taken"] = gadgets.total_seconds(start, finish)
        garmr.logger().debug("Time Taken: %s:" % result["time_taken"])
        return result


    def redirect_checks(self, garmr, url):
        result = {}
        result["name"] = self.redirect_checks.__name__
        start = datetime.now()
        response = gadgets.open_url(url)
        try:
            garmr.logger().info("Checking for HTTPS")
            assert "https://" in response.geturl(), "Have not been redirected to HTTPS"
            garmr.logger().info("Redirected to HTTPS version of site")
        except AssertionError, e:
            garmr.logger().error(str(e))
            result["errors"] = True
            result["message"] = str(e)
        finish = datetime.now()
        result["time_taken"] = gadgets.total_seconds(start, finish)
        garmr.logger().debug("Time Taken: %s:" % result["time_taken"])
        return result
