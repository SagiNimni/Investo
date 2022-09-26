from MarketAnalyzer.StocksFilter.DataExtractor import Extractor
from MarketAnalyzer.StocksFilter.constants import *
from MarketAnalyzer.StocksFilter.DataAnalyzer import *


def print_beautiful(data):
    for tup in data:
        print(tup[0] + ':\n', tup[1], '\n')


def choose_stocks(sectors=None):

    extractor = Extractor(ALL_CAPS[0], ALL_CAPS[1], MINIMUM_VOLUME, MAXIMUM_VOLUME, MINIMUM_PRICE, MAXIMUM_PRICE,
                          sectors=sectors, limit=1000)
    extractor.extract(10, batch_size=100, warnings=True)
    extractor.save('stocks')
    data = Extractor.load('stocks')
    result = execute_analyze(data)
    print_beautiful(result)


if __name__ == '__main__':
    choose_stocks()
