from MarketAnalyzer.StocksFilter.DataExtractor import Extractor, list_symbols
from MarketAnalyzer.StocksFilter.constants import *


def choose_stocks(sectors=None, market_cap=None):

    list_symbols(r'.\checklist')

    extractor = Extractor(5, r'.\checklist')

    if market_cap is None:
        stocks = extractor.filter(ALL_CAPS[0], ALL_CAPS[1], MINIMUM_VOLUME, MINIMUM_PRICE, MAXIMUM_PRICE, sectors=sectors)
    elif market_cap == 'small':
        stocks = extractor.filter(SMALL_CAPS[0], SMALL_CAPS[1], MINIMUM_VOLUME, MINIMUM_PRICE, MAXIMUM_PRICE, sectors=sectors)
    elif market_cap == 'medium':
        stocks = extractor.filter(MEDIUM_CAPS[0], MEDIUM_CAPS[1], MINIMUM_VOLUME, MAXIMUM_PRICE, MAXIMUM_PRICE, sectors=sectors)
    elif market_cap == 'large':
        stocks = extractor.filter(LARGE_CAPS[0], LARGE_CAPS[1], MINIMUM_VOLUME, MAXIMUM_PRICE, MAXIMUM_PRICE, sectors=sectors)
    else:
        raise ValueError("The market cap parameter provided is wrong")

    for ratios in stocks.values():
        # ratios.liquidity_test()
        # ratios.leverage_test()
        # ratios.efficiency_test()
        # ratios.profitability_test()
        # ratios.market_value_test()
        result = ratios.growth_rate_test()
        print(result)


if __name__ == '__main__':
    choose_stocks()
