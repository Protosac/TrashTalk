#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "miller.tim"
__date__ = "$Feb 17, 2017 9:50:13 AM$"

import urllib2
import base64
import json


class CleanUp(object):

        def __init__(self, dumpingSite, username, password):
            self.dumpingSite = dumpingSite
            self.data = {}
            self.description = "Clean up dumping Site (id: %s) at: trashtalk.com"
            self.username = username
            self.password = password
            self.baseCallRequest = "https://test.seeclickfix.com/api/v2/issues"
            

        def setData(self):
            self.data={
                "lat":self.dumpingSite.getLat(),
                "lng":self.dumpingSite.getLng(),
                "address":self.dumpingSite.getAddress(),
                "request_type_id":"other",
                "answers":{
                    "summary":"Meet-Up to Clean-Up",
                    "description": self.description % self.dumpingSite.getIdent()
                }
            }
        
        def postCleanUp(self):
            api_request = urllib2.Request(self.baseCallRequest)#Currently Posts to the test site
            api_request.add_header("Content-type", "application/json")
            api_request.add_header("Authorization", "Basic "+base64.b64encode(self.username+":"+self.password))
            api_response = urllib2.urlopen(api_request, json.dumps(self.data))
            response_data = json.loads(api_response.read())
            return response_data
