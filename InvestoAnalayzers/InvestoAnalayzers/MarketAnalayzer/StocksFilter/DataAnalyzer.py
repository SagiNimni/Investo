from tqdm import tqdm
import time
import pandas as pd


def execute_analyze(financial_ratios, max_years='', save=None, plot_result=False, plot_graphs=False):
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
