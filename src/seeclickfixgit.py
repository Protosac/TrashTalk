## Manipulate the SeeClickFix API to find illegal dumping sites
## Then, post a clean-up message with a link to a community organizer website

__author__ = "miller.tim"
__date__ = "$Jan 26, 2017 6:06:40 PM$"

from watchareas import WatchArea
from cleanup import CleanUp

def main():    
    #Create an watch area for Oakaland
    watchAreaID = 35332 #Oakland Test Watch Area
    typeIssue = "Illegal Dumping"
    oaklandWatchArea = WatchArea(watchAreaID, typeIssue)
    
#    Call for dumping sites until at least one is found. 
#    Do Not Exceed 10 pages of calls
    maxPages = 10
    getDumpingSites(oaklandWatchArea,maxPages)
    
    #Find all reporters associated with the found dumping sites
    oaklandWatchArea.callForReporters()
    #Display the dumping sites associated with each reporter
    oaklandWatchArea.displayReporters()
#   Display the reporters associated with each dumping site
    oaklandWatchArea.displayIssues()

#   Chose a dumping Site
    for key in dumpingSites.keys():
        dumpingSite = dumpingSites[key]
        
#   Create and post a Clean Up for the chosen dumping site
    username = ""#Requires a username and password for test.seeclickfix.com
    password = ""
    cleanup = CleanUp(dumpingSite, username, password)
    cleanup.setData()
    response = cleanup.postCleanUp()
    print(response)
    print("end")

#Function allows the calls to cycle through more than one page
def getDumpingSites(watchArea, maxPages):
    i = 0 
    while watchArea.getNumIssues() <= 0 and i < maxPages:
        watchArea.callForIssues()
        i =+ 1  


main()


