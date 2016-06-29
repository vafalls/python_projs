#!/usr/bin/python

import tkSimpleDialog
import tkMessageBox
import mechanize
import re
from mechanize._html import Link
import Tkinter
import time
import sys


def getfirstlinksite(area):
    my_browser = mechanize.Browser(factory=mechanize.RobustFactory())
    my_browser.set_handle_robots(False)
    my_browser.open("http://www.hemnet.se/")

    my_browser.select_form(nr=1)

    my_browser["keywords"] = area

    try:
        my_browser.submit()
    except HTTPError, e:
        sys.exit("post failed: %d: %s" % (e.code, e.msg))
        
    return my_browser


def getlinksfromwebsite(website, regex):
    my_browser = website
    mylist = []
    index_max = 0
    for index, val in enumerate(my_browser.links()):
        if re.match(regex, str(val), flags=0):
            mylist.append(val)
            index_max += 1
    return mylist


def getnroftotalhits():
    number_of_hits_regex = re.compile('.*Till salu.*result-list-segment-control__badge.*')
    lines = browser.reload()
    for w, x in enumerate(lines):
        if re.match(number_of_hits_regex, x, flags=0):
            nr = re.search('>[0-9]*<', x)
            if nr:
                return nr.group(0)[1:-1]
            else:
                print "ERROR"


def getagentandcompanynames(itemlinks):
    print "Fetching agent and company names"
    listofagents = []
    listofcompanies = []
    for w, x in enumerate(itemlinks):
        site = browser.follow_link(x)
        lines = site.readlines()
        for p, q in enumerate(lines):
            if "class=\"broker\"" in q:
                listofagents.append(lines[p+2].strip()[3:-4])
                company = lines[p+7]
                company = company.strip()
                http = re.search('^.*<i', company)
                if http:
                    listofcompanies.append(http.group(0)[0:-3])
                else:
                    listofcompanies.append(company)
        sys.stdout.write(". ")
        if (w+1) % 30 == 0:
            sys.stdout.write("\n")
        browser.back(1)
    print "\nCompleted!"
    return listofagents, listofcompanies


def getclickablelinks(itemlinks):
    print "Fetching links"
    regex_beginning = re.compile('url=\'/bostad.*[0-9]{4,}\'. te')
    clicklist = []
    for g, h in enumerate(itemlinks):
        nr = re.search(regex_beginning, str(h))
        if nr:
            clicklist.append("http://hemnet.se/"+nr.group(0)[6:-5])
    print "Completed!"
    return clicklist


def tyuioprules():
    print "    ______________"
    print "   /              \\"
    print "   | TYUIOP RULES |"
    print "   \\______________/"
    time.sleep(2)


def downloadsomething(something):
    print "\nDownloading "+something+"!"
    for num in range(1, 30):
        print ".",
        time.sleep(0.075)
    print "\nCompleted!"


if __name__ == "__main__":
    LINK_EXTRACTION_REGEX = re.compile('.*\'class\', \'item-link-container\'\), \(\'target\', \'_blank\'.*')
    PAGE_NUMBER_REGEX = re.compile('.*page=[2-9].*')

    # Inputdialog
    root = Tkinter.Tk()
    root.wm_deiconify()
    root.withdraw()
    browser = getfirstlinksite(
            tkSimpleDialog.askstring("Meck", "Search keywords: (max 3 and comma separated)"))

    # This can't be free forever ;)
    if time.localtime()[0] > 2016:
        tkMessageBox.showerror("ERROR", "Can't run application")
        exit()

    # Show funny text
    tyuioprules()
    downloadsomething("Virus")
    downloadsomething("Gay Porn")

    print "Fetching data from website"
    pageLinks = getlinksfromwebsite(browser, PAGE_NUMBER_REGEX)
    itemLinks = getlinksfromwebsite(browser, LINK_EXTRACTION_REGEX)
    
    print "Number of total objects is " + getnroftotalhits()
    
    # Get remaining links from different subpages
    # They are divided between multiple sites with max 50 results in each
    for i in range(1, len(pageLinks), 1):
        browser.follow_link(pageLinks[i])
        itemLinks += getlinksfromwebsite(browser, LINK_EXTRACTION_REGEX)
        browser.back(1)
        
    clickableList = getclickablelinks(itemLinks)
    agentList, companyList = getagentandcompanynames(itemLinks)

    # Write results to file
    target = open("meck.txt", 'w')
    for a, b in enumerate(agentList):
        target.write(str(agentList[a])+";"+str(companyList[a])+";"+str(clickableList[a])+"\n")
        # print("agent='%s' link='%s'" % (str(agentList[a]), str(clickableList[a])))
    
    print "Program finished!"
    print "Exiting in 10 sec"
    time.sleep(10)
