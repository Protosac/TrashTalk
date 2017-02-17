#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "miller.tim"
__date__ = "$Feb 17, 2017 9:42:25 AM$"

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
        
            
