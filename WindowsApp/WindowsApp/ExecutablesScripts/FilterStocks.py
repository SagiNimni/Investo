from InvestoAnalayzers.MarketAnalayzer.StocksFilter.filter import filter_by_growth
from Exceptions import InsufficientArgumentError
import sys


if __name__ == '__main__':
    num_argument = len(sys.argv) - 1
    if num_argument != 2:
        raise InsufficientArgumentError("Expected for two argument, got {0}".format(num_argument))
    
    elif num_argument == 2:
        filter_by_growth(sys.argv[1], int(sys.argv[2]))
