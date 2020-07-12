import binascii

def crc32asii(v):
    v = bytes(str(v), encoding='utf-8')
    c = '%x' % (binascii.crc32(v) & 0xffffffff)
    return c.zfill(8)

def find_uid(uhash):
    head = uhash.zfill(8)[:4]
    with open(f'./map/{head}.txt', 'r') as f:
        match = list(filter(lambda x: crc32asii(x)==uhash, f.read().split('\n')))
    if len(match) == 0:
        return None
    elif len(match) > 1:
        print('Duplicates: ', match)
        return match[0]
    else:
        return match[0]
    
    
if __name__ == '__main__':
    # test
    uhash = 'd3734f71'
    # 268639242
    find_uid(uhash)