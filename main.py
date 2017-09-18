# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:42:46 2017

@author: vadim
"""
import urllib.request
import lxml.html
import urllib.parse
import sys



class Stack:
    def __init__(self):
        self.items=[]

    def isEmpty(self):
        return self.items==[]

    def push(self , item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]
    


def GetUrl(siteInfo, link):
    linkDic = urllib.parse.urlparse(link)
    url = "";

    if linkDic.path:
        if linkDic.hostname == siteInfo.hostname:
            url = link
        elif not linkDic.hostname:
            url = siteInfo.scheme + "://" + siteInfo.hostname + link;
        
    return url



def Response(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    doc = urllib.request.urlopen(req);
    return doc

def GetInfo(url):
    allLinks = {}
    stack = Stack()
    stack.push(url)
    siteInfo = urllib.parse.urlparse(url)

    print(siteInfo)
    file = open('main.txt','w') 
    while not stack.isEmpty():
        currentLink = stack.pop()
        print(stack.size())
        response = Response(currentLink)
        statusCode = response.getcode()
        allLinks[currentLink] = statusCode
        
        htmlCode = lxml.html.document_fromstring(response.read())
        file.write(currentLink + "\n")
        for link in htmlCode.xpath("//a"):
            #file.write(url)
            newUrl = GetUrl(siteInfo, link.get("href"))
            file.write("                " + str(newUrl) + "    |    " + str(link.get("href")) + "\n")
            if(not allLinks.get(newUrl)):
                stack.push(newUrl)
                allLinks[newUrl] = 200
               # break
            
    file.close()
    return allLinks

    


def main(argv):
    
    print ("Hello World!")
    url = 'https://applepride.ru/'
    info = GetInfo(url);
    
   # OutputLinks(links)
main("FF")
if (len(sys.argv) == 2):
    main(sys.argv[1])
else:
    print("Неверное количество параметров")