#!/usr/bin/python

import mechanize
import re
import time
from mechanize._html import Link

def getFirstLinkSite(area):
    my_browser = mechanize.Browser(factory=mechanize.RobustFactory())
    my_browser.set_handle_robots(False)
    my_browser.open("http://www.hemnet.se/")

    my_browser.select_form(nr=0)
    my_browser["search[keywords]"] = area
    
    try:
        site = my_browser.submit()
    except HTTPError, e:
        sys.exit("post failed: %d: %s" % (e.code, e.msg))
        
    return my_browser


def getLinksFromWebsite(website, regex):
    my_browser = website
    list = [] 
    index_max = 0
    for index, val in enumerate(my_browser.links()):
        if(re.match(regex, str(val), flags=0)):
            list.append(val)
            index_max += 1
    #print index_max
    return list

def getNrOfTotalHits(my_browser):
    NUMBER_OF_HITS_REGEX = re.compile('.*Till salu.*result-list-segment-control__badge.*')
    lines = browser.reload()
    for counter, x in enumerate(lines):
        if(re.match(NUMBER_OF_HITS_REGEX, x, flags=0)):
            nr = re.search('>[0-9]*<', x)
            if(nr):
                return nr.group(0)[1:-1]
            else:
                print "ERROR"

def getAgentAndCompanyNames(itemLinks, my_browser):
    listOfAgents = []
    listOfCompanies = []
    for counter, x in enumerate(itemLinks):
        site = browser.follow_link(x)
        lines = site.readlines()
        for p, q in enumerate(lines):
            if("class=\"broker\"" in q):
                listOfAgents.append(lines[p+2].strip()[3:-4])
                company = lines[p+8]
                company = company.strip()
                http = re.search('http', company)
                if(http):
                    listOfCompanies.append(company[9:-1])
                    print "found http:",company[9:-1]
                else:
                    listOfCompanies.append(company)
                    print "didnt find:",company
        browser.back(1)
    return (listOfAgents, listOfCompanies)

def getClickableLinks(itemLinks):
    REGEX_BEGINNING = re.compile('url=\'/bostad.*[0-9]{4,}\'. te')
    REGEX_END = re.compile("")
    clickableList = []
    for a, i in enumerate(itemLinks):
        nr = re.search(REGEX_BEGINNING, str(i))
        if(nr):
            clickableList.append("http://hemnet.se/"+nr.group(0)[6:-5])
    return clickableList

if __name__ == "__main__":    
    print "Fetching data from website"

    LINK_EXTRACTION_REGEX = re.compile('.*\'class\', \'item-link-container\'\)\, \(\'target\'\, \'_blank\'.*')
    PAGE_NUMBER_REGEX = re.compile('.*page=[2-9].*')
    
    browser = getFirstLinkSite("Bromma")
    
    pageLinks = getLinksFromWebsite(browser, PAGE_NUMBER_REGEX)
    itemLinks = getLinksFromWebsite(browser, LINK_EXTRACTION_REGEX)
    
    print "Number of total objects is "+getNrOfTotalHits(browser)
    
    #Get remaining links from different subpages
    #They are divided between multiple sites with max 50 results in each
    for i in range(1, len(pageLinks), 1):
        browser.follow_link(pageLinks[i])
        itemLinks += getLinksFromWebsite(browser, LINK_EXTRACTION_REGEX)
        browser.back(1)
        
    clickableList = getClickableLinks(itemLinks)
    agentList, companyList = getAgentAndCompanyNames(itemLinks, browser)
    
    counter = 0
    for i in enumerate(itemLinks):
        counter += 1
    
    target = open("meck.txt", 'w')
    
#     print "itemLinks is ", counter
#     print "clickableList is ", len(clickableList)
#     print "agentList is ", len(agentList)
    
    for a, b in enumerate(agentList):
        target.write(str(agentList[a])+";"+str(companyList[a])+";"+str(clickableList[a])+"\n")
#         print("agent='%s' link='%s'" % (str(agentList[a]), str(clickableList[a])))
    
    print "Done!"
