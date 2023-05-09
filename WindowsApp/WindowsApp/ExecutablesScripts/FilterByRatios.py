from InvestoAnalayzers.MarketAnalayzer.StocksFilter.filter import sort_by_ratio
from Exceptions import InsufficientArgumentError
import sys
import pandas as pd

if __name__ == '__main__':
    num_argument = len(sys.argv) - 1
    if num_argument != 3:
        raise InsufficientArgumentError("Expected for two argument, got {0}".format(num_argument))

    else:
        sort_by_ratio(sys.argv[1], sys.argv[2], sys.argv[3])
