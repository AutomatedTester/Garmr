import argparse
from scanner import ActiveTest, PassiveTest, Scanner
import corechecks
from reporter import Reporter
import sys
import traceback

def main():
    parser = argparse.ArgumentParser(description='Check urls for compliance with Secure Coding Guidelines')
    parser.add_argument("-u", "--url", action="append", dest="targets", help="add a target to test")
    parser.add_argument("-m", "--module", action="append", dest="modules", help="load a test suite")
    parser.add_argument("-f", "--file", action="append", dest="target_files", help="File with urls to test")
    parser.add_argument("-p", "--force-passive", action="store_true", default=False, dest="force_passives", help ="Force passives to be run for each active test")
    parser.add_argument("-d", "--dns", action="store_false", default=True, dest="resolve_target", help ="Skip DNS resolution when registering a target.")
    parser.add_argument("-r", "--report", action="store", default="reporter.AntXmlReporter", dest="report",help="Load a reporter, format module.class, e.g. reporter.AntXmlReporter")
    parser.add_argument("-o", "--output", action="store", default="garmr-results.xml", dest="output", help="Default output is garmr-results.xml")
    #todo add option to influence DNS resolution before scanning.
    
    args = parser.parse_args()
    scanner = Scanner()
    
    scanner.force_passives = args.force_passives
    scanner.resolve_target = args.resolve_target
    scanner.output = args.output
     
    
    if args.targets != None:
        for target in args.targets:
            scanner.register_target(target)
        
    if args.target_files != None:
        for targets in args.target_files:
            try:
                f = open(targets, "r")
                for target in f:
                    t = target.strip()
                    if len(t) > 0:
                        scanner.register_target(t)
            except:
                Scanner.logger.error("Unable to process the target list in: %s", targets)
    
    corechecks.configure(scanner)
    
    if args.modules != None:
        for module in args.modules:
            try:
                __import__(module)
                m = sys.modules[module]
                m.configure(scanner)
            except:
                Scanner.logger.fatal("Unable to load the requested module [%s]", module)
                quit()
        
    try:
        reporter = args.report.split('.')
        if len(reporter) == 1:
            scanner.reporter = Reporter.reporters[reporter[0]]
        else:
            scanner.reporter = getattr(sys.modules[reporter[0]], reporter[1])()
            Scanner.logger.info("Writing report to [%s] using [%s]" % (args.output, args.report))
        if isinstance(scanner.reporter, Reporter) == False:
            raise Exception("Cannot configure a non-scanner object!")
    except Exception, e:
        Scanner.logger.fatal("Unable to use the reporter class [%s]: %s", args.report, e)
        quit()
    
    scanner.run_scan()
    
    
if __name__ == "__main__":
    main()