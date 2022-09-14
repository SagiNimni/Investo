# Libraries
from termcolor import colored
from tqdm import tqdm
import time

from MarketAnalyzer.StocksFilter.Sectors import *
import requests
import pandas as pd


class Extractor(object):

    # Constants
    API_KEY = "c161a4324922676fd4d6c88bd2f2428c"
    FMP_API = "https://financialmodelingprep.com/api/v3"

    # Methods
    def __init__(self, years, min_market_cap: int, max_market_cap: int, min_volume: int, max_volume: float,
                     min_price: int, max_price: int, sectors: None, limit=100, warnings=False):
        """
        The constructor takes a list of stocks (provided by the user in a text file) extracts a dict of important
        financial ratios for each company within the provided list

        :param companies_list: A path to a text file that contains the stocks list
        :param limit: the amount of years to analyze in the reports
        """

        self.financial_ratios = {}

        parameters = f"marketCapMoreThan={min_market_cap}&marketCapLowerThan={max_market_cap}&" \
                     f"volumeMoreThan={min_volume}&volumeLowerThan={max_volume}" \
                     f"&priceMoreThan={min_price}&priceMoreThan={max_price}&limit={limit}&country=US" \
                     f"&isActivelyTrading=true"

        companies = []
        if sectors is not None:
            for sector in sectors:
                companies += (requests.get(f"{Extractor.FMP_API}/stock-screener?{parameters}&sector={sector}"
                                           f"&apikey={Extractor.API_KEY}").json())
        else:
            companies += (requests.get(
                f"{Extractor.FMP_API}/stock-screener?{parameters}&apikey={Extractor.API_KEY}").json())

        companies = list(map(lambda c: (c['symbol'], c['sector']), companies))

        print("Obtaining Financial Data...")
        time.sleep(0.1)
        for company, sector in tqdm(companies, colour='white'):
            try:
                ratios = requests.get(f'{Extractor.FMP_API}/ratios/{company}?limit={years}'
                                      f'&apikey={Extractor.API_KEY}').json()
                ratios = pd.DataFrame.from_dict(ratios)
                if ratios.empty:
                    continue

                growth = requests.get(f'{Extractor.FMP_API}/financial-growth/{company}'
                                      f'?limit={years}&apikey={Extractor.API_KEY}').json()
                growth = pd.DataFrame.from_dict(growth)
                if growth.empty:
                    continue

                metrics = requests.get(f'{Extractor.FMP_API}/key-metrics/{company}'
                                       f'?limit={years}&apikey={Extractor.API_KEY}').json()
                metrics = pd.DataFrame.from_dict(metrics)
                if metrics.empty:
                    continue

                ratios_analyzer = eval(f"{sector.replace(' ', '')}(ratios, growth, metrics)")

                self.financial_ratios.update({company: ratios_analyzer})

            except Exception as e:
                if warnings:
                    print(colored("\n========================", 'yellow'))
                    print(colored('Warning!', 'yellow'))
                    print(colored(f'Failed to obtain data for {company} company ', 'yellow'))
                    print(colored("========================", 'yellow'))

        time.sleep(0.1)
        print("Data Fetch Completed")

    def execute_analyze(self):
        print("Starts Analysis...")
        time.sleep(0.1)
        chosen_companies = []
        for company, ratios in tqdm(self.financial_ratios.items(), colour='white'):
            # ratios.liquidity_test()
            # ratios.leverage_test()
            # ratios.efficiency_test()
            # ratios.profitability_test()
            # ratios.market_value_test()
            growth_test = ratios.growth_rate_test(plot=True)
            if all(value.all() for value in growth_test.values()):
                chosen_companies.append(company)

        time.sleep(0.1)
        print("Analyze Completed")
        return chosen_companies
