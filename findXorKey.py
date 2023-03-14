#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

The GROM firmware is XOR'ed with a 512-byte value to obfuscate it.
Attempt to determine the 512 byte value that is used by performing simple frequency analysis.

Don't run this!! THe value in xorKey.bin is already correct, this will change it
"""
import glob
import os
import collections
from itertools import cycle

firmwareNames = glob.glob('original_firmware/*.hex')

headerN = 4
loopN = 512
byteVals = [collections.Counter() for i in range(loopN)]

for fName in firmwareNames:
    print(fName)
    with open(fName, 'rb') as f:
        fBytes = f.read()[headerN:]
        for i, b in enumerate(list(fBytes)):
            byteVals[i%loopN].update([b])

byteVals = bytes([c.most_common(1)[0][0] for c in byteVals])
print(''.join(['{:02x}'.format(v) for v in byteVals]))

#with open('xorKey.bin', 'wb') as f:
#    f.write(byteVals)