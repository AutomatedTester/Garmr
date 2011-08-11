import httplib
import urllib2


    
def open_url(url):
    return urllib2.urlopen(url)

def clean_url(urls):
    import re
    mtch = re.search("https?://([^/]*?)(/.*)?", urls)
    split = []
    for matches in mtch.groups():
        split.append(matches)
    return split

def clean_header(response_headers):
    headers = {}
    for head in response_headers:
        lst = head.strip(" \r\n").split(":")
        headers[lst[0]] = lst[1].strip()
        return headers

def total_seconds(start, finish):
    td = finish - start
    return float((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)) / 10**6