# Libraries
from MarketAnalyzer.StocksFilter.Sectors import *
import requests
import pandas as pd
import yfinance as yf


class Extractor(object):

    # Constants
    API_KEY = "c161a4324922676fd4d6c88bd2f2428c"

    # Methods
    def __init__(self, limit, companies_list="./checklist.txt"):
        """
        The constructor takes a list of stocks (provided by the user in a text file) extracts a dict of important
        financial ratios for each company within the provided list

        :param companies_list: A path to a text file that contains the stocks list
        :param limit: the amount of years to analyze in the reports
        """

        self.financial_ratios = {}
        self.financial_data = {}
        self.stock_info = {}

        with open(companies_list, 'r+') as f:
            companies = f.read().split('\n')

        for company in companies:
            balance_sheet = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/'
                                         f'{company}?limit={limit}&apikey={Extractor.API_KEY}').json()
            balance_sheet = pd.DataFrame.from_dict(balance_sheet)

            ratios = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/'
                                  f'{company}?limit={limit}&apikey={Extractor.API_KEY}').json()
            ratios = pd.DataFrame.from_dict(ratios)

            info = yf.Ticker(company).info

            liquidity = [ratios['currentRatio'], ratios['quickRatio'], ratios['cashRatio']]
            leverage = [ratios['debtRatio'], ratios['debtToEquity'], ratios['interestCoverage']]
            efficiency = [ratios['daysOfInventoryOutstanding']*365, ratios['daysOfInventoryOutstanding'],
                          ratios['assetTurnover'], ratios['daysOfPayablesOutstanding'], ratios['receivablesTurnover']]
            profitability = [ratios['grossProfitMargin'], ratios['operatingProfitMargin'], ratios['returnOnAssets'],
                             ratios['returnOnEquity']]
            value = [ratios['revenuePerShare'], ratios['peRatio'], ratios['dividendYield']]

            stock_ratios = eval('{0}({1},{2},{3},{4},{5})'.format(
                info['sector'], liquidity, leverage, efficiency, profitability, value))

            self.financial_ratios.update({company: (info['sector'], stock_ratios)})

            self.stock_info.update({company: {'price': info['currentPrice'],
                                              'market-cap': info['marketCap'],
                                              'volume': info['volume']}})

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

        for company in self.financial_data:
            if min_market_cap < self.stock_info[company]['market-cap'] < max_market_cap and\
                    min_volume < self.stock_info[company]['volume'] and\
                    min_price < self.stock_info[company]['price'] < max_price:
                if sectors is None:
                    filtered_data.update({company: self.financial_data[company]})
                    continue
                if self.stock_info[company]['sector'] in sectors:
                    filtered_data.update({company: self.financial_data[company]})

        return filtered_data
