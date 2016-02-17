#!/usr/bin/python

import mechanize
import re
import time
import socket

def getMyCurrentIp():
    my_browser = mechanize.Browser(factory=mechanize.RobustFactory())
    my_browser.set_handle_robots(True)

    site = my_browser.open("http://showip.net/")
    
    fullList = site.readlines()
    for index, val in enumerate(fullList):
        nr = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', val)
        if(nr):
            return nr.group(0)


if __name__ == "__main__":
    print "Starting Script!"
    #Date;Local Ip;External Ip
    target = open("ip_info.log", 'a')
    target.write(time.strftime("%Y-%m-%d")+";"+
                 socket.gethostbyname(socket.gethostname())+";"+
                 getMyCurrentIp()+"\n")
    
    print "End of script!"
    
