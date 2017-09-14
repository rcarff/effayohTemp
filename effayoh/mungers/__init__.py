from __future__ import division, absolute_import, print_function
from builtins import super

class FAOCountry(tuple):

    __slots__ = []
    object_pool = {}

    def __new__(cls, country, code):
        tup = (country, code)
        if tup in FAOCountry.object_pool:
            return FAOCountry.object_pool[tup]
        else:
            obj = super().__new__(cls, tup)
            FAOCountry.object_pool[obj] = obj
            return obj
