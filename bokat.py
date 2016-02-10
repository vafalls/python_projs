#!/usr/bin/python

import mechanize
import re
import time
from mechanize._html import Link
from _mysql import NULL
BASE_URL = "http://www.bokat.se/protected/"

class dataStructure:
    def __init__(self):
        self.data1s = []
        self.data2s = []
    def setHeader(self, header):
        self.header = header
    def addDataPair(self, data1, data2s):
        self.data1s.append(data1)
        self.data2s.append(data2s)
    def getHeader(self):
        return self.header
    def getData1(self, nr):
        if(nr >= len(self.data1s)):
            return None
        return self.data1s[nr]
    def getData2(self, nr):
        if(nr >= len(self.data2s)):
            return None
        return self.data2s[nr]
    def getLastIndexNr(self):
        if(len(self.data1s) == len(self.data2s)):
            return len(self.data1s)-1
        else:
            raise ValueError('Couldn\'t return last index')
    def getIndexOfData1(self, data1):
        for i, v in enumerate(self.data1s):
            if(data1 == self.data1s[i]):
                return i
        return None
    def isData2Existing(self, data2):
        for i, v in enumerate(self.data2s):
            if(data2 == self.data2s[i]):
                return True
    def __str__(self):
        return self.data1s.__str__()

def getStartPageAndInputPassword():
    my_browser = mechanize.Browser(factory=mechanize.RobustFactory())
    my_browser.set_handle_robots(False)
    
    request = mechanize.Request("http://www.bokat.se/protected/groupInfo.jsp")
    response = mechanize.urlopen(request)
    forms = mechanize.ParseResponse(response, backwards_compat=False)
    loginForm = forms[0]
    loginForm["j_username"] = "WivIb"
    loginForm["j_password"] = "tjosan"
     
    try:
        response = mechanize.urlopen(loginForm.click())
    except HTTPError, e:
        sys.exit("post failed: %d: %s" % (e.code, e.msg))
    return response

def getStatusLinks(response):
    PAGE_NUMBER_REGEX = re.compile('.*eventInfo.*')
    list = []
    
    for index, val in enumerate(response.readlines()):
        
        if(re.match(PAGE_NUMBER_REGEX, str(val), flags=0)):
            substr = re.search('action=\'.*\'><td', val)
            if(substr):
                list.append(BASE_URL+substr.group(0)[8:-5])
            
    return list

def singleTimeInfo(lines):
    REGEX_1 = re.compile('.*method="POST" action=\'eventInfo\.jsp.*')
    REGEX_2 = re.compile('.*\/images\/.*\.png.*')
    REGEX_DATE = re.compile('.*Inbjudan skickades ut.*')
    pt = dataStructure()
    conclusion = []
    
    for index, val in enumerate(lines):
        
        if(re.match(REGEX_DATE, val, flags=0)):
            substr = re.search('20[0-9]{2}-[0-9]{2}-[0-9]{2}', val)
            if(substr):
                pt.setHeader(substr.group(0))
            
        if(re.match(REGEX_1, val, flags=0)) and (re.match(REGEX_2, lines[index+5], flags=0)):
            pt.addDataPair(lines[index+11][19:-7], lines[index+5][37:-13])
    
    return pt

def collectAttendanceInfo(listOfOccasions):
    playTimes = []
    for index, val in enumerate(listOfOccasions):
        response = mechanize.urlopen(val)
        playTimes.append(singleTimeInfo(response.readlines()))
    return playTimes
            
def findUniqueNames(playTimes):
    allNames = []
    for ind1, val1 in enumerate(playTimes):
        for i in range(0, val1.getLastIndexNr()):
            allNames.append(val1.getData1(i))
    allNames = set(allNames)
    return allNames

def createNewListStructure(allNames, playTimes):
    newCorrectList = []
    for i1, val1 in enumerate(allNames):
        personList = dataStructure()
        personList.setHeader(val1)
        for i2, val2 in enumerate(playTimes):
            for i3 in range(val2.getLastIndexNr()):
                if(val1 == val2.getData1(i3)):
                    personList.addDataPair(val2.getHeader(), val2.getData2(i3))
        newCorrectList.append(personList)
    return newCorrectList

def writeToFile(List):
    target = open("bokat.txt", 'w')
    for index, val in enumerate(newList):
        target.write("\n"+ val.getHeader()+"\n")
        for i in range(0, val.getLastIndexNr()):
            target.write(val.getData1(i)+";"+val.getData2(i)+"\n")
            
def writeToRealFile(newList, listOfDates):
    
    #write names to real file
    target = open("bokat_real.txt", 'w')
    for i, v in enumerate(newList):
        if(i==0):
            target.write(" ;")
        target.write(v.getHeader()+";")
        if(i==len(newList)-1):
            target.write("\n")
            
    #Write a new row to the ouputfile
    for i, v in enumerate(listOfDates):
        writeLineToRealFile(target, v, newList)

def writeLineToRealFile(target, date, newList):
    target.write(date+";")
    for i1, v1 in enumerate(newList):
        for i2 in range(0, v1.getLastIndexNr()+1, 1):
            if(v1.getData1(i2) == date):
                target.write(newList[i1].getData2(i2)+";")
                break    
            elif(i2 == v1.getLastIndexNr()):
                target.write("---;")
                break
    target.write("\n")
        
def getListOfDates(newList):
    listOfDates = []
    listOfDates2 = []
    for i, v in enumerate(newList):
        for i in range(0, v.getLastIndexNr()):
            listOfDates.append(v.getData1(i))
    listOfDates = set(listOfDates)
    for i, v in enumerate(listOfDates):
        listOfDates2.append(v)
    return listOfDates2

if __name__ == "__main__":    
    print "Fetching data from website"

    LINK_EXTRACTION_REGEX = re.compile('.*\'class\', \'item-link-container\'\)\, \(\'target\'\, \'_blank\'.*')
    PAGE_NUMBER_REGEX = re.compile('.*page=[2-9].*')
    
    response = getStartPageAndInputPassword()
    listOfOccasions = getStatusLinks(response)
    playTimes = collectAttendanceInfo(listOfOccasions)
    
    printer = open("bokat_before_conv.txt", 'w')
    for i, v in enumerate(playTimes):
        printer.write("\n"+v.getHeader()+"\n")
        for i2 in range(0, v.getLastIndexNr()+1, 1):
            printer.write(v.getData1(i2)+";"+v.getData2(i2)+"\n")
            
    allNames = findUniqueNames(playTimes)
    print sorted(allNames)
    newList = createNewListStructure(allNames, playTimes)
    
    writeToFile(newList)
    
    listOfDates = getListOfDates(newList)
    writeToRealFile(newList, listOfDates)
            
        
    print "Done!"
