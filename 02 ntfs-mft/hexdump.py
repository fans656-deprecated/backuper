def hexdump(data):
    toHex = lambda c: '{:02X}'.format(ord(c))
    toChar = lambda c: c if 0x20 <= ord(c) < 0x7f else '.'
    group = lambda a, n, c: [c.join(a[i:i+n]) for i in xrange(0, len(a), n)]
    make = lambda a, f, c1, c2: group(group(map(f, a), 8, c1), 2, c2)
    maked = lambda r: zip(make(r, toHex, ' ', '  '), make(r, toChar, '', ' '))
    fmt = '{:010X}: {:48}  {:16}'
    return [fmt.format(i * 16, a, b) for i, (a, b) in enumerate(maked(data))]
