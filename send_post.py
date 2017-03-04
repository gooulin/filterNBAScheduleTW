import urllib, urllib2
import json,httplib

def sendPost(baseUrl,key,dict,channelId):
    connection = httplib.HTTPSConnection(baseUrl)
    connection.connect()
    connection.request('POST', '/developers/channels/'+channelId+'/posts', json.dumps(dict), {
           "X-Parse-Developer-Key": key,
           "Content-Type": "application/json"
         })
    res = connection.getresponse()
    results = json.loads(res.read())
    print results
    print "status:"
    if (res.status == 200):
        print res.status
    return results
