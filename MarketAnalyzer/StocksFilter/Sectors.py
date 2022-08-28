# Ratios
def test(class_name: type):
    tests = {}
    map(lambda var: tests.update({var: eval(f'self.{var}==other.{var}')}),
        class_name.__init__.__code__.co_varnames)
    return tests


class LiquidityRatios:

    def __init__(self, current_ratio, quick_ratio, cash_ratio):
        self.current_ratio = current_ratio
        self.quick_ratio = quick_ratio
        self.cash_ratio = cash_ratio

    def __eq__(self, other):
        if not isinstance(other, LiquidityRatios):
            return NotImplemented

        return test(LiquidityRatios)


class LeverageRatios:

    def __init__(self, debt_ratio, debt_to_equity_ratio, interest_coverage_ratio):
        self.debt_ratio = debt_ratio
        self.debt_to_equity_ratio = debt_to_equity_ratio
        self.interest_coverage_ratio = interest_coverage_ratio

    def __eq__(self, other):
        if not isinstance(other, LeverageRatios):
            return NotImplemented

        return test(LeverageRatios)


class EfficiencyRatios:

    def __init__(self, inventory_turnover, days_sales_in_inventory, assets_turnover,
                 days_payables_outstanding, receivables_turnover):
        self.inventory_turnover = inventory_turnover
        self.assets_turnover = assets_turnover
        self.days_sales_in_inventory = days_sales_in_inventory
        self.days_payables_outstanding = days_payables_outstanding
        self.receivables_turnover = receivables_turnover

    def __eq__(self, other):
        if not isinstance(other, EfficiencyRatios):
            return NotImplemented

        return test(EfficiencyRatios)


class ProfitabilityRatios:

    def __init__(self, gross_margin, operating_margin, return_on_assets, return_on_equity):
        self.gross_margin = gross_margin
        self.operating_margin = operating_margin
        self.return_on_assets = return_on_assets
        self.return_on_equity = return_on_equity

    def __eq__(self, other):
        if not isinstance(other, ProfitabilityRatios):
            return NotImplemented

        return test(ProfitabilityRatios)


class MarketValueRatios:

    def __init__(self, earning_per_share, price_earning, dividend_yield):
        self.earning_per_share = earning_per_share
        self.price_earning = price_earning
        self.dividend_yield = dividend_yield

    def __eq__(self, other):
        if not isinstance(other, MarketValueRatios):
            return NotImplemented

        return test(MarketValueRatios)


# Sectors
class Sector:

    LIQUIDITY_CONSTANTS = None
    LEVERAGE_CONSTANTS = None
    EFFICIENCY_CONSTANTS = None
    PROFITABILITY_CONSTANTS = None
    VALUE_CONSTANTS = None

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        """


        :param liquidity: [current ratio, quick ratio, cash ratio]
        :param leverage: [debt_ratio, debt_to_equity_ratio, interest_coverage_ratio]
        :param efficiency: [inventory_turnover, assets_turnover, days_sales_in_inventory,
                            days_payables_outstanding, receivables_turnover]
        :param profitability: [gross_margin, operating_margin, return_on_assets, return_on_equity]
        :param value: [earning_per_share, price_earning, book_value_per_share, dividend_yield]
        """
        self.liquidity = LiquidityRatios(*liquidity)
        self.leverage = LeverageRatios(*leverage)
        self.efficiency = EfficiencyRatios(*efficiency)
        self.profitability = ProfitabilityRatios(*profitability)
        self.value = MarketValueRatios(*value)

    def liquidity_test(self):
        return self.liquidity.__eq__(self.LIQUIDITY_CONSTANTS)

    def leverage_test(self):
        return self.leverage.__eq__(self.LEVERAGE_CONSTANTS)

    def efficiency_test(self):
        return self.efficiency.__eq__(self.EFFICIENCY_CONSTANTS)

    def profitability_test(self):
        return self.profitability.__eq__(self.PROFITABILITY_CONSTANTS)

    def market_value_test(self):
        return self.value.__eq__(self.VALUE_CONSTANTS)


class Energy(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class BasicMaterials(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class Industrials(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class Utilities(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class Healthcare(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class FinancialServices(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class ConsumerCyclical(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class Technology(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class RealEstate(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class CommunicationServices(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)


class ConsumerDefensive(Sector):

    LIQUIDITY_CONSTANTS = LiquidityRatios()
    LEVERAGE_CONSTANTS = LeverageRatios()
    EFFICIENCY_CONSTANTS = EfficiencyRatios()
    PROFITABILITY_CONSTANTS = ProfitabilityRatios()
    VALUE_CONSTANTS = MarketValueRatios()

    def __init__(self, liquidity: list, leverage: list, efficiency: list, profitability: list, value: list):
        super(Sector, self).__init__(liquidity, leverage, efficiency, profitability, value)

