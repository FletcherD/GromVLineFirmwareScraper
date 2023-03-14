#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

Used to correct the XOR key used for obfuscation.
Correct any errors found in the firmware and this will correct the XOR key based on that and output the new value
No need to run this, the value currently in xorKey.bin is the correct one and no more corrections are necessary
"""
import glob
import os
import collections
from itertools import cycle

firmwareNames = glob.glob('original_firmware/*.hex')
correctedDir = 'original_firmware_unobfuscated'

with open('xorKey.bin', 'rb') as f:
    xorLoop = f.read()

headerN = 4
xorLoopNew = bytearray(xorLoop)

def printBytes(b):
    print(''.join(['{:02x}'.format(v) for v in b]))

for fName in firmwareNames:
    basename = os.path.basename(fName)
    newName = os.path.join(correctedDir, basename)
    fOld = open(fName, 'rb').read()[headerN:]
    fNew = open(newName, 'rb').read()[headerN:]
    for i in range(len(fOld)):
        xorVal = fOld[i] ^ fNew[i]
        if xorVal != xorLoop[i%512]:
            print('Byte {:3d} new value: {:02x}'.format(i%512, xorVal))
            xorLoopNew[i%512] = xorVal
        
printBytes(xorLoopNew)
