#!/usr/bin/env python
# -*- coding: utf-8 -*-


class A():

    _a = 1

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        print('setter')
        self._a = value


a = A()

a.a = 2
print(a.a)