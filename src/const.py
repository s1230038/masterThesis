"""
Constant types in Python.
# https://maku77.github.io/python/syntax/const.html

How to use:
import const

const.FOO = 100
const.BAR = 'Hello'
"""

class _const:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value

import sys
sys.modules[__name__]=_const()