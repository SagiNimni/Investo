import math
import sys
import pandas as pd


class BasicMarketConstants:
    SMALL_CAPS = (300000000, 2000000000)
    MEDIUM_CAPS = (2000000000, 10000000000)
    LARGE_CAPS = (10000000000, math.inf)
    ALL_CAPS = (0, math.inf)

    MINIMUM_VOLUME = 0
    MAXIMUM_VOLUME = math.inf
    MINIMUM_PRICE = 0
    MAXIMUM_PRICE = 100000


# Optimal ratios
class GrowthRatiosConstants:
    RETURN_ON_INVESTED_CAPITAL = pd.Series(10)
    EARNING_PER_SHARE_GROWTH = pd.Series(10)
    SALES_GROWTH = pd.Series(10)
    BOOK_VALUE_PER_SHARE_GROWTH = pd.Series(10)
    FREE_CASH_FLOW_GROWTH = pd.Series(10)


class PriceEarningPerSector:
    pass


BENCHMARKS_FILE_NAME = sys.argv[1].rsplit('\\', 3)[0].replace('\\', '/') + '/IndustryBenchmarks/benchmarks.json'
BENCHMARKS_LATEST_YEAR = 2020

