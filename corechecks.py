from urlparse import urlparse
import requests
from scanner import ActiveTest, PassiveTest, Scanner, get_url


class HttpOnlyAttributePresent(PassiveTest):
    description = "Inspect the Set-Cookie: header and determine if the HttpOnly attribute is present."
    def analyze(self, response):
        cookieheader = "Set-Cookie"
        has_cookie = cookieheader in response.headers
        if has_cookie:
            if "httponly" in response.headers[cookieheader].lower():
                result = self.result("Pass", "HttpOnly is set", response.headers[cookieheader])
            else:
                result = self.result("Fail", "HttpOnly is not set", response.headers[cookieheader])            
        else:
            result = self.result("Skip", "No cookie is set by this response.", None)
        return result
    
class SecureAttributePresent(PassiveTest):
    description = "Inspect the Set-Cookie: header and determine if the Secure attribute is present."
    def analyze(self, response):
        url = urlparse(response.url)
        cookieheader = "Set-Cookie"
        has_cookie = cookieheader in response.headers
        if has_cookie:
            if "httponly" in response.headers[cookieheader].lower():
                if url.scheme == "https":
                    result = self.result("Pass", "HttpOnly is set", response.headers[cookieheader])
                else:
                    result = self.result("Fail", "HttpOnly should only be set for cookies sent over SSL.", response.headers[cookieheader]) 
            else:
                if url.scheme == "https":
                    result = self.result("Fail", "HttpOnly is not set", response.headers[cookieheader])
                else:
                    result = self.result("Pass", "The secure attribute is not set (expected for HTTP)", response.headers[cookieheader])            
        else:
            result = self.result("Skip", "No cookie is set by this response.", None)
        return result
        

class StrictTransportSecurityPresent(PassiveTest):
    secure_only = True
    description = "Check if the Strict-Transport-Security header is present in TLS requests."
    def analyze(self, response):
        stsheader = "Strict-Transport-Security"
        sts = stsheader in response.headers
        if sts == False:
            result = self.result("Fail", "Strict-Transport-Security header not found.", None)
        else:
            result = self.result("Pass", "Strict-Transport-Security header present.", response.headers[stsheader])
        return result

class XFrameOptionsPresent(PassiveTest):
    description = "Check if X-Frame-Options header is present."
    def analyze(self, response):
        xfoheader = "X-Frame-Options"
        xfo = xfoheader in response.headers
        if xfo == False:
            result = self.result("Fail", "X-Frame-Options header not found.", None)
        else:
            result = self.result("Pass", "X-Frame-Options header present.", response.headers[xfoheader])
        return result

class RobotsTest(ActiveTest):
    run_passives = True
    description = "Check for the presence of a robots.txt file. If save_contents is true, the contents will be saved."
    config = {"save_contents" : "False"}
    def do_test(self, url):
        u = urlparse(url)
        roboturl="%s://%s/robots.txt" % (u.scheme, u.netloc)
        response = requests.get(roboturl)
        if response.status_code == 200:
            result = self.result("Pass", "A robots.txt file is present on the server", 
                                 response.content if self.config["save_contents"].lower() == "true" else None)
        else:
            result = self.result("Fail", "No robots.txt file was found.", None)
        return (result, response);
    
class StsUpgradeCheck(ActiveTest):
    insecure_only = True
    run_passives = False
    description = "Inspect the Strict-Transport-Security redirect process according to http://tools.ietf.org/html/draft-hodges-strict-transport-sec"
    
    def do_test(self, url):
        stsheader = "Strict-Transport-Security"
        u = urlparse(url)
        if u.scheme == "http":
            correct_header = False
            bad_redirect = False
            response1 = get_url(url, False)
            invalid_header = stsheader in response1.headers
            is_redirect = response1.status_code == 301
            if is_redirect == True:
                redirect = response1.headers["location"]
                r = urlparse(redirect)
                if r.scheme == "https":
                    response2 = get_url(redirect, False)
                    correct_header = stsheader in response2.headers
                else:
                    bad_redirect = True
                    
            success = invalid_header == False and is_redirect == True and correct_header == True
            if success == True:
                message = "The STS upgrade occurs properly (no STS header on HTTP, a 301 redirect, and an STS header in the subsequent request."
            else:
                message = "%s%s%s%s" % (
                    "The initial HTTP response included an STS header (RFC violation)." if invalid_header else "",
                    "" if is_redirect else "The initial HTTP response should be a 301 redirect (RFC violation see ).",
                    "" if correct_header else "The followup to the 301 redirect must include the STS header.",
                    "The 301 location must use the https scheme." if bad_redirect else ""
                    )
            result = self.result("Pass" if success else "Fail", message, None)
            return (result, response1)
    
        
def configure(scanner):
    if isinstance(scanner, Scanner) == False:
        raise Exception("Cannot configure a non-scanner object!")
    scanner.register_check(StrictTransportSecurityPresent())
    scanner.register_check(XFrameOptionsPresent())
    scanner.register_check(RobotsTest())
    scanner.register_check(StsUpgradeCheck())
    scanner.register_check(HttpOnlyAttributePresent())
    scanner.register_check(SecureAttributePresent())