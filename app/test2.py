#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
collections.OrderedDict()

d = collections.OrderedDict({
    "q1": 1,
    "_q3": 3,
    "q2": {
        "q21": 21,
        "_q22": 22,
        "q23": [
            {
                "_q2311":2311, "q2312":2312
            },
            {
                "q2321":2321, "q2322":2322
            }
        ]
    }
})

l = [1, 2, 3]

# for i in d:
#     print(i)




# x = filter(lambda i: i[0] != "_", d)

# x = map(lambda i: (i, d[i]) if i[0] != "_" else (None, None), d)
# print(dict(x))
# for i, j in x:
#     print(i, j)

def _filter(x):
    if isinstance(x, dict):
        y = {}
        for key in x:
            if key[0] != "_":
                y[key] = _filter(x[key])
        return y
    elif isinstance(x, list):
        y = []
        for value in x:
            y.append(_filter(value))
        return y

    return x



t = _filter(d)

print(t)