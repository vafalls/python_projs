#!/usr/bin/python

import mechanize
import re
import time
import os
import cgi
from mechanize._html import Link
from _mysql import NULL
BASE_URL = "http://www.bokat.se/protected/"

if __name__ == "__main__":
    print "starting"
    target = open("test_file.txt", 'w')
    
    a = 'Anders Sj\xf6kvist'
    print a
    target.write("1: "+a)
#     a = unicode(a, "utf-8")
    print a
    target.write("2: "+a)
    
    print "ending"