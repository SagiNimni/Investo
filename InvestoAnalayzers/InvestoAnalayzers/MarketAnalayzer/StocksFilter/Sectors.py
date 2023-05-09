import time
from InvestoAnalayzers.MarketAnalayzer.StocksFilter.constants import GrowthRatiosConstants as growthConstants
from InvestoAnalayzers.MarketAnalayzer.StocksFilter.constants import BENCHMARKS_FILE_NAME, BENCHMARKS_LATEST_YEAR
from InvestoAnalayzers.MarketAnalayzer.StocksFilter.IndustryBenchmarks.ObtainData import obtain_benchmarks
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import json


# Ratios
class Ratios:

    def __init__(self, ratios: pd.DataFrame):
        self.ratios = ratios

    def _test_each_year_(self, constants, year):
        tests = {}
        index = BENCHMARKS_LATEST_YEAR - int(year)

        for ratio, values in self.ratios.items():
            try:
                tests.update({ratio: values[index] / float(constants[ratio][0])})

            except TypeError:
                continue

            except KeyError:
                break

        return tests


class GrowthRatios(Ratios):

    def __init__(self, ratios: pd.DataFrame):
        super().__init__(ratios)

    def compare_to_constants(self, max_years):

        tests = {}
        for ratio, values in self.ratios.items():
            tests.update({ratio: values[:max_years].mean() >= Sector.GROWTH_CONSTANTS.ratios[ratio][0]})

        return tests

    def plot(self, name):
        # TODO fix plot function
        df = pd.concat([self.eps, self.roic, self.sgr, self.bvps, self.fcf], axis=1).iloc[::-1]
        df.columns = ['EPS', 'ROIC', 'SGR', 'BVPS', 'FCF']
        df.index = list(range(date.today().year - df.shape[0], date.today().year))
        df.plot(title=name, label='Year', kind='bar', figsize=(9, 8))
        plt.show()


class LiquidityRatios(Ratios):

    def __init__(self, ratios: pd.DataFrame):
        super().__init__(ratios)

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = pd.DataFrame([{'currentRatio': benchmarks['CurrentRatio' + sic],
                                       'quickRatio': benchmarks['QuickRatio' + sic],
                                        'cashRatio': benchmarks['CashRatio' + sic]}])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


class LeverageRatios(Ratios):

    def __init__(self, ratios: pd.DataFrame):
        super().__init__(ratios)

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = pd.DataFrame([{'debtRatio': benchmarks['DebtRatio' + sic],
                                        'debtEquityRatio': benchmarks['DebtToEquityRatio' + sic],
                                        'interestCoverageRatio': benchmarks['InterestCoverageRatio' + sic]}])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


class EfficiencyRatios(Ratios):

    def __init__(self, ratios: pd.DataFrame):
        super().__init__(ratios)

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = pd.DataFrame([{'inventoryTurnover': benchmarks['InventoryTurnover' + sic],
                                        'assetTurnover': benchmarks['AssetTurnover' + sic],
                                        'receivablesTurnover': benchmarks['ReceivablesTurnover' + sic]}])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


class ProfitabilityRatios(Ratios):

    def __init__(self, ratios: pd.DataFrame):
        super().__init__(ratios)

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = pd.DataFrame([{'grossProfitMargin': benchmarks['GrossMargin' + sic],
                                        'operatingProfitMargin': benchmarks['OperatingMargin' + sic],
                                        'returnOnAssets': benchmarks['RoeAfterTax' + sic],
                                        'returnOnEquity': benchmarks['Roa' + sic],
                                        'netProfitMargin': benchmarks['ProfitMargin' + sic]}])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


# TODO add PE ratio per sector
class MarketValueRatios(Ratios):

    def __init__(self, ratios: pd.DataFrame):
        super().__init__(ratios)

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = pd.DataFrame([{'priceEarningsRatio': 10.0,
                                       'dividendYield': benchmarks['DividendPayoutRatio' + sic]}])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


