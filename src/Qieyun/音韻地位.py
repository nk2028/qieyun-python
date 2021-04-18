# -*- coding: utf-8 -*-

from collections import defaultdict, namedtuple
from os import path
import re
from typing import List, Optional

from .拓展音韻屬性 import 母到清濁, 母到音, 母到組, 韻到攝
from .書影 import 生成縮略圖, 生成書影

HERE = path.abspath(path.dirname(__file__))

# 常量

編碼表 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

所有母 = '幫滂並明端透定泥來知徹澄孃精清從心邪莊初崇生俟章昌常書船日見溪羣疑影曉匣云以'
所有呼 = '開合'
所有等 = '一二三四'
所有重紐 = 'AB'
所有韻 = '東冬鍾江支脂之微魚虞模齊祭泰佳皆夬灰咍廢眞臻文欣元魂痕寒刪山仙先蕭宵肴豪歌麻陽唐庚耕清青蒸登尤侯幽侵覃談鹽添咸銜嚴凡'
所有聲 = '平上去入'

重紐母 = '幫滂並明見溪羣疑影曉'
重紐韻 = '支脂祭眞仙宵清侵鹽'

開合皆有的韻 = '支脂微齊祭泰佳皆夬廢眞元寒刪山仙先歌麻陽唐庚耕清青蒸登'
必為開口的韻 = '咍痕欣嚴之魚臻蕭宵肴豪侯侵覃談鹽添咸銜'
必為合口的韻 = '灰魂文凡'
開合中立的韻 = '東冬鍾江虞模尤幽'

韻順序表 = '東_冬鍾江支脂之微魚虞模齊祭泰佳皆夬灰咍廢眞臻文欣元魂痕寒刪山仙先蕭宵肴豪歌_麻_陽唐庚_耕清青蒸登尤侯幽侵覃談鹽添咸銜嚴凡'

一等韻 = '冬模泰咍灰痕魂寒豪唐登侯覃談'
二等韻 = '江佳皆夬刪山肴耕咸銜'
三等韻 = '鍾支脂之微魚虞祭廢眞臻欣元文仙宵陽清蒸尤幽侵鹽嚴凡'
四等韻 = '齊先蕭青添'
一三等韻 = '東歌'
二三等韻 = '麻庚'

解析音韻描述 = re.compile('([%s])([%s]?)([%s]?)([%s]?)([%s])([%s])' % (所有母, 所有呼, 所有等, 所有重紐, 所有韻, 所有聲))

# 底層資料結構

條目 = namedtuple('條目', ['音韻地位', '出處'])
出處 = namedtuple('出處', ['資料名稱', '韻部原貌', '反切', '釋義', '釋義補充', '縮略圖', '書影'])

# 「音韻地位」物件

