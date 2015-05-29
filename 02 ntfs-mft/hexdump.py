#def hexdump(data):
#    groupJoin = lambda ch, size, a: [ch.join(a[i:i+size])
#            for i in range(0, len(a), size)]
#    make = lambda c1, c2, a: groupJoin(c1, 2, groupJoin(c2, 8, a))
#    hs = ['{:02X}'.format(ord(c)) for c in data]
#    cs = [c if 0x20 <= ord(c) < 0x7f else '.' for c in data]
#    hs = make('  ', ' ', hs)
#    cs = make(' ', '', cs)
#    for i, (a, b) in enumerate(zip(hs, cs)):
#        print '{:010X}: {:48}  {:16}'.format(i * 16, a, b)

def group(a, *ns):
    for n in ns:
        a = [a[i:i+n] for i in xrange(0, len(a), n)]
    return a

def join(a, *cs):
    return [cs[0].join(join(t, *cs[1:])) for t in a] if cs else a

def hexdump(data):
    toHex = lambda c: '{:02X}'.format(ord(c))
    toChr = lambda c: c if 32 <= ord(c) < 127 else '.'
    make = lambda f, *cs: join(group(map(f, data), 8, 2), *cs)
    hs = make(toHex, '  ', ' ')
    cs = make(toChr, ' ', '')
    for i, (h, c) in enumerate(zip(hs, cs)):
        print '{:010X}: {:48}  {:16}'.format(i * 16, h, c)
