# -*- coding: utf-8 -*-

import midi_controler as md 
import display
import keyboard
import os
import pygame.midi
from evdev import InputDevice, list_devices, ecodes
import memory
import sys
from select import select
from midiPattern import MidiPattern
import time

Count = dict()
for item in ["KEY_F1", "KEY_F2", "KEY_F3", "KEY_F4", "KEY_F5"]:
    Count[item] = 0


mi = md.Midi()
mi.setup()
'''
disp = display.Display()
disp.setup()
'''

# Arguments in Memory
mem = 1
inst_mem = list()
base_mem = list()
vol_mem = list()
vel_mem = list()
memory.readMemory(inst_mem, base_mem, vol_mem, vel_mem)


# Key-code
getCode = dict()
with open("keybinds.txt") as f:
    for line in f:
        (keyname, code) = line.split()
        getCode[keyname] = int(code)

# Key-note
getNote = dict()
with open("keyseq.txt") as f:
    for line in f:
        (keyname, note) = line.split()
        getNote[keyname] = int(note)

# Get device
devices = list()
for fn in list_devices():
    dev = InputDevice(fn)
    rate = dev.repeat[0]
    if rate > 0:
        devices.append(dev.fn)

devices = map(InputDevice, devices)
devices = {dev.fd: dev for dev in devices}

num_devices = len(devices)

print num_devices,"keyboards detected"

def quitCautious():
    for _fd in devices.keys():
        try:
            devices[_fd].ungrab();
        except IOError:
            print "Already ungrabbed"
    #disp.close()
    mi.close()
    #disp.pygame.quit()
    sys.exit()
    return

# Grab keyboards
if num_devices == 0:
    print "Do not find keyboards"
    quitCautious()

for _fd in devices.keys():
    try:
        devices[_fd].grab()
        print "Grabbed keyboard", devices[_fd]
    except IOError:
        print "Already grabbed"

# Setup keyboards
keyboards = dict()
_number = 1
for d in devices:
    _keyboard = keyboard.Keyboard(_number, _number-1, inst_mem[mem-1], vol_mem[mem-1], 30, 70, base_mem[mem-1], 0)
    keyboards[d] = _keyboard
    _number += 1

print keyboards

# Configure keyboard
kbCount = 0
for kb in keyboards.values():
    kb.config(mi)
    for keyname in getCode.keys():
        kb.pressed[keyname] = 0
        kbCount += 1


recordList = list()

while True:
    rlist, wlist, xlist = select(devices, [], [])
    currentChannel = 0
    for fd in rlist:
        for event in devices[fd].read():
            # Identify device
            kb = keyboards[fd]
            # Identify key
            # Map from event.code to keyname by ecodes.KEY
            keyname = ecodes.KEY[event.code]
            
            #print event.type,keyname,event.value
            if event.type == ecodes.EV_KEY and keyname in getCode.keys():
                if event.value == 1: # Keydown
                    if keyname == "KEY_ESC":
                        quitCautious()
                    elif keyname == "KEY_F1" and Count[keyname] == 0:
                        record = MidiPattern(kbCount) # kbCount == Channel number
                        recordList.append(record)
                        Count[keyname] += 1
                        Count["KEY_F2"] = 0
                        record.start_record()
                    elif keyname == "KEY_F2" and Count[keyname] == 0:
                        recordList[-1].stop_record(len(recordList))
                        Count["KEY_F1"] = 0
                    else: # Play note
                        kb.noteOf[keyname] = kb.baseNote + getNote.get(keyname, -100)-1
                        # default -100 as a flag
                        if kb.noteOf[keyname] >= kb.baseNote: # Check if it is one of the note
                        # Ignore it if it is not
                            kb.key_down(mi, keyname, kb.noteOf[keyname])
                            if Count["KEY_F1"] > 0:
                                recordList[-1].add_note(ctime=time.time(), channel=currentChannel, note=kb.noteOf[keyname], velocity=kb.velocity)
                elif event.value == 0: # Keyup
                    if False:
                        pass
                    else: # Play note
                        if keyname in kb.noteOf.keys():
                            kb.key_up(mi, keyname, kb.noteOf[keyname])
                            if Count["KEY_F1"] > 0:
                                recordList[-1].add_note(ctime=time.time(), channel=currentChannel, note=kb.noteOf[keyname], velocity=0)
        currentChannel += 1

    #disp.update()
    #disp.check_exit()

'''
mi.turnDown()
'''


