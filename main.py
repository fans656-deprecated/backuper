import itertools

def hexDump(data):
    toHex = lambda c: '{:02X}'.format(ord(c))
    toChar = lambda c: c if 0x20 <= ord(c) < 0x7f else '.'
    group = lambda a, n, c: [c.join(a[i:i+n]) for i in xrange(0, len(a), n)]
    make = lambda a, f, c1, c2: group(group(map(f, a), 8, c1), 2, c2)
    maked = lambda r: zip(make(r, toHex, ' ', '  '), make(r, toChar, '', ' '))
    fmt = '{:010X}: {:48}  {:16}'
    return [fmt.format(i * 16, a, b) for i, (a, b) in enumerate(maked(data))]

class PTE(object):

    def __init__(self, data):
        data = map(ord, data)
        self.data = data
        self.status = self.getStatus(data[0])
        self.type = self.getType(data[4])
        self.empty = self.type == 'Empty'
        self.begSector = self.getCHS(data[1:1+3])
        self.endSector = self.getCHS(data[5:5+3])
        self.begLBA = self.getInt(data[8:8+4])
        self.numSectors = self.getInt(data[0xc:0xc+4])

    def getStatus(self, data):
        try:
            return {0x80: 'active', 0x00: 'inactive'}[data]
        except KeyError:
            return 'invalid'

    def getType(self, data):
        try:
            return {0x00: 'Empty',
                    0x07: 'NTFS',
                    0x42: 'Dynamic'}[data]
        except KeyError:
            return 'Unknown'

    def getCHS(self, data):
        head = data[0]
        sector = data[1] & 0x3f
        cylinder = ((data[1] & 0xc0) << 2) | data[2]
        return (cylinder, head, sector)

    def getInt(self, data):
        return data[3] << 24 | data[2] << 16 | data[1] << 8 | data[0]

    def __str__(self):
        s = ''
        s += '\n' + 'Status:            {}'.format(self.status)
        s += '\n' + 'Type:              {}'.format(self.type)
        s += '\n' + 'Beg:               {}'.format(self.begSector)
        s += '\n' + 'End:               {}'.format(self.endSector)
        s += '\n' + 'BegLBA:            {}'.format(self.begLBA)
        s += '\n' + 'Number of sectors: {}'.format(self.numSectors)
        s += '\n' + 'Size:              {} GiB'.format(self.numSectors * 512 >> 30)
        return s

for idisk in itertools.count():
    try:
        data = open('mbr{}.bin'.format(idisk), 'rb').read()[0x1be:]
        ptes = [PTE(data[i*16:i*16+16]) for i in range(4)]
        ptes = [pte for pte in ptes if not pte.empty]
        print '=' * 30 + 'Pysical Disk {}'.format(idisk)
        for pte in ptes:
            print pte
        print
    except IOError:
        break
