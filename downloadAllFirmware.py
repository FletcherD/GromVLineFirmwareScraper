#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

Attempt to download every version of the VLine firmware from the Grom website.
"""
import requests, urllib
import glob
import os
import re
import datetime, time
from multiprocessing import Pool

baseUrl1 = r'https://gromaudio.com/downloads/firmware/vl1'
baseUrl2 = r'http://g-auth.net/ota/files/release/fw/'

dlDir = './original_firmware'

firmwareBaseNames = (
    'lex4', 
    'lex5', 
    'lex6', 
    'ls460_npa',
    'toy6', 
    'toyhk',
    'ten',
    'lex7tk', 
    'lex789', 
    'nis8', 
    'nis9', 
    'nisk', 
    'hon3', 
    'gm1', 
    )

firmwareUrlDict = {
    'toyhk': 'HK',
    'nis8': 'INF8',
    'nis9': 'INF9',
    }

def setFileModifiedTime(filePath, dt):
    modTime = dt.timetuple()
    modTime = time.mktime(modTime)
    os.utime(filePath, (modTime, modTime))

def dlUrl(fullUrl):
    fileName = fullUrl.split('/')[-1]
    newFilePath = os.path.join(dlDir, fileName)
    if os.path.exists(newFilePath):
        return 1
    r = requests.get(fullUrl)
    if r.status_code == 200:
        print(fullUrl + ': success')
        with open(newFilePath, 'wb') as fOut:
            fOut.write(r.content)
        modTime = datetime.datetime.strptime(r.headers['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')
        setFileModifiedTime(newFilePath, modTime)
        return 0
    else:
        if r.status_code != 404:
            print('Error: ', fullUrl, r.status_code)
        return r.status_code
    
def getUrls(baseName, i):
    thisUrl = baseUrl1
    urls = []
    for g in ['gromvl1', 'gromvl2']:
        urls.append('{}/{}_{}_{:d}.hex'.format(thisUrl, g, baseName, i))
        if i < 10:
            urls.append('{}/{}_{}_{:02d}.hex'.format(thisUrl, g, baseName, i))
            
    if baseName in firmwareUrlDict:
        thisUrl = baseUrl2 + firmwareUrlDict[baseName]
    else:
        thisUrl = baseUrl2 + baseName.upper()
    for g in ['gromvl1', 'gromvl2']:
        urls.append('{}/{}_{}_{:d}.hex'.format(thisUrl, g, baseName, i))
        if i < 10:
            urls.append('{}/{}_{}_{:02d}.hex'.format(thisUrl, g, baseName, i))
            
    return urls

if __name__ == '__main__':
    os.makedirs(dlDir, exist_ok=True)
    
    print(firmwareBaseNames)
    
    fileUrls = []
    for baseName in firmwareBaseNames:
        for i in range(100):
            fileUrls.extend(getUrls(baseName, i))
    
    with Pool(64) as p:
        p.map(dlUrl, fileUrls)
