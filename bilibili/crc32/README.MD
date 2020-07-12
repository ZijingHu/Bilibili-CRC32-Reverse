# Bilibili.com UID Search

## Guide

1. Get cid of a video.
    - https://api.bilibili.com/x/player/pagelist?bvid={bvid}
2. Get danmaku data from
    - http://comment.bilibili.com/{cid}.xml
    - http://api.bilibili.com/x/v2/dm/history?type=1&oid={cid}&date={yyyy-mm-dd}
3. Get crc32-uids from the 7th column
4. Access users' home page
    - https://space.bilibili.com/{uid}

**Please note that about 8% of crc32-uids are not unique and nothing you can do to fix it.**

## Usage

When uses for the first time, you need to generate the reference table that may require 7GB of storage.
```
from crc32_table import *

gen_crctable()
```

If you have already generated the reference table...
```
from crc32_reverse import *

find_uid(uid_crc32)
```


## Reference

- https://github.com/shafferjohn/bilibili-search
- https://github.com/Aruelius/crc32-crack
- https://moepus.oicp.net/2016/11/27/crccrack/