# Libraries
from MarketAnalyzer.StocksFilter.Sectors import *
from stocksymbol import StockSymbol
import requests
import pandas as pd
import pickle


def list_symbols(symbols_list_dir, indexes=None):
    api_key = "7e24b8f4-a6f8-4720-afdf-c3ca1710bc57"
    ss = StockSymbol(api_key)

    if indexes is None:
        indexes = ss.get_index_list()
        indexes = list(filter(lambda index: index['market'] == 'america', indexes))
        indexes = list(map(lambda index: index['indexId'], indexes))

    symbols = []
    for index in indexes:
        symbols += ss.get_symbol_list(index=index, symbols_only=True)
    symbols = list(set(symbols))

    with open(symbols_list_dir, 'wb') as f:
        pickle.dump(symbols, f)


class Extractor(object):

    # Constants
    API_KEY = "c161a4324922676fd4d6c88bd2f2428c"

    # Methods
    def __init__(self, limit, companies_list):
        """
        The constructor takes a list of stocks (provided by the user in a text file) extracts a dict of important
        financial ratios for each company within the provided list

        :param companies_list: A path to a text file that contains the stocks list
        :param limit: the amount of years to analyze in the reports
        """

        self.financial_ratios = {}
        self.financial_data = {}
        self.stock_info = {}

        with open(companies_list, 'rb') as f:
            companies = pickle.load(f)

        for company in companies:
            balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/'
                                         f'{company}?limit={limit}&apikey={Extractor.API_KEY}').json()
            balance_sheet = pd.DataFrame.from_dict(balance_sheet)

            cash_flow = requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/'
                                     f'{company}?limit={limit}&apikey={Extractor.API_KEY}').json()
            cash_flow = pd.DataFrame.from_dict(cash_flow)

            income_statement = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/'
                                     f'{company}?limit={limit}&apikey={Extractor.API_KEY}').json()
            income_statement = pd.DataFrame.from_dict(income_statement)

            ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}'
                                  f'{company}?limit={limit}&apikey={Extractor.API_KEY}').json()
            ratios = pd.DataFrame.from_dict(ratios)

            info = requests.get(f'https://financialmodelingprep.com/api/v3/quote/{company}'
                                f'?apikey={Extractor.API_KEY}').json()

            ratios_analyzer = eval(f"{info['sector'].replace(' ', '')}(ratios, balance_sheet, cash_flow,"
                                   f" income_statement, info)")
            self.financial_ratios.update({company: ratios_analyzer})

            self.stock_info.update({company: {'price': info['price'],
                                              'market-cap': info['marketCap'],
                                              'volume': info['avgVolume']}})

    def filter(self, min_market_cap: int, max_market_cap: int, min_volume: int, min_price: int, max_price: int,
               sectors=None, limit=None) -> dict:
        """
        This method filters the companies according to the parameters and returns a filtered dict

        :param min_market_cap: the minimum threshold for stock's market cap
        :param max_market_cap: the maximum threshold for stock's market cap
        :param min_volume: the minimum threshold for stock's volume
        :param min_price: the minimum price for stock
        :param max_price: the maximum price for stock
        :param sectors: a list of sectors to filter from the list(optional)
        :param limit: limit the number of stocks to find(optional)
        :return: A dict of filtered data
        """

        filtered_data = {}

        for company in self.financial_ratios:
            if min_market_cap < self.stock_info[company]['market-cap'] < max_market_cap and\
                    min_volume < self.stock_info[company]['volume'] and\
                    min_price < self.stock_info[company]['price'] < max_price:
                if sectors is None:
                    filtered_data.update({company: self.financial_ratios[company]})
                    continue
                if type(self.stock_info[company]).__name__ in sectors:
                    filtered_data.update({company: self.financial_ratios[company]})

        return filtered_data
