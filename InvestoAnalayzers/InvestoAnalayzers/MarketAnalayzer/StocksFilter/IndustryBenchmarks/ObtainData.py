import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import json
import string
import os


def get_ready_ratios_data(file_name: str):
    ready_ratios_url = "https://www.readyratios.com/"
    html = BeautifulSoup(requests.get(ready_ratios_url + 'sec/industry/').text, 'html.parser')
    ratios_list = html.find_all("table")[0].find_all("a")
    url_extensions = []
    for ratio in ratios_list:
        name = re.sub(r"\([^()]*\)", '', ratio.string.strip('\n')).replace('-', ' ').replace(',', ' ')
        name = string.capwords(name).replace(' ', '')
        url_extensions.append((ratio.get('href'), name))

    ratios_per_industry = {}
    file_path, file_name = file_name.rsplit('/', 1)
    try:
        os.mkdir(file_path)
    except FileExistsError:
        pass

    writer = pd.ExcelWriter(file_path + "/" + file_name + '.xlsx')
    for extension, ratio_name in url_extensions:
        benchmarks_dataframe = pd.read_html(ready_ratios_url + extension)[0]
        ratios_per_industry.update({ratio_name: benchmarks_dataframe})
        benchmarks_dataframe.to_excel(writer, sheet_name=ratio_name)
    writer.save()
    return ratios_per_industry


def json_benchmarks(data, file_name: str):

    def percent_to_decimal(number):
        if type(number) == str:
            if '%' in number:
                return round(float(number.strip('%')) / 100.0, 3)
        return number

    with open(file_name + '.json', 'w+') as f:
        benchmarks = {}
        years = iter(list(data.values())[0]['Year'])

        # The first year is pay blocked in the website
        next(years)

        for year in years:
            benchmarks.update({year: {}})
            for ratio_name, ratio_values in data.items():
                industries = ratio_values['Industry title']['Industry title'].tolist()
                industries[0] = '00'
                year_values = ratio_values['Year'][year].tolist()
                benchmarks[year].update(dict(map(lambda values: (ratio_name + values[0][:2], percent_to_decimal(values[1])),
                                                 list(zip(industries, year_values)))))

        json.dump(benchmarks, f)


def obtain_benchmarks(file_name):
    if not os.path.exists(file_name):
        ratios = get_ready_ratios_data(file_name)
        json_benchmarks(ratios, file_name)

