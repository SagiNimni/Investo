from MarketAnalayzer.StocksFilter.constants import GrowthRatiosConstants as growthConstants, BENCHMARKS_PATH
from MarketAnalayzer.StocksFilter.IndustryBenchmarks.ObtainData import obtain_data
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import json
import os


# Ratios
class Ratios:

    def _test_each_year_(self, constants, year):
        tests = {}
        index = date.today().year-1 - int(year)

        for ratio, values in self.ratios.items():
            try:
                tests.update({ratio: (values[index] / constants.ratios[ratio])[0]})

            except TypeError:
                continue

            except KeyError:
                break

        return tests


class GrowthRatios(Ratios):

    def __init__(self, roic, sgr, eps, bvps, fcf):
        self.ratios = pd.DataFrame({'roic': [roic],
                                    'sgr': [sgr],
                                    'eps': [eps],
                                    'bvps': [bvps],
                                    'fcf': [fcf]})

    def compare_to_constants(self, max_years):

        tests = {}
        for ratio, values in self.ratios.items():
            tests.update({ratio: values[:max_years].mean() >= Sector.GROWTH_CONSTANTS.ratios[ratio][0]})

        return tests

    def plot(self, name):
        df = pd.concat([self.eps, self.roic, self.sgr, self.bvps, self.fcf], axis=1).iloc[::-1]
        df.columns = ['EPS', 'ROIC', 'SGR', 'BVPS', 'FCF']
        df.index = list(range(date.today().year - df.shape[0], date.today().year))
        df.plot(title=name, label='Year', kind='bar', figsize=(9, 8))
        plt.show()


class LiquidityRatios(Ratios):

    def __init__(self, current_ratio, quick_ratio, cash_ratio):
        self.ratios = pd.DataFrame({'current-ratio': [current_ratio],
                                    'quick-ratio': [quick_ratio],
                                    'cash-ratio': [cash_ratio]})

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = LiquidityRatios(benchmarks['CurrentRatio' + sic],
                                         benchmarks['QuickRatio' + sic],
                                         benchmarks['CashRatio' + sic])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


class LeverageRatios(Ratios):

    def __init__(self, debt_ratio, debt_to_equity_ratio, interest_coverage_ratio):
        self.ratios = pd.DataFrame({'debt-ratio': [debt_ratio],
                                    'debt-to-equity-ratio': [debt_to_equity_ratio],
                                    'interest-coverage': [interest_coverage_ratio]})

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = LeverageRatios(benchmarks['DebtRatio' + sic],
                                        benchmarks['DebtToEquityRatio' + sic],
                                        benchmarks['InterestCoverageRatio' + sic])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


class EfficiencyRatios(Ratios):

    def __init__(self, inventory_turnover, assets_turnover, receivables_turnover):
        self.ratios = pd.DataFrame({'inventory-turnover': [inventory_turnover],
                                    'assets-turnover': [assets_turnover],
                                    'receivables_turnover': [receivables_turnover]})

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = EfficiencyRatios(benchmarks['InventoryTurnover' + sic],
                                          benchmarks['AssetTurnover' + sic],
                                          benchmarks['ReceivablesTurnover' + sic])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


class ProfitabilityRatios(Ratios):

    def __init__(self, gross_margin, operating_margin, return_on_assets, return_on_equity, profit_margin):
        self.ratios = pd.DataFrame({'gross_margin': [gross_margin],
                                    'operating_margin': [operating_margin],
                                    'return_on_assets': [return_on_assets],
                                    'return_on_equity': [return_on_equity],
                                    'profit_margin': [profit_margin]})

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = ProfitabilityRatios(benchmarks['GrossMargin' + sic],
                                             benchmarks['OperatingMargin' + sic],
                                             benchmarks['RoeAfterTax' + sic],
                                             benchmarks['Roa' + sic],
                                             benchmarks['ProfitMargin' + sic])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


# TODO add PE ratio per sector
class MarketValueRatios(Ratios):

    def __init__(self, price_earning, dividend_yield):
        self.ratios = pd.DataFrame({'price-earnings': [price_earning],
                                    'dividend_yield': [dividend_yield]})

    def compare_to_benchmarks(self, sic):
        tests = {}
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = MarketValueRatios(10.0,
                                           benchmarks['DividendPayoutRatio' + sic])
            tests.update({year: self._test_each_year_(benchmarks, year)})

        return pd.DataFrame(tests).transpose()


# Sectors
class Sector:

    GROWTH_CONSTANTS = GrowthRatios(growthConstants.RETURN_ON_INVESTED_CAPITAL,
                                    growthConstants.SALES_GROWTH,
                                    growthConstants.EARNING_PER_SHARE_GROWTH,
                                    growthConstants.BOOK_VALUE_PER_SHARE_GROWTH,
                                    growthConstants.FREE_CASH_FLOW_GROWTH)

    if not os.path.exists(BENCHMARKS_PATH[0] + BENCHMARKS_PATH[1] + '.json'):
        obtain_data(BENCHMARKS_PATH)

    with open(BENCHMARKS_PATH[0] + BENCHMARKS_PATH[1] + '.json') as f:
        BENCHMARKS_PER_SIC = json.load(f)

    def __init__(self, name, ratios, growth, key_metrics, sic):
        """


        :param ratios: a dict of all ratios for the company
        """

        self.sic = sic

        self.name = name

        self.liquidity = LiquidityRatios(ratios['currentRatio'],
                                         ratios['quickRatio'],
                                         ratios['cashRatio'])

        self.leverage = LeverageRatios(ratios['debtRatio'],
                                       ratios['debtEquityRatio'],
                                       ratios['interestCoverage'])

        self.efficiency = EfficiencyRatios(ratios['inventoryTurnover'],
                                           ratios['assetTurnover'],
                                           ratios['receivablesTurnover'])

        self.profitability = ProfitabilityRatios(ratios['grossProfitMargin'],
                                                 ratios['operatingProfitMargin'],
                                                 ratios['returnOnAssets'],
                                                 ratios['returnOnEquity'],
                                                 ratios['netProfitMargin'])

        self.value = MarketValueRatios(ratios['priceEarningsRatio'],
                                       ratios['dividendYield'])

        self.growth = GrowthRatios(key_metrics['roic'] * 100,
                                   growth['revenueGrowth'] * 100,
                                   growth['epsgrowth'] * 100,
                                   growth['bookValueperShareGrowth'] * 100,
                                   growth['freeCashFlowGrowth'] * 100)

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

