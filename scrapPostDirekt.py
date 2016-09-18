#!/usr/bin/env python

"""Scrapes data and saves into CSV file

Scrapes data from postdirekt.de about German addresses 
and  parses into a CSV file.
"""
import csv
import datetime
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

__author__ = "Lorenzo Lerate"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "lorenzo.lerate@gmail.com"


url = 'https://www.postdirekt.de/plzserver/PlzAjaxServlet' 
listPostalCodes = list()

#first step: gather all the zip codes starting from 01 to 99
print('Gathering zip codes')
for i in range(1,100): #show progress
    print(str(datetime.datetime.now())+' '+str(i)+'% complete')
    index = ("%02d" % (i,))
    post_fields = {'finda':'city','city':"'"+index+"'",'lang':'de_DE'}  #set POST fields

    request = Request(url, urlencode(post_fields).encode()) #request data 
    response = urlopen(request).read().decode()
    jsonResponse = json.loads(response) #parse response into JSON
    try:
        dictRows = jsonResponse['rows'] #the 'row' section is where is the needed information
        for row in dictRows:
             listPostalCodes.append(row['plz'])
    except Exception:
        continue

print (str(len(listPostalCodes))+' postal codes')

listPlaces = list()
percentaje = 0
print('Gathering addresses')

#preparing CSV file
csvFilename = 'addresses.csv'
with open(csvFilename, 'w') as csvFile:  #open CSV file
    fieldnames = ['plz','city','cityaddition','district','street']
    writer = csv.DictWriter(csvFile, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader() #write header with selected columns
    
    #step2: iterate over zip codes list and get the value of the related addreses
    for postalCode in listPostalCodes:
        if (i % round(len(listPostalCodes) / 100)) == 1: #show progress
            if(percentaje<100):
                print(str(datetime.datetime.now())+' '+str(percentaje)+'% complete')
                percentaje+=1
                writer.writerows(listPlaces) #every percentil is reached write into the CSV file and empty list
                listPlaces.clear()
            elif percentaje == 100:
                print(str(datetime.datetime.now())+' Almost done')
                percentaje+=1
            
        i+=1
        post_fields = {'finda':'streets','plz_plz':"'"+postalCode+"'", 'lang':'de_DE'}  #ser POST fields
        
        try:
            request = Request(url, urlencode(post_fields).encode())
            response = urlopen(request).read().decode()
            jsonResponse = json.loads(response)

            dictRows = jsonResponse['rows'] #the 'row' section is where is the needed information
            for row in dictRows:
                listPlaces.append(row)
        except Exception as e:
            print (e)
            break

    writer.writerows(listPlaces)

file = open(csvFilename)
numlines = len(file.readlines())
print ('Added '+str(numlines)+' places to '+csvFilename)
file.close()
