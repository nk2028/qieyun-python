from os import path
from urllib.request import urlretrieve

here = path.abspath(path.dirname(__file__))
url = 'https://raw.githubusercontent.com/nk2028/qieyun-data/8bbd239/'

def retrieve(filename):
    target = path.join(here, 'src/Qieyun', filename)
    if not path.exists(target):
        urlretrieve(url + filename, target)

retrieve('rhyme_book.csv')
retrieve('rhyme_table.csv')
