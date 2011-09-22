from urlparse import urlparse
import requests
from scanner import ActiveTest, PassiveTest, Scanner, get_url


class AdminAvailable(ActiveTest):
    run_passives = True
    config = {"path" : "admin"}
    
    def do_test(self, url):
        u = urlparse(url)
        adminurl="%s://%s/%s" % (u.scheme, u.netloc, self.config["path"])
        response = requests.get(adminurl)
        if response.status_code == 200:
            result = self.result("Pass", "Django admin page is present at %s." % adminurl, response.content)
        else:
            result = self.result("Fail", "Default Django admin page is not present at %s" % adminurl, None)
        return (result, response);


def configure(scanner):
    if isinstance(scanner, Scanner) == False:
        raise Exception("Cannot configure a non-scanner object!")
    scanner.register_check(AdminAvailable())
    