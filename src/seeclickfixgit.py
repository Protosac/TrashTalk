# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

##
__author__ = "miller.tim"
__date__ = "$Jan 26, 2017 6:06:40 PM$"

import urllib
import json


##Function driven object        
#Monitor A Watch area. Give it a hash table for dumping sites and another for reporters/users
        ##Functions include:    1) Checking for dumping sites using the API and adding new ones to the sites hashtable
        ##                      2) Checking for Reporters using the issues hash table and adding new ones to its hashtable
class WatchArea(object):        

        def __init__(self, area, typeIssue):
            self.baseCall = "https://test.seeclickfix.com/api/v2/issues?page=%d&watcher_token=%d"
            self.baseCallReporter = "https://test.seeclickfix.com/api/v2/users?lat=%f&lng=%f"
            self.area = area
            self.allIssues = dict()
            self.allReporters = dict()
            self.page = 1
            self.typeIssue = typeIssue
                
        #Add new dumping sites to hashtable
        def callForIssues(self):
            callWatchArea = urllib.urlopen(self.baseCall % (self.page, self.area))
            readWatchArea = callWatchArea.read()
            watchArea = json.loads(readWatchArea)
            issues = watchArea['issues']
            for issue in issues:
                summary = issue['summary']
                if self.typeIssue in summary:
                    ident = issue['id']
                    status = issue['status']
                    lat = issue['lat']
                    lng = issue['lng']
                    dSite = DumpingSite(ident, status, summary, lat, lng)
                    self.allIssues[ident] = dSite
            self.page = watchArea['metadata']['pagination']['next_page']

        #Add new reporters to hashtable
        def callForReporters(self):
            #Cycle through all of the issues
            for key in self.allIssues.keys():
                #Call the API and get the reporters for each issue. Calls are based on the GPS Coordinates of the dumping site
                issue = self.allIssues[key]
                lat = issue.getLat()
                lng = issue.getLng()
                ident = issue.getIdent()
                callReporters = urllib.urlopen(self.baseCallReporter % (lat, lng))
                readReporters = callReporters.read()
                reporters = json.loads(readReporters)
                #Cycle through each reporter
                reporter = reporters['users']
                for each in reporter:                                
                    eachID = each['id']
                    eachName = each['name']
                    #Add its ID to the dumping site's keychain of reporters
                    issue.addReporter(eachID)
                    #Check whether the key for the reporter is already in the list of keys in the Reporter Hashtable
                    if eachID in self.allReporters:
                        #If the reporter is already in the Hashtable, simply add the dumping site ID to its keychain of dumping sites
                        changeReporter = self.allReporters[eachID]
                        changeReporter.addDumpingSite(ident)                                       
                    #Else, create a new reporter with the site ID on its chain, add it to the allReporters Hashtable 
                    else:
                        newReporter = Reporters(eachID, eachName, ident)
                        self.allReporters[eachID] = newReporter
                     
        def getIssues(self):
                return (self.allIssues)

        def getReporters(self):
                return (self.allReporters)
        
        def displayIssues(self):
            for key in self.allIssues.keys():
                singleSite = self.allIssues[key]
                #print ("Identity: %s, Summary: %s, Lat: %s, Long: %s" % (key, singleSite.getSummary(), singleSite.getLat(), singleSite.getLng()))
                print ("Summary: %s, Status: %s, A Reporter: %s" % (singleSite.getSummary(), singleSite.getStatus(), singleSite.getOneReporter()))        

        def displayReporters(self):
            for key in self.allReporters.keys():
                singleReporter = self.allReporters[key]
                print("Name: %s, A Dumping Site: %s" % (singleReporter.getName(), singleReporter.getOneDumpingSite()))

                        
##Structure Driven Objects                        
##Identify Each Dumping Site and Give it keys(ids) to all of its reporters
##Functions Include: 
class DumpingSite(object):
        
        def __init__(self, ident, summary, status, lat, lng):
            self.ident = ident
            self.summary = summary
            self.status = status
            self.lat = lat
            self.lng = lng                
            self.reporters = [] #say 'reporters' not 'users' #It's only the id, not the whole object

        ##Modification Functions
        def addReporter(self, newReporter):
            self.reporters.append(newReporter)
        
        def closeSite(self):
            self.status = "closed"
            
        def acknowledgeSite(self):
            self.status = "acknowledged"
            
        def openSite(self):
            self.status = "open"
            
        ##Retrieval Functions
        def getIdent(self):
            return(self.ident)

        def getSummary(self):
            return(self.summary)
        
        def getStatus(self):
            return (self.status)

        def getLat(self):
            return(self.lat)

        def getLng(self):
            return(self.lng)

        def getReporters(self):
            return(self.reporters)

        def getOneReporter(self):
            return(self.reporters[0])
                
##Identify Each User and give it keys to each dumping Site associated with it 
class Reporters(object):
        #Reporters are only created from dumpingSites. Consequently, they always begin with at least one
        def __init__(self, ident, name, dumpingSite):
                self.ident = ident
                self.name = name
                self.dumpingSites = [dumpingSite] #Only the site ID
                                
        def addDumpingSite(self, dumpingSite):
                self.dumpingSites.append(dumpingSite)

        def getIdent(self):
                return (self.ident)

        def getName(self):
                return (self.name)

        def getDumpingSites(self):
                return(self.dumpingSites)

        def getOneDumpingSite(self):
                return(self.dumpingSites[0])

        
###Under Construction
class MeetUp(object):

    def __init__(self, dumpSite, inviteList):
        self.host = {}
        self.guestList = {}
        self.inviteList = inviteList
        self.dumpSite = dumpSite
                
        
def main():
    localWatchArea = 181 #Oakland Watch Area
    typeIssue = ""
    oaklandWatchArea = WatchArea(localWatchArea, typeIssue)
    oaklandWatchArea.callForIssues()
    oaklandWatchArea.callForReporters()
#    oaklandWatchArea.displayIssues()
#    oaklandWatchArea.displayReporters()
#    reporters = oaklandWatchArea.getReporters()
#    for key in reporters.keys():
#        reporter = reporters[key]
#        print(reporter.getDumpingSites())
    issues = oaklandWatchArea.getIssues()
    for key in issues.keys():
        issue = issues[key]
        print(issue.getReporters())
    print("end")

main()        


