from .韻書 import 字頭2音韻地位_韻書出處們
from .韻圖 import 字頭_音韻地位2韻圖出處們

def 字頭2音韻地位_出處們(字頭):
    def inner():
        for 條目 in 字頭2音韻地位_韻書出處們(字頭):
            音韻地位 = 條目['音韻地位']
            韻書出處們 = 條目['韻書出處們']
            韻圖出處們 = 字頭_音韻地位2韻圖出處們(字頭, 音韻地位)
            yield {
                '音韻地位': 音韻地位,
                '韻書出處們': 韻書出處們,
                '韻圖出處們': 韻圖出處們,
            }
    return list(inner())
