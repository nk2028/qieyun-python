from os import path
from urllib.request import urlretrieve

here = path.abspath(path.dirname(__file__))
target = path.join(here, 'src/Qieyun/qieyun.csv')

if not path.exists(target):
    urlretrieve('https://raw.githubusercontent.com/nk2028/qieyun-data/f187326f1178fe68165f67507b75c53f4d38dc41/data.csv', target)
