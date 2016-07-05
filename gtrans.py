#!/usr/bin/env python
# -*- coding: latin-1 -*-
from __future__ import print_function
import urllib2, sys, time, os

##lazycoder
srcl = "en" #source language
dstl = "es" #destination language

srcf = "./eng.txt" #the source language strings
dstf = "./tr.txt" #the destination language strings
format = "A" # "w" is for web which is javascript base key,value example for translations(see example input text file) or  "i" is for iphone translations STRINGS file and A for 
# Android string.xml file
#Android input <string name="username">Username</string>

# srcf = "./ip"
# dstf = "./Localizable.strings" + "_" + dstl
# format = "i" # or  "i"

# remove file if exists
if os.path.exists(dstf): os.remove(dstf)

def translate(to_translate, to_langage=dstl, langage=srcl):
    agents = {'User-Agent':"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read()
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    # time.sleep(1)
    return result
    #print result

if __name__ == '__main__':
    #to_translate = raw_input("Enter Your String>>>>>>") #you can use this shit for single translate
    with open(srcf, 'r') as f, open(dstf, "a") as g:
        content = f.readlines()
        for i in content:
            try:
                if format == "w" :
                    txt = i.split(":",1)[-1]
                    txtClean = txt.strip().replace("'","").rstrip(",")

                if format == "i" :
                    txt = i.split("=", 1)[0]
                    txtClean = txt.strip().replace("'","").replace('"', '').rstrip(";")
                if format == "A" :
                    key = i.split("=",1)[1].replace('"',"").split(">",1)[0]
                    txtClean = i.split("=",1)[1].replace('"',"").split(">",1)[1].split("<",1)[0]

                print( "Text: " + txtClean )

                if(txtClean) :
                    tr_txt = translate(txtClean)

                    # print( "TR    : " + tr_txt )
                    # print("\n")

                    if format == "w" :
                        j = i.replace(txt, '"' + tr_txt + '",')
                    if format == "i" :
                        rept = i.split("=", 1)[1]
                        j = i.replace(rept, '"' + tr_txt + '";')
                    if format == "A" :
                        rept = i.split("=",1)[1].replace('"',"").split(">",1)[0]
                        j = i.replace(rept, '"' + tr_txt + '";')
                    g.writelines(j + "\n")
            except :
                g.writelines("// failed: " + i + "\n")
    f.close()
    g.close()
