#! /usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom 
import urllib
import re
import xml.etree.ElementTree as ET

parts = ["@", ":at", "\(at\)"]

def parseXML(name):
    tree = ET.parse(name)  
    root = tree.getroot()
    mainList = []
    for el in root: 
        mainList.append(el.text) 
    return mainList

#  (?:@|:at|\(at\))  

def proceed(list1, depth):
    emails = []
    links = []
    for el in list1:
        response = urllib.urlopen(el).read()
        emails += re.findall(r"\"?([-a-zA-Z0-9.`?{}]+(?:%s)+\w+\.\w+)\"?" % ("|".join(parts)), response)
        links += re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response)
    depth-=1
    if (depth < 0): return emails
    else: return emails+proceed(links, depth)

emailsXML = ET.Element('emails')
for email in proceed(parseXML('data.xml'), 1):
    curEmail = ET.SubElement(emailsXML, 'email')
    curEmail.text= email
resData = minidom.parseString(ET.tostring(emailsXML)).toprettyxml(indent='\t')
resFile = open("res.xml", "w")  
resFile.write(resData)

    

