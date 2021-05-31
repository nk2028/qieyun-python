# -*- coding: utf-8 -*-

import re


def 生成書影(資料名稱, 圖片id, 縮略圖=False):
    '''
    Test
    '''

    縮略圖 = 'thumb/' if 縮略圖 else ''

    if 資料名稱 == '王一':
        page = int(圖片id)
        return f'https://cethiunn-1305783649.cos.ap-guangzhou.myqcloud.com/P2011/{縮略圖}{page:04}.jpg'

    if 資料名稱 == '廣韻':
        match = re.fullmatch(r'([^0-9]+)([0-9]+)([^0-9]+)', 圖片id)
        volume = ['上平', '下平', '上', '去', '入'].index(match[1]) + 1
        # TODO FIXME: 此段程式碼對左右理解有誤
        page = int(match[2]) + [8, 2, 2, 4, 3][volume - 1]
        position = match[3]  # pylint: disable=unused-variable
        return f'https://kuankhiunn-1305783649.cos.ap-guangzhou.myqcloud.com/deakdzuondangpuoon/volume{volume}/{縮略圖}p{page:03}.jpg'

    if 資料名稱 == '指微韻鑑（嘉吉本）':
        page = int(圖片id)
        return f'https://hiunnkyanq-1305783649.cos.ap-guangzhou.myqcloud.com/keakitpuoon/{縮略圖}{page+14:02}.jpg'

    if 資料名稱 == '韻鏡（古逸叢書本）':
        page = int(圖片id)
        return f'https://hiunnkyanq-1305783649.cos.ap-guangzhou.myqcloud.com/kuujitdzungsjvpuoon/{縮略圖}{page+9:02}.png'

    raise NotImplementedError('未收錄指定書影')
