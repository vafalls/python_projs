#!/usr/bin/python

import mechanize
import re

numeroUno = ["NumeroUno"]
theAteam = ["The-A-Team"]
radioForce = ["RadioForce"]

def getVappGateway():
    mech = mechanize.Browser()
    site = mech.open("https://atvpgspp16.athtem.eei.ericsson.se/Reports/vapp_report")
    print mech.title()
    
    fullList = site.readlines()
    for index, val in enumerate(fullList):
        if("NumeroUno" in val):
            numeroUno.append(fullList[index+3].strip()[4:len(fullList[index+3].strip())-5])
        if("The-A-Team" in val):
            theAteam.append(fullList[index+3].strip()[4:len(fullList[index+3].strip())-5])
        if("RadioForce" in val):
            radioForce.append(fullList[index+3].strip()[4:len(fullList[index+3].strip())-5])
    for x in range(0, 3):
        print (numeroUno[x], theAteam[x], radioForce[x])
if __name__ == "__main__":
    print "Fetching data from website"
    getVappGateway()
    print "Done!"
