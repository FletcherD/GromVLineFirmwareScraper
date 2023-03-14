#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 21:36:22 2023

@author: fletcher

Read a raw binary file compiled for the VBase microprocessor (a NXP LPC1765)
    and modify it so it will be accepted and flashed by the VBase bootloader.
There are several things that need to be true for VBase to accept the image:
    1. There must be a 4 byte header of "VL" followed by a version number.
    2. The value at 0x1F4 must be the magic number 0x5abc1fe9.
    3. The value at 0x1C must be the magic number 0x21436587. This is the value 
        used by the NXP chip to enable Code Read Protection, however it isn't
        at the correct offset here; it seems to just be used as a magic number
        by the VBase bootloader.
    4. The version number must also be at 0x1F0. The version number must be 
        different from the current firmware. I use the current time to 
        basically just randomize this.
    5. All bytes other than the first 4 must be XOR'ed with the magic 512-byte key.
"""
import sys
import os
import collections
import time
from itertools import cycle

inFile = sys.argv[1]

with open('xorKey.bin', 'rb') as f:
    xorLoop = f.read()
    
def byte_xor(ba1, ba2):
        """ XOR two byte strings """
        return bytes([_a ^ _b for _a, _b in zip(ba1, cycle(ba2))])

versionNum = [0x14, int(time.time())%256]
magicNum = [0x5a, 0xbc, 0x1f, 0xe9]
crpNum = [0x21, 0x43, 0x65, 0x87]

with open(inFile, 'rb') as f:
    fBytes = bytearray(f.read())

    header = bytes([ord('V'), ord('L'), versionNum[0], versionNum[1]])

    fBytes[0x1F0:0x1F2] = [versionNum[1], versionNum[0]]
    fBytes[0x1F4:0x1F8] = magicNum
    fBytes[0x1C:0x20] = crpNum

    fBytesXor = byte_xor(fBytes, xorLoop)
    with open('gromvl1.hex', 'wb') as fOut:
        fOut.write(header)
        fOut.write(fBytesXor)
