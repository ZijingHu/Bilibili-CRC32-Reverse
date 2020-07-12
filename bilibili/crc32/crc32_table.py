import os
import binascii

def crc32asii(v):
    v = bytes(str(v), encoding='utf-8')
    c = '%x' % (binascii.crc32(v) & 0xffffffff)
    return c.zfill(8)

def gen_crctable():
    if 'map' not in os.listdir():
        os.mkdir('./map')
    else:
        raise SystemError('The folder "map" has already existed.')
    for i in range(0xffff):
        head = hex(i)[2:].zfill(4)
        with open(f'./map/{head}.txt', 'w', buffering=1) as f:
            pass

    for c in range(200):
        map_dict = {hex(crc_head)[2:].zfill(4): [] for crc_head in range(0x10000)}
        list(map(
            lambda i: map_dict[crc32asii(i)[:4]].append(str(i)),
            range(c*3500000, (c+1)*3500000)
        ))
        for head in map_dict.keys():
            with open(f'./map/{head}.txt', 'a', buffering=1) as f:
                f.write('\n'.join(map_dict[head])+'\n')
        print(f'{c+1}/200\r', end='')