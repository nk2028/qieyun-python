# -*- coding: utf-8 -*-

'''
切韻系韻書資料上的操作。
'''

from collections import defaultdict, namedtuple
from os import path
from typing import Optional

from .音韻地位 import 音韻地位
from ._書影 import 生成書影

HERE = path.abspath(path.dirname(__file__))

d字頭2編碼們 = defaultdict(dict)
d編碼2字頭們 = defaultdict(dict)
d編碼2廣韻字頭們 = defaultdict(dict)
d字頭_編碼2韻書出處們 = defaultdict(list)
d資料名稱_小韻號_編碼2字頭們 = defaultdict(dict)

def iter音韻地位():
    '''
    所有至少對應一個字頭的音韻地位。
    '''
    for 編碼 in d編碼2字頭們:
        yield 音韻地位.from編碼(編碼)

def _字頭2音韻地位_韻書出處們(字頭: str):
    '''
    由字頭查出相應的音韻地位和解釋。
    '''
    return [
        {
            '音韻地位': 音韻地位.from編碼(編碼),
            '韻書出處們': d字頭_編碼2韻書出處們.get((字頭, 編碼), []),
        } for 編碼 in d字頭2編碼們.get(字頭, [])
    ]

def 音韻地位2代表字(當前音韻地位) -> Optional[str]:
    '''
    獲取音韻地位對應的代表字。
    '''
    編碼 = 當前音韻地位.編碼

    # 優先選擇廣韻字頭
    廣韻字頭們 = d編碼2廣韻字頭們.get(編碼)
    if 廣韻字頭們 is not None:
        return next(iter(廣韻字頭們))

    字頭們 = d編碼2字頭們.get(編碼)
    if 字頭們 is not None:
        return next(iter(字頭們))

    return None

def 音韻地位2字頭_韻書出處們(當前音韻地位):
    '''
    獲取音韻地位對應的所有字頭及其韻書出處。
    '''
    編碼 = 當前音韻地位.編碼
    return [
        {
            '字頭': 字頭,
            '韻書出處們': d字頭_編碼2韻書出處們.get((字頭, 編碼), []),
        } for 字頭 in d編碼2字頭們.get(編碼, [])
    ]

def _讀取資料():
    '''
    TODO: documentation
    '''
    with open(path.join(HERE, 'rhyme_book.csv'), encoding='utf-8') as f:
        next(f) # skip header
        for line in f:
            資料名稱, 小韻號, 韻部原貌, 最簡描述, 反切覈校前, 反切, 字頭覈校前, 字頭, 釋義, 釋義補充, 圖片id = line.rstrip('\n').split(',') # pylint: disable=unused-variable

            if 反切 == '': 反切 = 反切覈校前
            if 字頭 == '': 字頭 = 字頭覈校前

            縮略圖 = 生成書影(資料名稱, 圖片id, 縮略圖=False)
            書影 = 生成書影(資料名稱, 圖片id)

            編碼 = 音韻地位.from描述(最簡描述).編碼

            d字頭2編碼們[字頭][編碼] = None
            d編碼2字頭們[編碼][字頭] = None
            d字頭_編碼2韻書出處們[字頭, 編碼].append({
                '資料名稱': 資料名稱,
                '韻部原貌': 韻部原貌,
                '反切': 反切,
                '釋義': 釋義,
                '釋義補充': 釋義補充,
                '縮略圖': 縮略圖,
                '書影': 書影,
            })
            d資料名稱_小韻號_編碼2字頭們[資料名稱, 小韻號, 編碼][字頭] = None

            if 資料名稱 == '廣韻':
                d編碼2廣韻字頭們[編碼][字頭] = None

_讀取資料()
