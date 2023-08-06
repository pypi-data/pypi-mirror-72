#!/usr/bin/env python3

import json

__IMAGE_DOS_HEADER__ = '''
{
    "e_magic":{
        "value": 0,
        "type":"word",
        "offset": 0,
        "size": 2
    }
}
'''

__IMAGE_NT_HEADERS__ = '''
{
    "Signature":{
        "value": 0,
        "type": "dword",
        "offset": 0,
        "size": 4
    }
}
'''

# name, value, type, offset, size
idh = (
    ("e_magic", 0x00, "word", 0x00, 0x02),
    ("e_cblp", 0x00, "word", 0x02, 0x02)
)

for n, v, t, o, s in idh:
    print(n)

#idh = json.loads(__IMAGE_DOS_HEADER__)
