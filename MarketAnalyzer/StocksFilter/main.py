from MarketAnalyzer.StocksFilter.DataExtractor import Extractor
from MarketAnalyzer.StocksFilter.constants import *
from MarketAnalyzer.StocksFilter.DataAnalyzer import *


def choose_stocks(sectors=None):

    extractor = Extractor(ALL_CAPS[0], ALL_CAPS[1], MINIMUM_VOLUME, MAXIMUM_VOLIME, MINIMUM_PRICE, MAXIMUM_PRICE,
                          sectors=sectors, limit=1000)
    extractor.extract(10, batch_size=100, warnings=True)
    extractor.save('stocks')
    data = Extractor.load('stocks')
    result = execute_analyze(data)
    print(result)


if __name__ == '__main__':
    choose_stocks()
