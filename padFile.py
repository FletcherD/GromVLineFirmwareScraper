#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

Pads a firmware file to 128k, writing the file offset every so often. This can be used when reading back the firmware to debug the firmware positioning
"""
import sys
import os
import collections
import time
import struct
from itertools import cycle

gromFirmwareSize = 0x20000

inFileName = sys.argv[1]
outFileName = os.path.splitext(inFile)[0]+'.pad.hex'

with open(outFileName, 'wb') as fOut:
    with open(inFileName, 'rb') as fIn:
        fOut.write(fIn.read())

    while fOut.tell() % 16 != 0:
        fOut.write(0)

    while fOut.tell() < gromFirmwareSize:
        row = bytearray(16)
        row[0:4] = struct.pack("<I", fOut.tell())
        fOut.write(row)
