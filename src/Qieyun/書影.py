# -*- coding: utf-8 -*-

import re

def 生成縮略圖(資料名稱, 圖片id):
    '''
    Test
    '''
    if 資料名稱 == '廣韻':
        match = re.fullmatch(r'([^0-9]+)([0-9]+)([^0-9]+)', 圖片id)
        volume = ['上平', '下平', '上', '去', '入'].index(match[1]) + 1
        page = int(match[2]) + [8, 2, 2, 4, 3][volume - 1]
        position = match[3] # pylint: disable=unused-variable
        return f'https://cdn.jsdelivr.net/gh/nk2028/kuankhiunn@main/volume{volume}/thumb/p{page:03}.jpg'
    if 資料名稱 == 'p2011':
        page = int(圖片id)
        return f'https://cdn.jsdelivr.net/gh/nk2028/hvanghiunn@main/p2011/thumb/{page:04}.jpg'
    raise RuntimeError

def 生成書影(資料名稱, 圖片id):
    '''
    Test
    '''
    if 資料名稱 == '廣韻':
        match = re.fullmatch(r'([^0-9]+)([0-9]+)([^0-9]+)', 圖片id)
        volume = ['上平', '下平', '上', '去', '入'].index(match[1]) + 1
        page = int(match[2]) + [8, 2, 2, 4, 3][volume - 1]
        position = match[3] # pylint: disable=unused-variable
        return f'https://cdn.jsdelivr.net/gh/nk2028/kuankhiunn@main/volume{volume}/p{page:03}.jpg'
    if 資料名稱 == 'p2011':
        page = int(圖片id)
        return f'https://cdn.jsdelivr.net/gh/nk2028/hvanghiunn@main/p2011/{page:04}.jpg'
    raise RuntimeError
