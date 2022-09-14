from MarketAnalyzer.StocksFilter.DataExtractor import Extractor
from MarketAnalyzer.StocksFilter.constants import *


# TODO add threading that runs the two function together
def choose_stocks(sectors=None):

    extractor = Extractor(10, ALL_CAPS[0], ALL_CAPS[1], MINIMUM_VOLUME, MAXIMUM_VOLIME, MINIMUM_PRICE, MAXIMUM_PRICE,
                          sectors=sectors, limit=10)
    stocks = extractor.execute_analyze()
    print(stocks)


if __name__ == '__main__':
    choose_stocks()
