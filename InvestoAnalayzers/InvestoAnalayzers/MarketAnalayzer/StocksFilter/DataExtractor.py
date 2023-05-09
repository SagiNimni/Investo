# Libraries
from termcolor import colored
from functools import reduce
from tqdm import tqdm
import math
import time
import os
import psutil

from InvestoAnalayzers.MarketAnalayzer.StocksFilter.Sectors import *
import requests
import pandas as pd
import threading
import pickle


class Extractor(object):

    # Exceptions
    class SavingError(Exception):
        pass

    class LoadingError(Exception):
        pass

    # Constants
    API_KEY = "c161a4324922676fd4d6c88bd2f2428c"
    FMP_API_V3 = "https://financialmodelingprep.com/api/v3"
    FMP_API_V4 = "https://financialmodelingprep.com/api/v4"

    # Methods
    def __init__(self, min_market_cap, max_market_cap, min_volume, max_volume,
                 min_price, max_price, sectors=None, limit=100):
        """

        :param min_market_cap:
        :param max_market_cap:
        :param min_volume:
        :param max_volume:
        :param min_price:
        :param max_price:
        :param sectors:
        :param limit:
        """

        self.financial_ratios = {}

        parameters = f"marketCapMoreThan={min_market_cap}&marketCapLowerThan={max_market_cap}&" \
                     f"volumeMoreThan={min_volume}&volumeLowerThan={max_volume}" \
                     f"&priceMoreThan={min_price}&priceMoreThan={max_price}&limit={limit}&country=US" \
                     f"&isActivelyTrading=true"

        companies = []
        if sectors is not None:
            for sector in sectors:
                companies += (requests.get(f"{Extractor.FMP_API_V3}/stock-screener?{parameters}&sector={sector}"
                                           f"&apikey={Extractor.API_KEY}").json())
        else:
            companies += (requests.get(
                f"{Extractor.FMP_API_V3}/stock-screener?{parameters}&apikey={Extractor.API_KEY}").json())

        self.companies = list(map(lambda c: (c['symbol'], c['sector']), companies))

    def extract(self, years, batch_size=100, warnings=False):
        """

        :param years:
        :param batch_size:
        :param warnings:
        :return:
        """

        global extracted_ratios_list, memory_usage
        extracted_ratios_list = {}
        memory_usage = []

        def worker(companies):
            global extracted_ratios_list, memory_usage

            memory_usage.append(psutil.Process(os.getpid()).memory_info().rss / 1000000)

            for company, sector in companies:
                try:
                    if sector == '':
                        sector = 'Undefined'
                    ratios = requests.get(f'{Extractor.FMP_API_V3}/ratios/{company}?limit={years}'
                                          f'&apikey={Extractor.API_KEY}').json()
                    ratios = pd.DataFrame.from_dict(ratios)
                    if ratios.empty:
                        continue

                    growth = requests.get(f'{Extractor.FMP_API_V3}/financial-growth/{company}'
                                          f'?limit={years}&apikey={Extractor.API_KEY}').json()
                    growth = pd.DataFrame.from_dict(growth)
                    if growth.empty:
                        continue

                    metrics = requests.get(f'{Extractor.FMP_API_V3}/key-metrics/{company}'
                                           f'?limit={years}&apikey={Extractor.API_KEY}').json()
                    metrics = pd.DataFrame.from_dict(metrics)
                    if metrics.empty:
                        continue

                    core_info = requests.get(f'{Extractor.FMP_API_V4}/company-core-information?symbol={company}&apikey={Extractor.API_KEY}').json()
                    if core_info:
                        if core_info:
                            sic_code = core_info[0]['sicCode']
                            if sic_code is None:
                                sic_code = '00'
                            else:
                                sic_code = sic_code[:2]
                    else:
                        sic_code = '00'

                    ratios_analyzer = eval(f"{sector.replace(' ', '')}(company, ratios, growth, metrics, sic_code)")

                    extracted_ratios_list.update({company: ratios_analyzer})

                except Exception as e:
                    if warnings:
                        time.sleep(0.1)
                        print(colored("\n========================", 'yellow'))
                        print(colored('Warning!', 'yellow'))
                        print(colored(f'Failed to obtain data for {company} company ', 'yellow'))
                        print(e)
                        print(colored("========================", 'yellow'))
                        time.sleep(0.1)

        print("=============================")
        print("Obtaining Financial Data...")
        time.sleep(0.1)

        # Start each slave to work on separate batch
        start_time = time.time()
        batch_pointer = 0
        slaves = []
        for _ in range(math.ceil(len(self.companies)/batch_size)):
            slave = threading.Thread(target=worker, args=(self.companies[batch_pointer:batch_pointer+batch_size], ))
            slaves.append(slave)
            slave.start()
            batch_pointer += batch_size

        # Wait until all slaves are finished
        for slave in tqdm(slaves, colour='white'):
            slave.join()

        memory_usage = reduce(lambda a, b: a + b, memory_usage) / len(memory_usage)
        self.financial_ratios = extracted_ratios_list

        time.sleep(0.1)
        print("Finished in " + str(time.time() - start_time) + ' Seconds')
        print('RAM Usage: ' + str(memory_usage) + 'MB')
        print("Data Fetch Completed")
        print("=============================")

    def save(self, file_name):
        """

        :param file_name:
        :return:
        """

        try:
            path = file_name.rsplit('\\', 1)[0]
            if not os.path.exists(path):
                os.mkdir(path)

            with open(file_name, 'wb') as f:
                pickle.dump(self.financial_ratios, f)
        except Exception as e:
            raise Extractor.SavingError('Failed to save data')

    @staticmethod
    def load(filename):
        """

        :param filename:
        :return:
        """
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                return data
        except Exception as e:
            raise Extractor.LoadingError("Couldn't load objects from the pickle file")
