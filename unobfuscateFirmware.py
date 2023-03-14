#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

Output
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

The GROM firmware is XOR'ed with a 512-byte key to obfuscate it.
Write an unobfuscated version of every firmware file using the key
"""
import glob
import os
import collections
from itertools import cycle

firmwareNames = glob.glob('original_firmware/*.hex')
outputDir = 'original_firmware_unobfuscated'
os.makedirs(outputDir, exist_ok=True)

headerN = 4
loopN = 512
byteVals = [collections.Counter() for i in range(loopN)]

with open('xorKey.bin', 'rb') as f:
    xorLoop = f.read()
    
def byte_xor(ba1, ba2):
        """ XOR two byte strings """
        return bytes([_a ^ _b for _a, _b in zip(ba1, cycle(ba2))])

for fName in firmwareNames:
    print(fName)
    with open(fName, 'rb') as f:
        header = f.read(headerN)
        fBytes = f.read()
        fBytesXor = byte_xor(fBytes, xorLoop)
        with open(os.path.join(outputDir, os.path.basename(fName)), 'wb') as fx:
            fx.write(header)
            fx.write(fBytesXor)
