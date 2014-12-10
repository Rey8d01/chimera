#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
e = {'hh':56, 'bb':8}
r = json.dumps(e)
print(r)
exit()

def inorder(t):
    if t:
        for x in inorder(t.left):
            yield x
        yield t.label
        for x in inorder(t.right):
            yield x


struct = {
    'f1': 1,
    'f2': 2,
    'f3': {
        'f31': 31,
        'f32': 32
    },
    'f4': [
        {
            'f411': 411
        },
        {
            'f421': 421,
            'f422': 422
        }
    ],
    'f5': 5
}

field_name = 'f4[1].f422'


class Structure:
    def __init__(self, s):
        print(s)
        self._s = s

    def __iter__(self):
        return self.in_order(self._s)

    def in_order(self, s, prefix='', set_key=None, set_value=None):
        for key, value in s.items():
            # print(value)
            if isinstance(value, dict):
                for i in self.in_order(value, key + '.', set_key, set_value):
                    yield prefix + i
            elif isinstance(value, list):
                j = 0
                for item in value:
                    for i in self.in_order(item, key + '[' + str(j) + '].', set_key, set_value):
                        yield prefix + i
                    j = j + 1
            else:
                if set_key == prefix + key:
                    s[key] = set_value
                yield prefix + key

    def __str__(self):
        return str(self._s)

    def __setitem__(self, key, value):
        for i in self.in_order(self._s, set_key=key, set_value=value):
            if i == key:
                return True
        return False


s = Structure(struct)

s[field_name] = 555
for i in s:
    print(i)

print(s)

exit()


def f1():
    return 1


def fetch_dict(dic, pre_name='', rep=None):
    for field, value in dic.items():
        print(field)
        # yield f1()
        if isinstance(value, dict):
            yield fetch_dict(value, pre_name + field + '.', rep)
        elif isinstance(value, list):
            i = 0
            for item in value:
                if isinstance(item, dict):
                    yield fetch_dict(item, field + '[' + str(i) + '].', rep)
                i = i + 1
        else:
            x_name = pre_name + field
            yield x_name

            # print(dic)
            # if pre_name == '':
            # else:
            # return x_name
            # print(x_name)
            # if x_name == rep:
            #     # print(11)
            #     value = 'GRAAAAA!'


# print(fetch_dict(struct, '', field_name))


# def replace_el(dic, field_name):
# # print(dic)
#     fields = fetch_dict(dic)
#     for field in fields:
#         print(field)
#         # if field_name == field:
#         #     dic[field] = 'GRAAAAA!'
#
# replace_el(struct, field_name)



# print(struct.items())
iter = fetch_dict(struct, '', field_name)
# # print(iter.next())
# # print(iter.next())
# # print(iter.next())
# # print(iter.next())
for i in iter:
    # print(1)
    print(i)