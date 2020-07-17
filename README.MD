## Tools for Scraping bilibili.com

- [API Collection](https://github.com/SocialSisterYi/bilibili-API-collect)
- [CRC32-uid Reverse](./bilibili/crc32)
Get uid from danmaku api. The probability is 0.08 that the uid is not unique.
- [Danmaku & Audience Persona](./bilibili/scraper.py)
Scrape danmaku data and construct persona for senders of danmaku.

...

## Usage

-  **For cracking crc32-uid**

More details can be found [here](./bilibili/crc32/README.MD)

When use for the first time, you need to generate the reference table that may require 7GB of storage.
```
from bilibili.crc32.crc32_table import *

gen_crctable()
```

If you have already generated the reference table...
```
from bilibili.crc32.crc32_reverse import *

find_uid(crc32-uid)
```

-  **For scrapping danmaku / followings / publication types**

```
from bilibili.scraper.danmaku import *

# login to get cookies
login()

# prepare the bvid and date of video before scrapping
cid = get_cid_via_bv(bvid)
get_danmaku(cid, yyyy-mm-dd)
get_following(uid)
get_pub(uid) # Get all categories of publication of the user
```

## License
[MIT](https://choosealicense.com/licenses/mit/)