class 音韻地位:
    '''《切韻》音系音韻地位。'''

    def __init__(self, 母, 呼, 等, 重紐, 韻, 聲):
        音韻地位.驗證(母, 呼, 等, 重紐, 韻, 聲)

        self.母 = 母
        self.呼 = 呼
        self.等 = 等
        self.重紐 = 重紐
        self.韻 = 韻
        self.聲 = 聲

    @property
    def 清濁(self) -> str:
        '''
        清濁（全清、次清、全濁、次濁）。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').清濁
        '全清'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').清濁
        '全濁'
        ```
        '''
        return 母到清濁[self.母]

    @property
    def 音(self) -> str:
        '''
        音（脣音、舌音、齒音、牙音、喉音）。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').音
        '脣'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').音
        '牙'
        ```
        '''
        return 母到音[self.母]

    @property
    def 組(self) -> Optional[str]:
        '''
        組。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').組
        '幫'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').組
        '見'
        ```
        '''
        return 母到組[self.母]

    @property
    def 攝(self) -> str:
        '''
        攝。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').攝
        '咸'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').攝
        '止'
        ```
        '''
        return 韻到攝[self.韻]

    @property
    def 描述(self) -> str:
        '''
        音韻描述。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').描述
        '幫三凡入'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').描述
        '羣開三A支平'
        ```
        '''
        母 = self.母
        呼 = self.呼
        等 = self.等
        重紐 = self.重紐
        韻 = self.韻
        聲 = self.聲

        return 母 + (呼 or '') + 等 + (重紐 or '') + 韻 + 聲

    @property
    def 最簡描述(self) -> str:
        '''
        最簡音韻描述。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').最簡描述
        '幫凡入'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').最簡描述
        '羣開A支平'
        ```
        '''
        母 = self.母
        呼 = self.呼
        等 = self.等
        重紐 = self.重紐
        韻 = self.韻
        聲 = self.聲

        if 韻 not in 開合皆有的韻:
            呼 = None
        if 韻 not in 一三等韻 and 韻 not in 二三等韻:
            等 = None

        return 母 + (呼 or '') + (等 or '') + (重紐 or '') + 韻 + 聲

    @property
    def 表達式(self) -> str:
        '''
        音韻表達式。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').表達式
        '幫母 三等 凡韻 入聲'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').表達式
        '羣母 開口 三等 重紐A類 支韻 平聲'
        ```
        '''
        母 = self.母
        呼 = self.呼
        等 = self.等
        重紐 = self.重紐
        韻 = self.韻
        聲 = self.聲

        呼字段 = f'{呼}口 ' if 呼 else ''
        重紐字段 = f'重紐{重紐}類 ' if 重紐 else ''

        return f'{母}母 {呼字段}{等}等 {重紐字段}{韻}韻 {聲}聲'

    @property
    def 最簡表達式(self) -> str:
        '''
        最簡音韻表達式。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').最簡表達式
        '幫母 凡韻 入聲'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').最簡表達式
        '羣母 開口 重紐A類 支韻 平聲'
        ```
        '''
        母 = self.母
        呼 = self.呼
        等 = self.等
        重紐 = self.重紐
        韻 = self.韻
        聲 = self.聲

        if 韻 not in 開合皆有的韻:
            呼 = None
        if 韻 not in 一三等韻 and 韻 not in 二三等韻:
            等 = None

        呼字段 = f'{呼}口 ' if 呼 else ''
        等字段 = f'{等}等 ' if 等 else ''
        重紐字段 = f'重紐{重紐}類 ' if 重紐 else ''
        韻字段 = f'{韻}韻 ' if 韻 else ''

        return f'{母}母 {呼字段}{等字段}{重紐字段}{韻字段}{聲}聲'

    @property
    def 編碼(self) -> str:
        '''
        音韻編碼。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').編碼
        'A9D'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').編碼
        'fFA'
        ```
        '''
        母 = self.母
        呼 = self.呼
        等 = self.等
        重紐 = self.重紐
        韻 = self.韻
        聲 = self.聲

        母編碼 = 所有母.index(母)

        韻編碼 = {
            '東三': 1,
            '歌三': 38,
            '麻三': 40,
            '庚三': 44,
        }.get(韻 + 等) or 韻順序表.index(韻)

        其他編碼 = ((呼 == '合') << 3) + ((重紐 == 'B') << 2) + 所有聲.index(聲)

        return 編碼表[母編碼] + 編碼表[韻編碼] + 編碼表[其他編碼]

    @property
    def 代表字(self) -> Optional[str]:
        '''
        代表字。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').代表字
        '法'
        >>> Qieyun.音韻地位.from描述('羣開三A支平').代表字
        '祇'
        ```
        '''
        編碼 = self.編碼
        字頭們 = d編碼2字頭們.get(編碼)
        if 字頭們 is None:
            return None
        return next(iter(字頭們)) # TODO: 優先選擇廣韻字頭

    @property
    def 條目(self):
        '''
        條目。

        ```python
        >>> Qieyun.音韻地位.from描述('影開二銜去').條目
        [('𪒠', '叫呼仿佛𪒠然自得音黯去聲一')]
        >>> Qieyun.音韻地位.from描述('常開三麻去').條目
        []
        ```
        '''
        編碼 = self.編碼
        字頭們 = d編碼2字頭們.get(編碼)
        return [
            (
                字頭,
                d字頭_編碼2出處們[字頭, 編碼], # 出處們
            ) for 字頭 in 字頭們
        ]

    def 屬於(self, s: str) -> bool:
        '''
        判斷音韻地位是否符合給定的音韻表達式。

        ```python
        >>> Qieyun.音韻地位.from描述('幫三凡入').屬於('章母')
        False
        >>> Qieyun.音韻地位.from描述('幫三凡入').屬於('一四等')
        False
        >>> Qieyun.音韻地位.from描述('幫三凡入').屬於('幫組 或 陽韻')
        True
        ```
        '''
        def inner(q: str):
            if q.endswith('母'):
                母們 = q[:-1]
                assert len(母們) > 0, '未指定母'
                for 母 in 母們:
                    assert 母 in 所有母, 母 + '母不存在'
                return self.母 in 母們

            if q.endswith('等'):
                等們 = q[:-1]
                assert len(等們) > 0, '未指定等'
                for 等 in 等們:
                    assert 等 in '一二三四', 等 + '等不存在'
                return self.等 in 等們

            if q.endswith('韻'):
                韻們 = q[:-1]
                assert len(韻們) > 0, '未指定韻'
                for 韻 in 韻們:
                    assert 韻 in 所有韻, 韻 + '韻不存在'
                return self.韻 in 韻們

            if q.endswith('聲'):
                聲們 = q[:-1]
                assert len(聲們) > 0, '未指定聲'
                def equal聲(聲: str) -> bool:
                    if 聲 in '平上去入': return self.聲 == 聲
                    if 聲 == '仄': return self.聲 != '平'
                    if 聲 == '舒': return self.聲 != '入'
                    raise AssertionError(聲 + '聲不存在')
                return any(equal聲(聲) for 聲 in 聲們)

            if q.endswith('組'):
                組們 = q[:-1]
                assert len(組們) > 0, '未指定組'
                # TODO: 所有組
                # for 組 in 組們:
                #     assert 組 in 所有組, 組 + '組不存在'
                return self.組 is not None and self.組 in 組們

            if q.endswith('音'):
                音們 = q[:-1]
                assert len(音們) > 0, '未指定音'
                for 音 in 音們:
                    assert 音 in '脣舌牙齒喉', 音 + '音不存在'
                return self.音 in 音們

            if q.endswith('攝'):
                攝們 = q[:-1]
                assert len(攝們) > 0, '未指定攝'
                # TODO: 所有攝
                # for 攝 in 攝們:
                #     assert 攝 in 所有攝, 攝 + '攝不存在'
                return self.攝 in 攝們

            if q == '開口': return self.呼 == '開'
            if q == '合口': return self.呼 == '合'
            if q == '開合中立': return self.呼 is None
            if q == '重紐A類': return self.重紐 == 'A'
            if q == '重紐B類': return self.重紐 == 'B'
            if q == '全清': return self.清濁 == '全清'
            if q == '次清': return self.清濁 == '次清'
            if q == '全濁': return self.清濁 == '全濁'
            if q == '次濁': return self.清濁 == '次濁'

            raise AssertionError('無此運算符：' + q)

        return any(all(inner(q) for q in p.split(' ')) for p in s.split(' 或 '))

    def __eq__(self, that):
        if not isinstance(that, 音韻地位):
            return False
        return self.描述 == that.描述

    @staticmethod
    def 驗證(母: str, 呼: Optional[str], 等: str, 重紐: Optional[str], 韻: str, 聲: str):
        '''
        驗證給定的音韻地位六要素是否合法。
        '''
        assert len(母) == 1 and 母 in 所有母, 'Unexpected 母: ' + repr(母)
        assert len(等) == 1 and 等 in 所有等, 'Unexpected 等: ' + repr(等)
        assert len(韻) == 1 and 韻 in 所有韻, 'Unexpected 韻: ' + repr(韻)
        assert len(聲) == 1 and 聲 in 所有聲, 'Unexpected 聲: ' + repr(聲)

        if 母 in '幫滂並明' or 韻 in 開合中立的韻:
            assert 呼 is None, 'Unexpected 呼: ' + repr(呼)
        elif 韻 in 必為開口的韻:
            assert 呼 == '開'
        elif 韻 in 必為合口的韻:
            assert 呼 == '合'
        else:
            assert 呼 is not None and len(呼) == 1 and 呼 in 所有呼, 'Unexpected 呼: ' + repr(呼)

        if 母 in 重紐母 and 韻 in 重紐韻:
            assert 重紐 is not None and len(重紐) == 1 and 重紐 in 所有重紐, 'Unexpected 重紐: ' + repr(重紐)
        else:
            assert 重紐 is None, 'Unexpected 重紐: ' + repr(重紐)

        if 韻 in 一等韻:
            assert 等 == '一', 'Unexpected 等: ' + repr(等)
        elif 韻 in 二等韻:
            assert 等 == '二', 'Unexpected 等: ' + repr(等)
        elif 韻 in 三等韻:
            assert 等 == '三', 'Unexpected 等: ' + repr(等)
        elif 韻 in 四等韻:
            assert 等 == '四', 'Unexpected 等: ' + repr(等)
        elif 韻 in 一三等韻:
            assert 等 in ('一', '三'), 'Unexpected 等: ' + repr(等)
        elif 韻 in 二三等韻:
            assert 等 in ('二', '三'), 'Unexpected 等: ' + repr(等)

    @staticmethod
    def from編碼(s: str):
        '''
        將音韻編碼轉換為音韻地位。
        '''
        assert len(s) == 3, 'Invalid 編碼: ' + repr(s)

        母編碼 = 編碼表.index(s[0])
        韻編碼 = 編碼表.index(s[1])
        其他編碼 = 編碼表.index(s[2])

        呼編碼 = 其他編碼 >> 3
        重紐編碼 = (其他編碼 >> 2) & 0b1
        聲編碼 = 其他編碼 & 0b11

        母 = 所有母[母編碼]
        呼 = 所有呼[呼編碼]
        重紐 = 所有重紐[重紐編碼]
        聲 = 所有聲[聲編碼]

        if 韻編碼 == 0:
            韻 = '東'; 等 = '一'
        elif 韻編碼 == 1:
            韻 = '東'; 等 = '三'
        elif 韻編碼 == 37:
            韻 = '歌'; 等 = '一'
        elif 韻編碼 == 38:
            韻 = '歌'; 等 = '三'
        elif 韻編碼 == 39:
            韻 = '麻'; 等 = '二'
        elif 韻編碼 == 40:
            韻 = '麻'; 等 = '三'
        elif 韻編碼 == 43:
            韻 = '庚'; 等 = '二'
        elif 韻編碼 == 44:
            韻 = '庚'; 等 = '三'
        else:
            韻 = 韻順序表[韻編碼]
            if 韻 in 一等韻:
                等 = '一'
            elif 韻 in 二等韻:
                等 = '二'
            elif 韻 in 三等韻:
                等 = '三'
            elif 韻 in 四等韻:
                等 = '四'

        if 母 in '幫滂並明' or 韻 in 開合中立的韻:
            assert 呼 == '開'
            呼 = None

        if 母 not in 重紐母 or 韻 not in 重紐韻:
            assert 重紐 == 'A'
            重紐 = None

        音韻地位.驗證(母, 呼, 等, 重紐, 韻, 聲)

        return 音韻地位(母, 呼, 等, 重紐, 韻, 聲)

    @staticmethod
    def from描述(描述: str):
        '''
        將音韻描述或最簡音韻描述轉換為音韻地位。
        '''
        # TODO: 重寫解析器，支援更多格式

        match = 解析音韻描述.fullmatch(描述)
        assert match is not None

        母 = match.group(1)
        呼 = match.group(2) or None
        等 = match.group(3) or None
        重紐 = match.group(4) or None
        韻 = match.group(5)
        聲 = match.group(6)

        if 呼 is None and 母 not in '幫滂並明':
            if 韻 in 必為開口的韻: 呼 = '開'
            elif 韻 in 必為合口的韻: 呼 = '合'

        if 等 is None:
            if 韻 in 一等韻: 等 = '一'
            elif 韻 in 二等韻: 等 = '二'
            elif 韻 in 三等韻: 等 = '三'
            elif 韻 in 四等韻: 等 = '四'

        音韻地位.驗證(母, 呼, 等, 重紐, 韻, 聲)

        return 音韻地位(母, 呼, 等, 重紐, 韻, 聲)

    def __repr__(self):
        return '<音韻地位 ' + self.描述 + '>'

