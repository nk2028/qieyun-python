# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple
from os import path
from typing import Optional

from .音韻地位 import 音韻地位
from .書影 import 生成書影

from .韻圖資料 import d廣韻小韻號2韻圖出處

HERE = path.abspath(path.dirname(__file__))

d字頭2編碼們 = defaultdict(dict)
d編碼2字頭們 = defaultdict(dict)
d字頭_編碼2出處們 = defaultdict(list)

def query字頭(字頭: str):
    '''
    由字頭查出相應的音韻地位和解釋。
    '''
    編碼們 = d字頭2編碼們.get(字頭)
    return [] if 編碼們 is None else [
        {
            '音韻地位': 音韻地位.from編碼(編碼),
            '出處': d字頭_編碼2出處們[字頭, 編碼],
        } for 編碼 in 編碼們
    ]

def iter音韻地位():
    '''所有至少對應一個字頭的音韻地位。'''
    for 編碼 in d編碼2字頭們:
        yield 音韻地位.from編碼(編碼)

def get代表字(當前音韻地位) -> Optional[str]:
    '''
    代表字。
    '''
    編碼 = 當前音韻地位.編碼
    字頭們 = d編碼2字頭們.get(編碼)
    if 字頭們 is None:
        return None
    return next(iter(字頭們)) # TODO: 優先選擇廣韻字頭

def get條目(當前音韻地位):
    '''
    條目。
    '''
    編碼 = 當前音韻地位.編碼
    字頭們 = d編碼2字頭們.get(編碼)
    return [
        (
            字頭,
            d字頭_編碼2出處們[字頭, 編碼], # 出處們
        ) for 字頭 in 字頭們
    ]

def 讀取資料(): # TODO: Fix documentation
    '''
    Test
    '''
    with open(path.join(HERE, 'qieyun.csv'), encoding='utf-8') as f:
        next(f) # skip header
        for line in f:
            資料名稱, 小韻號, 韻部原貌, 最簡描述, 反切覈校前, 反切, 字頭覈校前, 字頭, 釋義, 釋義補充, 圖片id = line.rstrip('\n').split(',')

            if 反切 == '': 反切 = 反切覈校前
            if 字頭 == '': 字頭 = 字頭覈校前

            縮略圖 = 生成書影(資料名稱, 圖片id, 縮略圖=False)
            書影 = 生成書影(資料名稱, 圖片id)

            編碼 = 音韻地位.from描述(最簡描述).編碼

            d字頭2編碼們[字頭][編碼] = None
            d編碼2字頭們[編碼][字頭] = None
            d字頭_編碼2出處們[字頭, 編碼].append({
                '資料類型': '韻書',
                '資料名稱': 資料名稱,
                '韻部原貌': 韻部原貌,
                '反切': 反切,
                '釋義': 釋義,
                '釋義補充': 釋義補充,
                '縮略圖': 縮略圖,
                '書影': 書影,
            })

            if 資料名稱 == '廣韻':
                韻圖出處 = d廣韻小韻號2韻圖出處.get(小韻號)
                if 韻圖出處 is not None:
                    d字頭_編碼2出處們[字頭, 編碼].append(韻圖出處)

讀取資料()
