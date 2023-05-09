from functools import reduce
from tqdm import tqdm
import time
import pandas as pd
import numpy as np


def execute_growth_analyze(financial_ratios, max_years='', save=None, plot_result=False, plot_graphs=False):
    """

    :param financial_ratios:
    :param save:
    :param plot_result:
    :param plot_graphs:
    :param max_years:
    :return:
    """

    print("=============================")
    print("Starts Analysis...")
    time.sleep(0.1)
    chosen_companies = pd.DataFrame([])

    for company, ratios in tqdm(financial_ratios.items(), colour='white'):
        growth_test = ratios.growth_rate_test(max_years, plot_graphs)

        if all(list(growth_test.values())):
            liquidity_grades = ratios.liquidity_test()
            leverage_grades = ratios.leverage_test()
            efficiency_grades = ratios.efficiency_test()
            profitability_grades = ratios.profitability_test()
            value_grades = ratios.market_value_test()
            chosen_companies.loc[:, company] = pd.Series({'growth': ratios.growth.ratios.mean(),
                                                          'liquidity': liquidity_grades,
                                                          'leverage': leverage_grades,
                                                          'efficiency': efficiency_grades,
                                                          'profitability': profitability_grades,
                                                          'value': value_grades})

    time.sleep(0.1)
    print("Analyze Completed")
    print("=============================")

    if plot_result:
        for company, grades in chosen_companies.items():
            print(f'{company:.^20}' + ':\n')
            print('Growth:')
            print(grades['growth'], '\n')
            print('Efficiency Ratios:')
            print(grades['efficiency'], '\n')
            print('Liquidity Ratios:')
            print(grades['liquidity'], '\n')
            print('Leverage Ratios:')
            print(grades['leverage'], '\n')
            print('Profitability Ratios:')
            print(grades['profitability'], '\n')
            print('Marker Value Ratios:')
            print(grades['value'], '\n\n')

    if save is not None:
        timeout = time.time()
        saved = False
        message = False

        while not saved and time.time() - timeout < 20:
            try:
                chosen_companies.to_json(save)
                saved = True
                print("Successfully saved the results")

            except PermissionError:
                if not message:
                    print("Please close the file to complete saving!")
                    message = True
                time.sleep(1)

        if not saved:
            print("Timeout, Could't save the results!")

    return chosen_companies


def filter_by_ratios_type(companies_grades_list: pd.DataFrame, ratio_type: str, ascending: bool, save=None):

    class RatiosTypesAscending:
        liquidity = True
        leverage = False
        efficiency = True
        profitability = True
        value = False

    def mean(values: list) -> float:
        if None in values:
            return np.NAN
        return reduce(lambda x, y: x + y, values) / len(values)

    try:
        ratio_grades = companies_grades_list.loc[ratio_type].apply(lambda grades: mean(list(grades.values())))
        if ascending:
            ratio_grades = ratio_grades.sort_values(ascending=eval(f"RatiosTypesAscending.{ratio_type}"))
        else:
            ratio_grades = ratio_grades.iloc[np.abs(ratio_grades-1).argsort()]

        if save is not None:
            ratio_grades.to_json(save)
            print("Succesfully sorted the list")
        else:
            return ratio_grades
    except Exception as e:
        print("Failed to sort the list", e)
