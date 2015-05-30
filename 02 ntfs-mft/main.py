from pprint import pprint

from drive import *
from hexdump import hexdump

drives = getPhysicalDrivePaths()
path = drives[0]
with open(path, 'rb') as f:
    sectorSize = getDiskSectorSize(path)
    mbr = f.read(512)
    hexdump(mbr)
    print 'Sector size: {}'.format(sectorSize)
