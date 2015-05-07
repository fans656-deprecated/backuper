import struct
import os

from hexdump import hexdump

MBR_PTE_OFFSET = 0x1be # partition table entry offset in mbr
MBR_PTE_SIZE = 16 # partion table entry size
MBR_PTE_PBS_OFFSET = 0x08 # partion boot sector offset in partion entry

def getPBSOffset(mbr):
    i = MBR_PTE_OFFSET + MBR_PTE_PBS_OFFSET
    return struct.unpack('<L', mbr[i:i+4])

#with open('mbr0.bin', 'rb') as f:
#    mbr = f.read(512)
#    pbsOffset = 512 * getPBSOffset(mbr)[0]
#    print pbsOffset

#with open(r'\\.\PhysicalDrive0', 'rb') as f:
#    f.seek(pbsOffset)
#    pbs = f.read(512)
#    open('pbs0-0.bin', 'wb').write(pbs)

pbs = open('pbs0-0.bin', 'rb').read()
for line in hexdump(pbs):
    print line
