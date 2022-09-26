import pandas as pd
from datetime import date
import matplotlib.pyplot as plt


# Ratios
class Ratios:

    def test_each_year(self, constants):
        tests = {}

        for var in type(self).__init__.__code__.co_varnames[1:]:
            tests.update({var: (eval(f'self.{var}>=constants.{var}'))})

        return tests

    def test_average(self, constants):
        tests = {}

        for var in type(self).__init__.__code__.co_varnames[1:]:
            tests.update({var: (eval(f'self.{var}.mean()>=constants.{var}'))})

        return tests

    def concatenate_ratios_average(self) -> pd.Series:
        series = []

        for var in type(self).__init__.__code__.co_varnames[1:]:
            series.append(eval(f'self.{var}'))

        return pd.concat(series, axis=1).mean()


class GrowthRatios(Ratios):

    def __init__(self, roic, sgr, eps, bvps, fcf):
        self.roic = roic
        self.sgr = sgr
        self.eps = eps
        self.bvps = bvps
        self.fcf = fcf

    def compare_to_constants(self, constants):
        if not isinstance(constants, GrowthRatios):
            return NotImplemented

        return self.test_average(constants)

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

    def __ge__(self, other):
        if not isinstance(other, LiquidityRatios):
            return NotImplemented

        return self.test_each_year(LiquidityRatios)


class LeverageRatios(Ratios):

    def __init__(self, debt_ratio, debt_to_equity_ratio, interest_coverage_ratio):
        self.debt_ratio = debt_ratio
        self.debt_to_equity_ratio = debt_to_equity_ratio
        self.interest_coverage_ratio = interest_coverage_ratio

    def __ge__(self, other):
        if not isinstance(other, LeverageRatios):
            return NotImplemented

        return self.test_each_year(LeverageRatios)


class EfficiencyRatios(Ratios):

    def __init__(self, inventory_turnover, days_sales_in_inventory, assets_turnover,
                 days_payables_outstanding, receivables_turnover):
        self.inventory_turnover = inventory_turnover
        self.assets_turnover = assets_turnover
        self.days_sales_in_inventory = days_sales_in_inventory
        self.days_payables_outstanding = days_payables_outstanding
        self.receivables_turnover = receivables_turnover

    def __ge__(self, other):
        if not isinstance(other, EfficiencyRatios):
            return NotImplemented

        return self.test_each_year(EfficiencyRatios)


class ProfitabilityRatios(Ratios):

    def __init__(self, gross_margin, operating_margin, return_on_assets, return_on_equity):
        self.gross_margin = gross_margin
        self.operating_margin = operating_margin
        self.return_on_assets = return_on_assets
        self.return_on_equity = return_on_equity

    def __ge__(self, other):
        if not isinstance(other, ProfitabilityRatios):
            return NotImplemented

        return self.test_each_year(ProfitabilityRatios)


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

    GROWTH_CONSTANTS = GrowthRatios(10, 10, 10, 10, 10)

    def __init__(self, name, ratios, growth, key_metrics):
        """


        :param ratios: a dict of all ratios for the company
        """

        self.name = name

        self.liquidity = LiquidityRatios(ratios['currentRatio'],
                                         ratios['quickRatio'],
                                         ratios['cashRatio'])

        self.leverage = LeverageRatios(ratios['debtRatio'],
                                       ratios['debtEquityRatio'],
                                       ratios['interestCoverage'])

        self.efficiency = EfficiencyRatios(ratios['daysOfInventoryOutstanding']*365,
                                           ratios['daysOfInventoryOutstanding'],
                                           ratios['assetTurnover'],
                                           ratios['daysOfPayablesOutstanding'],
                                           ratios['receivablesTurnover'])

        self.profitability = ProfitabilityRatios(ratios['grossProfitMargin'],
                                                 ratios['operatingProfitMargin'],
                                                 ratios['returnOnAssets'],
                                                 ratios['returnOnEquity'])

        self.value = MarketValueRatios(ratios['priceEarningsRatio'],
                                       ratios['dividendYield'])

        self.growth = GrowthRatios(key_metrics['roic'] * 100,
                                   growth['revenueGrowth'] * 100,
                                   growth['epsgrowth'] * 100,
                                   growth['bookValueperShareGrowth'] * 100,
                                   growth['freeCashFlowGrowth'] * 100)

    def liquidity_test(self):
        return self.liquidity.__ge__(self.LIQUIDITY_CONSTANTS)

    def leverage_test(self):
        return self.leverage.__ge__(self.LEVERAGE_CONSTANTS)

    def efficiency_test(self):
        return self.efficiency.__ge__(self.EFFICIENCY_CONSTANTS)

    def profitability_test(self):
        return self.profitability.__ge__(self.PROFITABILITY_CONSTANTS)

    def market_value_test(self):
        return self.value.__ge__(self.VALUE_CONSTANTS)

    def growth_rate_test(self, plot: bool):
        if plot:
            self.growth.plot(self.name)
        return self.growth.compare_to_constants(Sector.GROWTH_CONSTANTS)


class Energy(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(Energy, self).__init__(name, ratios, growth, key_metrics)


class BasicMaterials(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(BasicMaterials, self).__init__(name, ratios, growth, key_metrics)


class Industrials(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(Industrials, self).__init__(name, ratios, growth, key_metrics)


class Utilities(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(Utilities, self).__init__(name, ratios, growth, key_metrics)


class Healthcare(Sector):
    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(Healthcare, self).__init__(name, ratios, growth, key_metrics)


class FinancialServices(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(FinancialServices, self).__init__(name, ratios, growth, key_metrics)


class ConsumerCyclical(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(ConsumerCyclical, self).__init__(name, ratios, growth, key_metrics)


class Technology(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(Technology, self).__init__(name, ratios, growth, key_metrics)


class RealEstate(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(RealEstate, self).__init__(name, ratios, growth, key_metrics)


class CommunicationServices(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(CommunicationServices, self).__init__(name, ratios, growth, key_metrics)


class ConsumerDefensive(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(ConsumerDefensive, self).__init__(name, ratios, growth, key_metrics)


class Undefined(Sector):

    def __init__(self, name, ratios, growth, key_metrics):
        # self.LIQUIDITY_CONSTANTS = LiquidityRatios()
        # self.LEVERAGE_CONSTANTS = LeverageRatios()
        # self.EFFICIENCY_CONSTANTS = EfficiencyRatios()
        # self.PROFITABILITY_CONSTANTS = ProfitabilityRatios()
        # self.VALUE_CONSTANTS = MarketValueRatios()
        super(Undefined, self).__init__(name, ratios, growth, key_metrics)

