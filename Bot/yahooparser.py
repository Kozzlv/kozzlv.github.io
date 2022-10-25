import requests
from dpath.util import values as path_val
class Ticker:
    session = requests.session()
    headers = 'Mozilla/5.0 ' \
              '(Windows NT 10.0; WOW64) ' \
              'AppleWebKit/537.36' \
              ' (KHTML, like Gecko) ' \
              'Chrome/91.0.4472.135 ' \
              'Safari/537.36'
    value = {'price': 'regularMarketPrice',
             'percent': 'regularMarketChangePercent',
             'change': 'regularMarketChange',
             'volume': 'regularMarketVolume'}
    def __init__(self, name):
        self.name = name
        self.price = 0.00
        self.change = 0.00
        self.percent = 0.0
        self.volume = 0.0
    def update(self):
        self.price, self.percent, self.change, self.volume = self.__get_update()
    def __get_update(self):
        link = f"https://query2.finance.yahoo.com/v10/" \
               f"finance/quoteSummary/{self.name}?modules=price"
        response = self.session.get(link, headers={'User-Agent': self.headers})
        array = response.json()
        return_value = []
        for key in self.value:
            return_value.append(float(path_val(array, f"/**/{self.value[key]}/raw")[0]))
        return return_value