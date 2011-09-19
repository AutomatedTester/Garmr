from datetime import datetime
from reporter import Reporter
from urlparse import urlparse
import logging
import requests
import socket
import traceback

def clean_headers(self, response_headers):
        headers = {}
        for head in response_headers:
            lst = head.strip(" \r\n").split(":")
            headers[lst[0]] = lst[1].strip()
        return headers

def get_url(url, status = True):
    r = requests.get(url, allow_redirects = False)
    if status:
        r.raise_for_status()
    return r

class PassiveTest():
    secure_only = False
    insecure_only = False
    
    def analyze(self, response, results):
        return None
    
    def result(self, state, message, data):
        return {'state' : state,  'message' : message, 'data' : data }
        

class ActiveTest(): 
    
    secure_only = False
    insecure_only = False
    run_passives = True
    description = "The base class for an Active Test."
    
    def __init__(self):
        if hasattr(self, "setup"):
            self.setup()
    
    def execute(self, url):
        try:            
            result = self.do_test(url)
        except Exception, e:
            tb = traceback.format_exc()
            result = (ActiveTest().result("Error", e, tb), None)
        
        return result
             
    def result(self, state, message, data):
        return { 'state' : state, 'message' : message, 'data' : data, 'passive' : {}}
    
class Scanner():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s')
    logger = logging.getLogger("Garmr-Scanner")
    logger.setLevel(logging.DEBUG)
    
    def __init__(self):
        self.resolve_target = True
        self.force_passives = False
        self._passive_tests_ = []
        self._active_tests_ = []
        self._targets_ = []
        self._protos_ = ["http", "https"]
        Scanner.logger.debug("Scanner initialized.")
        self.reporter = Reporter()
    
    def scan_target(self, target):
        self.reporter.write_target(target)
        Scanner.logger.info("[%s] scanning:" % target)
        url = urlparse(target)
        is_ssl = url.scheme == "https"
        results = {}
        self.reporter.start_actives()
        for test in self._active_tests_:
            if (test.secure_only and not is_ssl):
                Scanner.logger.info("\t[Skip] [%s] (reason: secure_only)" % test.__class__)
                result = ActiveTest().result("Skip", "This check is only applicable to SSL requests", None)
                result['start'] = datetime.now()
                result['end'] = result['start']
                result['duration'] = 0
                results[test.__class__]
                continue
            elif (test.insecure_only and is_ssl):
                Scanner.logger.info("\t[Skip] [%s] (reason: insecure_only)" % test.__class__)
                result = ActiveTest().result("Skip", "This check is only applicable to SSL requests", None)
                result['start'] = datetime.now()
                result['end'] = result['start']
                result['duration'] = 0
                results[test.__class__] = result
                continue
            start = datetime.now()
            o = test.execute(target)
            result = o[0]
            response = o[1]
            end = datetime.now()
            td = end - start
            result['start'] = start
            result['end'] = end
            result['duration'] = float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6
            Scanner.logger.info("\t[%s] %s %s" % (test.__class__, result['state'], result['message']))
            self.reporter.write_active(test.__class__, result)
            if (result['state'] == "Error"):
                Scanner.logger.error(result['data'])
            if response != None and test.run_passives:
                result['passive'] = {}
                self.reporter.start_passives()
                for passive in self._passive_tests_:
                    if passive.secure_only and not is_ssl:
                        Scanner.logger.debug("\t\t[%s] Skip Test invalid for http scheme" % passive.__class__)                        
                        passive_result = PassiveTest().result("Skip", "This check is only applicable to SSL requests.", None)
                        start = datetime.now()
                        passive_result['start'] = start
                        passive_result['end'] = start
                        passive_result["duration"] = 0
                    else:
                        start = datetime.now()
                        passive_result = passive.analyze(response)
                        end = datetime.now()
                        td = end - start
                        passive_result['start'] = start
                        passive_result['end'] = end
                        passive_result['duration'] = float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6
                        Scanner.logger.info("\t\t[%s] %s %s" % (passive.__class__, passive_result['state'], passive_result['message']))
                    result["passive"][passive.__class__] = passive_result
                    self.reporter.write_passive(passive.__class__,passive_result)
                self.reporter.end_passives()
            results[test.__class__] = result
        self.reporter.end_actives()
        return results
    
    def run_scan(self):
        results = {}
        self.reporter.start_report()
        self.reporter.start_targets()
        for target in self._targets_:
            try:
                results[target] = self.scan_target(target)
            except:
                Scanner.logger.error(traceback.format_exc())
        self.reporter.end_targets()
        file = open(self.output, "w")
        file.write(self.reporter.end_report())
        file.close()

    
    def register_target(self, url):
        u = urlparse(url)
        valid = u.netloc != "" and u.scheme in self._protos_
        reason = "%s%s" % ("[bad netloc]" if u.netloc == "" else "", "" if u.scheme in self._protos_ else "[bad scheme]")
        
        # todo - support ipv6 urls
        host = u.netloc.split(':')[0]
        if (self.resolve_target):
            try:
                socket.getaddrinfo(host, None)
            except socket.gaierror:
                valid = False
                reason = "%s[dns]" % reason
        else:
            valid = True
        if valid:
            self._targets_.append(url)
            Scanner.logger.debug("[target]: %s" % url)
            return
        Scanner.logger.error("%s is not a valid target (reason: %s)" % (url, reason))
    
    def register_test(self, test):
        if isinstance(test, ActiveTest):
            self._active_tests_.append(test)
            Scanner.logger.debug("Added %s to active tests." % test.__class__)
            return len(self._active_tests_)
        if isinstance(test, PassiveTest):
            self._passive_tests_.append(test)
            Scanner.logger.debug("Added %s to passive tests." % test.__class__)
            return len(self._passive_tests_)
        raise Exception('test is not a valid test type')
