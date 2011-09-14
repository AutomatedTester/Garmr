import argparse
from scanner import ActiveTest, PassiveTest, Scanner
import corechecks

def main():
    parser = argparse.ArgumentParser(description='Check urls for compliance with Secure Coding Guidelines')
    parser.add_argument("-u", "--url", action="append", dest="targets", help="add a target to test")
    parser.add_argument("-m", "--module", action="append", dest="modules", help="load a test suite module")
    #todo add option to influence DNS resolution before scanning.
    
    args = parser.parse_args()
        
    print "Garmr v0.02"
    scanner = Scanner()
    
    
    
    for target in args.targets:
        scanner.register_target(target)
    
    corechecks.configure(scanner)
    '''
    implement module loading here.
    modules are collections of classes that extend ActiveTest and PassiveTest
    the module must implement the configure(Scanner) function which will register the exposed functions to the scanner.
    '''
    scanner.run_scan()
    
    
if __name__ == "__main__":
    main()