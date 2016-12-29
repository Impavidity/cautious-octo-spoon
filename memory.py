# -*-coding: utf-8 -*-

def readMemory(inst_mem, base_mem, vol_mem, vel_mem):
    with open("memory.txt") as f:
        lines = [line.strip() for line in f]
    for item in lines[0].split(' '):
        inst_mem.append(int(item))
    for item in lines[1].split(' '):
        base_mem.append(int(item))
    for item in lines[2].split(' '):
        vol_mem.append(int(item))
    for item in lines[3].split(' '):
        vel_mem.append(int(item))

def writeMemory(inst_mem, base_mem, vol_mem, vel_mem):
     with open("memory.txt") as f:
        for item in inst_mem:
            f.write("%d " %item)
        f.write('\n')
        for item in base_mem:
            f.write("%d " %item)
        f.write('\n')
        for item in vol_mem:
            f.write("%d " %item)
        f.write('\n')
        for item in vel_mem:
            f.write("%d " %item)
        f.write('\n')