#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 20:28:03 2023

@author: fletcher
"""
import requests
from multiprocessing import Pool, Manager

baseUrl = 'http://104.153.44.149/ota/ota.php?action=update&v={}&fwCode={}&fwNumber={}&fwLoader={}'
version = 'V2OVL3.62.0.0'
fwNumber = 0

goodFwCodes = {6, 7, 8, 20, 21, 22, 27, 31, 32, 78, 80, 81, 88, 90}

def getFwUpdate(thingToDo):
    version, fwCode, fwNumber, fwLoader = thingToDo
    thisUrl = baseUrl.format(version, fwCode, fwNumber, fwLoader)
    r = requests.get(thisUrl)
    if r.status_code == 200 or r.status_code == 300:
        fwDict[(fwCode, fwLoader)] = r.text
        if r.status_code == 200 and len(r.text) > 0:
            print(fwCode, fwLoader, r.text)
            return r.text
    else:
        print('Error: ', thisUrl, r.status_code)

def init_pool(dictX):
    # function to initial global dictionary
    global fwDict
    fwDict = dictX

if __name__ == '__main__':
    thingsToDo = []
    for i in goodFwCodes:
        for j in range(200):
            if (i, j) not in fwDict2:
                thingsToDo.append((version, i, 0, j))
            
    with Manager() as manager:
        fwDict = manager.dict(fwDict2)
        pool = Pool(10, initializer=init_pool, initargs=(fwDict,))
        pool.map(getFwUpdate, thingsToDo)
        pool.close()
        pool.join()
        print(fwDict)
        fwDict2 = dict(fwDict)