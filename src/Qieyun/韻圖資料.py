# -*- coding: utf-8 -*-

from collections import defaultdict
from os import path

from .音韻地位 import 音韻地位
from .書影 import 生成書影

HERE = path.abspath(path.dirname(__file__))

d編碼2廣韻小韻號 = defaultdict(dict)
d廣韻小韻號2字頭們 = defaultdict(dict)

d廣韻小韻號2韻圖出處 = {}

def 讀取資料():
    '''
    讀取韻書與韻圖資料，將韻書的小韻對應到韻圖等字頭。
    此函式執行後，結果將存儲於 `d廣韻小韻號2韻圖出處` 中。
    '''
    with open(path.join(HERE, 'qieyun.csv'), encoding='utf-8') as f:
        next(f) # skip header
        for line in f:
            資料名稱, 小韻號, 韻部原貌, 最簡描述, 反切覈校前, 反切, 字頭覈校前, 字頭, 釋義, 釋義補充, 圖片id = line.rstrip('\n').split(',') # pylint: disable=unused-variable

            if 反切 == '': 反切 = 反切覈校前
            if 字頭 == '': 字頭 = 字頭覈校前

            編碼 = 音韻地位.from描述(最簡描述).編碼

            if 資料名稱 == '廣韻':
                d編碼2廣韻小韻號[編碼][小韻號] = None
                d廣韻小韻號2字頭們[小韻號][字頭] = None

    with open(path.join(HERE, 'hiunndu.csv'), encoding='utf-8') as f:
        next(f) # skip header
        for line in f:
            小韻號, 字頭, 轉號, 韻圖韻, 韻圖母位置, 韻圖等, 韻圖母, 音韻描述 = line.rstrip('\n').split(',') # pylint: disable=unused-variable

            當前音韻地位 = 音韻地位.from描述(音韻描述)

            對應小韻號們 = d編碼2廣韻小韻號.get(當前音韻地位.編碼, ())
            for 對應小韻號 in 對應小韻號們:
                對應字頭們 = d廣韻小韻號2字頭們[對應小韻號]
                if 字頭 in 對應字頭們:
                    縮略圖 = 生成書影('韻鏡（永祿本）', 轉號, 縮略圖=True)
                    書影 = 生成書影('韻鏡（永祿本）', 轉號)

                    d廣韻小韻號2韻圖出處[對應小韻號] = {
                        '資料類型': '韻圖',
                        '資料名稱': '韻鏡（永祿本）',
                        '韻圖韻': 韻圖韻,
                        '韻圖母位置': 韻圖母位置,
                        '韻圖母': 韻圖母,
                        '韻圖等': 韻圖等,
                        '韻圖聲': 當前音韻地位.聲,
                        '對應廣韻小韻首字': next(iter(對應字頭們)),
                        '對應韻圖字頭': 字頭,
                        '縮略圖': 縮略圖,
                        '書影': 書影,
                    }

讀取資料()
