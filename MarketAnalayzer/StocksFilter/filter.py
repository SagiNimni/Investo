from MarketAnalayzer.StocksFilter.DataExtractor import Extractor
from MarketAnalayzer.StocksFilter.constants import BasicMarketConstants as Constants
from MarketAnalayzer.StocksFilter.DataAnalyzer import *


def choose_stocks(file_name, years_back, amount_of_stocks=1000, extract_market_cap='all', sectors=None, extract=True,
                  extraction_speed='fast', logs=True):

    if extract:
        if extraction_speed == 'fast':
            batch_size = int(amount_of_stocks / 10)
        elif extraction_speed == 'medium':
            batch_size = int(amount_of_stocks / 7)
        elif extraction_speed == 'slow':
            batch_size = int(amount_of_stocks / 5)
        else:
            raise AttributeError(f"Extraction speed attribute {extraction_speed} couldn't be resolved! ")

        if extract_market_cap == 'all':
            min_market_cap = Constants.ALL_CAPS[0]
            max_market_cap = Constants.ALL_CAPS[1]
        elif extract_market_cap == 'small':
            min_market_cap = Constants.SMALL_CAPS[0]
            max_market_cap = Constants.SMALL_CAPS[1]
        elif extract_market_cap == 'medium':
            min_market_cap = Constants.MEDIUM_CAPS[0]
            max_market_cap = Constants.MEDIUM_CAPS[1]
        elif extract_market_cap == 'large':
            min_market_cap = Constants.LARGE_CAPS[0]
            max_market_cap = Constants.LARGE_CAPS[1]
        else:
            raise AttributeError(f"Market cap attribute {extract_market_cap} couldn't be resolved! ")

        extractor = Extractor(min_market_cap, max_market_cap, Constants.MINIMUM_VOLUME, Constants.MAXIMUM_VOLUME,
                              Constants.MINIMUM_PRICE, Constants.MAXIMUM_PRICE, sectors=sectors, limit=amount_of_stocks)

        extractor.extract(years_back, batch_size=batch_size, warnings=logs)
        extractor.save(file_name)

    data = Extractor.load(file_name)
    execute_analyze(data, max_years=years_back, plot_result=logs, save=f'{file_name}.xlsx')
