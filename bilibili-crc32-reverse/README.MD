# Bilibili.com UID Search

## Guide

1. Get cid of a video. API: https://api.bilibili.com/x/player/pagelist?bvid={bvid}
2. Get danmaku data from http://comment.bilibili.com/{cid}.xml
3. UIDs are stored in the 7th columns

## Usage

```
from crc32_reverse import *

find_uid(uid_crc32)
```


## Reference

- https://github.com/shafferjohn/bilibili-search
- https://github.com/Aruelius/crc32-crack
- https://moepus.oicp.net/2016/11/27/crccrack/