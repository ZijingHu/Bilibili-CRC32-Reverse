import binascii

def crc32asii(v):
    v = bytes(str(v), encoding='utf-8')
    c = '%x' % (binascii.crc32(v) & 0xffffffff)
    return c.zfill(8)

def find_uid(uhash):
    head = uhash.zfill(8)[:4]
    with open(f'./map/{head}.txt', 'r') as f:
        match = list(filter(lambda x: crc32asii(x)==uhash, f.read().split('\n')))
    return match
    
    
if __name__ == '__main__':
    # test
    uhash = 'd3734f71'
    # 268639242
    find_uid(uhash)