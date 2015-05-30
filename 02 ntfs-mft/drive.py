import os
import struct
import itertools

import win32file
import winioctlcon

def getPhysicalDrivePaths():
    prefix = r'\\.\PhysicalDrive'
    paths = []
    for i in itertools.count():
        try:
            path = prefix + str(i)
            open(path).close()
            paths.append(path)
        except IOError:
            break
    return paths

def getDiskSectorSize(drivePath):
    hDrive = win32file.CreateFile(
            drivePath,
            win32file.GENERIC_READ,
            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None,
            win32file.OPEN_EXISTING,
            0,
            0)
    data = win32file.DeviceIoControl(
            hDrive,
            winioctlcon.IOCTL_DISK_GET_DRIVE_GEOMETRY,
            None,
            24,
            None
            )
    win32file.CloseHandle(hDrive)
    return struct.unpack('I', data[-4:])[0]

if __name__ == '__main__':
    print 'Physical Drives:'
    for path in getPhysicalDrivePaths():
        print '\tDrive: {}, Sector size: {}'.format(
                path,
                getDiskSectorSize(path))
