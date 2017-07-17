import sys
import httplib
import urllib
import urllib2

HOST =  ''
PORT = 80

def queryResult():
    params = urllib.urlencode({'md5s':'3a499d587a3cba0a7fb2edd8ed3261f7'})
    headers = {#'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X) AppleWebKit/601.1 (KHTML, like Gecko) CriOS/47.0.2526.70 Mobile/13C71 Safari/601.1.46',
               #'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               #'Referer' : '',
               'Content-Type' : 'application/x-www-form-urlencoded'
                }

    conn = httplib.HTTPConnection(HOST, PORT)
    conn.request('GET', 
                '', 
                params,
                headers)
                
    res = conn.getresponse()
    print res.read()
    
def method2():
    params = urllib.urlencode({'md5s':'3a499d587a3cba0a7fb2edd8ed3261f7'})
    f = urllib2.urlopen('', params)
    print f.read()

def main():
    #queryResult()
    method2()
    


if __name__ == '__main__':
    main()