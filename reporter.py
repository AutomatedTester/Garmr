

class Reporter():
    reporters = {}
    def start_report(self):
        return None
    
    def start_targets(self):
        return None
    
    def write_target(self, target):
        return None
    
    def start_actives(self):
        return None
    
    def write_active(self, test):
        return None
    
    def start_passives(self):
        return None
    
    def write_passive(self, target):
        return None
    
    def end_passives(self):
        return None
    
    def end_actives(self):
        return None
    
    def end_targets(self):
        return None
   
    def end_report(self):
        return "This reporter is unimplemented!"
        
class DetailReporter(Reporter):
    # TODO Implement detailed reporter
    def end_report(self):
        return "This reporter should emit an XML report that includes all of the the details for each test, including captured data"
    
Reporter.reporters['detail'] = DetailReporter()
        
class AntXmlReporter(Reporter):
    
    def __init__(self):
        self.report = ""
        self.errtypes = { 'Error' : "error", 'Fail' : "failure", 'Skip' : "skipped"}

    def start_report(self):
        self.report = '<?xml version="1.0" encoding="utf-8"?>\n'
        
        return None
    
    def start_targets(self):
        self.report += "<testsuites>\n"
        return None
    
    def write_target(self, target):
        self.states = {}
        self.states["Skip"] = 0
        self.states["Error"] = 0
        self.states["Pass"] = 0
        self.states["Fail"] = 0
        self.checks = 0
        self.current_target = target
        self.lines = ""
        return None
    
    def start_actives(self):
        return None
    
    def write_active(self, test, result):
        self.states[result["state"]] += 1
        self.checks += 1
        module, check = ("%s" % test ).split('.')
        self.lines += '\t\t<testcase classname="%s" name="%s" time="%s"' % (module, check, result["duration"])
        if result["state"] == "Pass":
            self.lines += " />\n"
        else:            
            self.lines += '>\n\t\t\t<{errtype}>{message}</{errtype}>\n\t\t</testcase>\n'.format(errtype=self.errtypes[result["state"]], message=result["message"]) 
        return None
    
    def start_passives(self):
        return None
    
    def write_passive(self, test, result):
        self.states[result["state"]] += 1
        self.checks += 1
        module, check = ("%s" % test ).split('.')
        self.lines += '\t\t<testcase classname="%s" name="%s" time="%s"' % (module, check, result["duration"])
        if result["state"] == "Pass":
            self.lines += " />\n"
        else:            
            self.lines += '>\n\t\t\t<{errtype}>{message}</{errtype}>\n\t\t</testcase>\n'.format(errtype=self.errtypes[result["state"]], message=result["message"])
        return None
    
    def end_passives(self):
        return None
    
    def end_actives(self):
        self.report+= '\t<testsuite name="{target}" errors="{errors}" failures="{failures}" skips="{skips}" tests="{checks}" time="{duration}">\n{lines}\t</testsuite>\n'.format(
            target = self.current_target, errors=self.states["Error"], failures = self.states["Fail"],
                                          skips = self.states["Skip"], checks = self.checks, duration=100, lines=self.lines)
        return None
    
    def end_targets(self):
        self.report += "</testsuites>\n"
        return None
   
    def end_report(self):
        return self.report
    
Reporter.reporters['xml'] = AntXmlReporter()
    