from MarketAnalayzer.StocksFilter.constants import GrowthRatiosConstants as growthConstants, BENCHMARKS_PATH
from MarketAnalayzer.StocksFilter.IndustryBenchmarks.ObtainData import obtain_data
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import json
import os


# Ratios
class Ratios:

    def test_each_year(self, constants, year):
        tests = {}
        index = date.today().year-1 - int(year)

        try:
            for var in type(self).__init__.__code__.co_varnames[1:]:
                tests.update({var: (eval(f'self.{var}[{index}]>=constants.{var}'))})

            return tests

        except TypeError:
            return []

    def test_average(self, constants, max_years=''):
        tests = {}

        for var in type(self).__init__.__code__.co_varnames[1:]:
            tests.update({var: (eval(f'self.{var}[:{max_years}].mean()>=constants.{var}'))})

        return tests

    def concatenate_ratios_average(self, max_years) -> pd.Series:
        series = []

        for var in type(self).__init__.__code__.co_varnames[1:]:
            series.append(eval(f'self.{var}[:{max_years}]'))

        return pd.concat(series, axis=1).mean()


class GrowthRatios(Ratios):

    def __init__(self, roic, sgr, eps, bvps, fcf):
        self.roic = roic
        self.sgr = sgr
        self.eps = eps
        self.bvps = bvps
        self.fcf = fcf

    def compare_to_constants(self, constants: Ratios, max_years):
        if not isinstance(constants, GrowthRatios):
            return NotImplemented

        return self.test_average(constants, max_years=max_years)

    def plot(self, name):
        df = pd.concat([self.eps, self.roic, self.sgr, self.bvps, self.fcf], axis=1).iloc[::-1]
        df.columns = ['EPS', 'ROIC', 'SGR', 'BVPS', 'FCF']
        df.index = list(range(date.today().year - df.shape[0], date.today().year))
        df.plot(title=name, label='Year', kind='bar', figsize=(9, 8))
        plt.show()


class LiquidityRatios(Ratios):

    def __init__(self, current_ratio, quick_ratio, cash_ratio):
        self.current_ratio = current_ratio
        self.quick_ratio = quick_ratio
        self.cash_ratio = cash_ratio

    def compare_to_benchmarks(self, benchmarks: Ratios, year):
        if not isinstance(benchmarks, LiquidityRatios):
            return NotImplemented

        return self.test_each_year(benchmarks, year)


class LeverageRatios(Ratios):

    def __init__(self, debt_ratio, debt_to_equity_ratio, interest_coverage_ratio):
        self.debt_ratio = debt_ratio
        self.debt_to_equity_ratio = debt_to_equity_ratio
        self.interest_coverage_ratio = interest_coverage_ratio

    def compare_to_benchmarks(self, benchmarks: Ratios):
        if not isinstance(benchmarks, LeverageRatios):
            return NotImplemented

        return self.test_each_year(benchmarks)


class EfficiencyRatios(Ratios):

    def __init__(self, inventory_turnover, assets_turnover, receivables_turnover):
        self.inventory_turnover = inventory_turnover
        self.assets_turnover = assets_turnover
        self.receivables_turnover = receivables_turnover

    def compare_to_benchmarks(self, benchmarks: Ratios):
        if not isinstance(benchmarks, EfficiencyRatios):
            return NotImplemented

        return self.test_each_year(benchmarks)


class ProfitabilityRatios(Ratios):

    def __init__(self, gross_margin, operating_margin, return_on_assets, return_on_equity, profit_margin):
        self.gross_margin = gross_margin
        self.operating_margin = operating_margin
        self.return_on_assets = return_on_assets
        self.return_on_equity = return_on_equity
        self.profit_margin = profit_margin

    def compare_to_benchmarks(self,  benchmarks: Ratios):
        if not isinstance(benchmarks, ProfitabilityRatios):
            return NotImplemented

        return self.test_each_year(benchmarks)


class MarketValueRatios(Ratios):

    def __init__(self, price_earning: pd.Series, dividend_yield: pd.Series):
        self.price_earning = price_earning
        self.dividend_yield = dividend_yield

    def __ge__(self, other):
        if not isinstance(other, MarketValueRatios):
            return NotImplemented

        return self.test_each_year(MarketValueRatios)


# TODO Add all values for each sector for benchmarking purposes
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
        tests = []
        for year, benchmarks in Sector.BENCHMARKS_PER_SIC.items():
            benchmarks = LiquidityRatios(benchmarks['CurrentRatio' + self.sic],
                                         benchmarks['QuickRatio' + self.sic],
                                         benchmarks['CashRatio' + self.sic])
            tests.append(self.liquidity.compare_to_benchmarks(benchmarks, year))
        tests = pd.DataFrame(tests)

        stock_grade = {}
        for ratio, results in tests.items():
            grade = results.value_counts()[True] / results.count() * 100
            stock_grade.update({ratio: grade})

        return stock_grade

    def leverage_test(self):
        benchmarks = LeverageRatios(Sector.BENCHMARKS_PER_SIC['DebtRatio' + self.sic],
                                     Sector.BENCHMARKS_PER_SIC['DebtToEquityRatio' + self.sic],
                                     Sector.BENCHMARKS_PER_SIC['InterestCoverageRatio' + self.sic])
        tests = self.leverage.compare_to_benchmarks(benchmarks)

    def efficiency_test(self):
        benchmarks = EfficiencyRatios(Sector.BENCHMARKS_PER_SIC['InventoryTurnover' + self.sic],
                                      Sector.BENCHMARKS_PER_SIC['AssetsTurnover' + self.sic],
                                      Sector.BENCHMARKS_PER_SIC['InterestCoverageRatio' + self.sic])
        return self.efficiency.compare_to_benchmarks(benchmarks)

    def profitability_test(self):
        benchmarks = ProfitabilityRatios(Sector.BENCHMARKS_PER_SIC['GrossMargin' + self.sic],
                                         Sector.BENCHMARKS_PER_SIC['OperatingMargin' + self.sic],
                                         Sector.BENCHMARKS_PER_SIC['Roa' + self.sic],
                                         Sector.BENCHMARKS_PER_SIC['Roe' + self.sic],
                                         Sector.BENCHMARKS_PER_SIC['ProfitMargin' + self.sic])
        return self.profitability.compare_to_benchmarks(benchmarks)

    def market_value_test(self):
        return self.value.__ge__(self.VALUE_CONSTANTS)

    def growth_rate_test(self, max_years, plot: bool):
        if plot:
            self.growth.plot(self.name)
        return self.growth.compare_to_constants(Sector.GROWTH_CONSTANTS, max_years=max_years)


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

