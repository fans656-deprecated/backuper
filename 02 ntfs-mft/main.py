from hexdump import hexdump

try:
    f = open(r'\\.\PhysicalDrive0', 'rb')
    s = f.read(512)
    hexdump(s)
    f.close()
except IOError as e:
    print dir(e)
