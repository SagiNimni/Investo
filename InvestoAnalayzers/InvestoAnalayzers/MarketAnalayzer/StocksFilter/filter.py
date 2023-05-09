from InvestoAnalayzers.MarketAnalayzer.StocksFilter.DataExtractor import Extractor
from InvestoAnalayzers.MarketAnalayzer.StocksFilter.constants import BasicMarketConstants as Constants
from InvestoAnalayzers.MarketAnalayzer.StocksFilter.constants import BENCHMARKS_FILE_NAME
from InvestoAnalayzers.MarketAnalayzer.StocksFilter.DataAnalyzer import *
import pandas as pd


def extract(file_name, years_back, amount_of_stocks=1000, extract_market_cap='all', sectors=None,
            extraction_speed='fast', logs=True):

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


def filter_by_growth(file_name, years_back, logs=True):
    data = Extractor.load(file_name)
    execute_growth_analyze(data, max_years=years_back, plot_result=logs, save=f'{file_name}.json')


def sort_by_ratio(file_path, ratio_to_filter, filter_type):

    if filter_type == 'industry':
        ascending = False
    elif filter_type == 'value':
        ascending = True
    else:
        raise ValueError("Wrong filter type, Please choose either 'industry' or 'value'.")

    ratios_types = ['liquidity', 'leverage', 'efficiency', 'profitability', 'value']
    if ratio_to_filter not in ratios_types:
        raise ValueError("Wrong ratio type, Please choose one of the exiting ratios")

    file_path = file_path.replace('\\', '/')
    stocks_grades = pd.read_json(file_path + '/' + file_path.rsplit('/', 1)[1] + '.json')
    filter_by_ratios_type(stocks_grades, ratio_to_filter, ascending=ascending, save=file_path + '/sorted.json')