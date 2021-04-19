# -*- coding: utf-8 -*-

'''
早期韻圖資料上的操作。
'''

from collections import defaultdict
import networkx as nx
from os import path

from .音韻地位 import 音韻地位
from ._書影 import 生成書影
from .韻書 import d資料名稱_小韻號_編碼2字頭們

HERE = path.abspath(path.dirname(__file__))

d編碼2字頭圖 = defaultdict(nx.Graph)
d編碼2韻圖出處們 = defaultdict(list)

for (資料名稱, 小韻號, 編碼), 字頭們 in d資料名稱_小韻號_編碼2字頭們.items():
    字頭圖 = d編碼2字頭圖[編碼]
    if len(字頭們) == 1:
        字頭圖.add_node(next(iter(字頭們)))
    else:
        xs = list(字頭們)
        小韻首字 = xs[0]
        for 字頭 in xs[1:]:
            字頭圖.add_edge(小韻首字, 字頭)

def _字頭_音韻地位2韻圖出處們(字頭, 當前音韻地位):
    '''
    獲取字頭與音韻地位對應的所有韻圖出處。
    '''
    編碼 = 當前音韻地位.編碼
    def inner():
        for 韻圖出處 in d編碼2韻圖出處們.get(編碼, []):
            對應韻圖字頭 = 韻圖出處['對應韻圖字頭']
            字頭圖 = d編碼2字頭圖[編碼]
            if 對應韻圖字頭 == 字頭 or 對應韻圖字頭 in nx.algorithms.descendants(字頭圖, 字頭):
                yield 韻圖出處
    return list(inner())

def _讀取資料():
    '''
    讀取韻書與韻圖資料，將韻書的小韻對應到韻圖等字頭。
    此函式執行後，結果將存儲於 `d廣韻小韻號2韻圖出處` 中。
    '''
    with open(path.join(HERE, 'rhyme_table.csv'), encoding='utf-8') as f:
        next(f) # skip header
        for line in f:
            資料名稱, 小韻號, 字頭, 轉號, 韻圖韻, 韻圖母位置, 韻圖母, 韻圖等, 音韻描述 = line.rstrip('\n').split(',') # pylint: disable=unused-variable

            當前音韻地位 = 音韻地位.from描述(音韻描述)
            編碼 = 當前音韻地位.編碼

            縮略圖 = 生成書影(資料名稱, 轉號, 縮略圖=True)
            書影 = 生成書影(資料名稱, 轉號)

            d編碼2韻圖出處們[編碼].append({
                '資料名稱': 資料名稱,
                '韻圖韻': 韻圖韻,
                '韻圖母位置': 韻圖母位置,
                '韻圖母': 韻圖母,
                '韻圖等': 韻圖等,
                '韻圖聲': 當前音韻地位.聲,
                '對應韻圖字頭': 字頭,
                '縮略圖': 縮略圖,
                '書影': 書影,
            })

_讀取資料()
