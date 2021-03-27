from os import path
from urllib.request import urlretrieve

here = path.abspath(path.dirname(__file__))
target = path.join(here, 'src/Qieyun/qieyun.csv')

if not path.exists(target):
    urlretrieve('https://raw.githubusercontent.com/nk2028/qieyun-data/9ee0dc6/data.csv', target)
