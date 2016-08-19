#!/usr/bin/python

import tkSimpleDialog
import tkMessageBox
import mechanize
import re
from mechanize._html import Link
import Tkinter
import time
import sys
import urllib2
import xml.etree.ElementTree as ET


# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText


class timeChunk:
    def __init__(self):
        self.fr = ''
        self.to = ''
        self.period = ''
        self.windspeed = ""
    def getFr(self):
        return self.fr
    def getTo(self):
        return self.to
    def getPeriod(self):
        return self.period
    def getWindspeed(self):
        return self.windspeed
    def __str__(self):
        return self.fr.__str__() + self.to.__str__()


def sendMail(message):
    # Create a text/plain message
    msg = MIMEText(message)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = "MySubject"
    msg['From'] = "asdasd"
    msg['To'] = "hej.dave@gmail.com"

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP('localhost')
    s.sendmail("asdasd", ["hej.dave@gmail.com"], msg.as_string())
    s.quit()

def collectXmlFile(url):
    response = urllib2.urlopen(url)
    xml = response.read()
    return ET.fromstring(xml)


if __name__ == "__main__":
    tree = collectXmlFile('http://www.yr.no/sted/Sverige/Stockholm/Saltsj%C3%B6baden/varsel.xml')

    # for child in tree:
    #     print(child.tag, child.attrib)

    for period in tree[len(tree)-1][0]:
        print(period.tag, period.attrib)