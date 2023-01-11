from flask import Flask
from InvestoAnalayzers.MarketAnalayzer.StocksFilter import filter


app = Flask(__name__)


@app.route('/listStocks')
def extract_new_stocks_list(file_name, years_back, *args):
    """
    This request gets values from the client and creates a list
    of stocks according to them.

    Args:
        file_name (_type_): _description_
        years_back (_type_): _description_
    """
    filter.extract_stocks(file_name, years_back)


@app.route('/bestFinancialsStocks')
def analayze_stocks(file_name, years_back):
    """
    Gets a list of stocks from the client and filters it by best financial reports
    returns a list of stocks that passed the test of the API.

    Args:
        file_name (_type_): _description_
        years_back (_type_): _description_
    """
    filter.choose_stocks(file_name, years_back)