# Sectors
class Sector:
    GROWTH_CONSTANTS = GrowthRatios(pd.DataFrame(({'roic': growthConstants.RETURN_ON_INVESTED_CAPITAL,
                                                   'revenueGrowth': growthConstants.SALES_GROWTH,
                                                   'epsgrowth': growthConstants.EARNING_PER_SHARE_GROWTH,
                                                   'bookValueperShareGrowth': growthConstants.BOOK_VALUE_PER_SHARE_GROWTH,
                                                   'freeCashFlowGrowth': growthConstants.FREE_CASH_FLOW_GROWTH})))

    obtain_benchmarks(BENCHMARKS_FILE_NAME)
    with open(BENCHMARKS_FILE_NAME) as f:
        BENCHMARKS_PER_SIC = json.load(f)

    def __init__(self, name, ratios, growth, key_metrics, sic):
        """


        :param ratios: a dict of all ratios for the company
        """

        self.sic = sic

        self.name = name

        self.liquidity = LiquidityRatios(ratios.loc[:, ['currentRatio', 'quickRatio', 'cashRatio']])

        self.leverage = LeverageRatios(ratios.loc[:, ['debtRatio', 'debtEquityRatio', 'interestCoverage']])

        self.efficiency = EfficiencyRatios(ratios.loc[:, ['inventoryTurnover', 'assetTurnover', 'receivablesTurnover']])

        self.profitability = ProfitabilityRatios(ratios.loc[:, ['grossProfitMargin', 'operatingProfitMargin',
                                                                'returnOnAssets', 'returnOnEquity', 'netProfitMargin']])

        self.value = MarketValueRatios(ratios.loc[:, ['priceEarningsRatio', 'dividendYield']])

        self.growth = GrowthRatios(growth.loc[:, ['revenueGrowth', 'epsgrowth', 'bookValueperShareGrowth', 'freeCashFlowGrowth']].assign(roic=pd.Series(key_metrics['roic'])) * 100)

    def liquidity_test(self):
        return self.liquidity.compare_to_benchmarks(self.sic).mean()

    def leverage_test(self):
        return self.leverage.compare_to_benchmarks(self.sic).mean()

    def efficiency_test(self):
        return self.efficiency.compare_to_benchmarks(self.sic).mean()

    def profitability_test(self):
        return self.profitability.compare_to_benchmarks(self.sic).mean()

    def market_value_test(self):
        return self.value.compare_to_benchmarks(self.sic).mean()

    def growth_rate_test(self, max_years, plot: bool):
        if plot:
            self.growth.plot(self.name)
        return self.growth.compare_to_constants(max_years)


class Energy(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(Energy, self).__init__(name, ratios, growth, key_metrics, sic)


class BasicMaterials(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(BasicMaterials, self).__init__(name, ratios, growth, key_metrics, sic)


class Industrials(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(Industrials, self).__init__(name, ratios, growth, key_metrics, sic)


class Utilities(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(Utilities, self).__init__(name, ratios, growth, key_metrics, sic)


class Healthcare(Sector):
    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(Healthcare, self).__init__(name, ratios, growth, key_metrics, sic)


class FinancialServices(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(FinancialServices, self).__init__(name, ratios, growth, key_metrics, sic)


class ConsumerCyclical(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(ConsumerCyclical, self).__init__(name, ratios, growth, key_metrics, sic)


class Technology(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(Technology, self).__init__(name, ratios, growth, key_metrics, sic)


class RealEstate(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(RealEstate, self).__init__(name, ratios, growth, key_metrics, sic)


class CommunicationServices(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(CommunicationServices, self).__init__(name, ratios, growth, key_metrics, sic)


class ConsumerDefensive(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(ConsumerDefensive, self).__init__(name, ratios, growth, key_metrics, sic)


class Undefined(Sector):

    def __init__(self, name, ratios, growth, key_metrics, sic):
        super(Undefined, self).__init__(name, ratios, growth, key_metrics, sic)

