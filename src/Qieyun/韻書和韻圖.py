# -*- coding: utf-8 -*-

'''
切韻系韻書及早期韻圖資料上的操作。
'''

from collections import namedtuple

from .韻書 import _字頭2音韻地位_韻書出處們
from ._韻圖 import _字頭_音韻地位2韻圖出處們

音韻地位_出處們 = namedtuple('條目', ['音韻地位', '韻書出處們', '韻圖出處們'])


def 字頭2音韻地位_出處們(字頭):
    '''
    獲取字頭對應的所有音韻地位及其韻書和韻圖出處。
    '''
    return [
        音韻地位_出處們(
            音韻地位=音韻地位,
            韻書出處們=韻書出處們,
            韻圖出處們=_字頭_音韻地位2韻圖出處們(字頭, 音韻地位),
        ) for 音韻地位, 韻書出處們 in _字頭2音韻地位_韻書出處們(字頭)
    ]