def query字頭(字頭: str) -> List[條目]: # TODO: Fix typing
    '''
    由字頭查出相應的音韻地位和解釋。

    ```python
    >>> Qieyun.query字頭('結') # TODO: Update to new format
    [(<音韻地位 見開四先入>, '締也古屑切十五')]
    >>> Qieyun.query字頭('冷')
    [
      (<音韻地位 來開四青平>, '冷凙吳人云冰凌又力頂切'),
      (<音韻地位 來開二庚上>, '寒也魯打切又魯頂切一'),
      (<音韻地位 來開四青上>, '寒也又姓前趙錄有徐州刺史冷道字安義又盧打切')],
    ]
    ```
    '''
    編碼們 = d字頭2編碼們.get(字頭)
    return [] if 編碼們 is None else [
        條目(
            音韻地位=音韻地位.from編碼(編碼),
            出處=d字頭_編碼2出處們[字頭, 編碼],
        ) for 編碼 in 編碼們
    ]

def iter音韻地位():
    '''所有至少對應一個字頭的音韻地位。'''
    for 編碼 in d編碼2字頭們:
        yield 音韻地位.from編碼(編碼)

# 載入資料

d字頭2編碼們 = defaultdict(dict)
d編碼2字頭們 = defaultdict(dict)
d字頭_編碼2出處們 = defaultdict(list)

def 讀取資料(): # TODO: Fix documentation
    '''
    Test
    '''
    with open(path.join(HERE, 'qieyun.csv'), encoding='utf-8') as f:
        next(f) # skip header
        for line in f:
            資料名稱, _, 韻部原貌, 最簡描述, 反切覈校前, 反切, 字頭覈校前, 字頭, 釋義, 釋義補充, 圖片id = line.rstrip('\n').split(',')

            if 反切 == '': 反切 = 反切覈校前
            if 字頭 == '': 字頭 = 字頭覈校前

            縮略圖 = 生成縮略圖(資料名稱, 圖片id)
            書影 = 生成書影(資料名稱, 圖片id)

            編碼 = 音韻地位.from描述(最簡描述).編碼

            d字頭2編碼們[字頭][編碼] = None
            d編碼2字頭們[編碼][字頭] = None
            d字頭_編碼2出處們[字頭, 編碼].append(出處(資料名稱, 韻部原貌, 反切, 釋義, 釋義補充, 縮略圖, 書影))

讀取資料()

# TODO: Add dpc tests
