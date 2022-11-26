from MarketAnalayzer.StocksFilter.filter import choose_stocks, extract_stocks
import sys


class InsufficientArgumentError(Exception):
    pass


if __name__ == '__main__':
    num_argument = len(sys.argv) - 1
    if num_argument < 2:
        raise InsufficientArgumentError(f"Expected for two argument, got {num_argument}")

    elif num_argument == 2:
        extract_stocks(sys.argv[1], int(sys.argv[2]))
        choose_stocks(sys.argv[1], int(sys.argv[2]))

    else:
        extra_arguments = ','.join(sys.argv[3:])
        eval(f'extract_stocks(sys.argv[1], int(sys.argv[2]), {extra_arguments})')
        eval(f'choose_stocks(sys.argv[1], int(sys.argv[2]))')
