from flask import Flask
from InvestoAnalayzers.MarketAnalayzer.StocksFilter import filter


app = Flask(__name__)


@app.route('/extract')
def extract_new_stocks_list(file_name, years_back, *args):
    filter.extract_stocks(file_name, years_back)


@app.route('/analayze')
def analayze_stocks(file_name, years_back):
    filter.choose_stocks(file_name, years_back)