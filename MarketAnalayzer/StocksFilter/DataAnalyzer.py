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
    chosen_companies = {}

    for company, ratios in tqdm(financial_ratios.items(), colour='white'):
        growth_test = ratios.growth_rate_test(max_years, plot_graphs)

        if all(list(growth_test.values())):
            liquidity_grades = ratios.liquidity_test()
            leverage_grades = ratios.leverage_test()
            efficiency_grades = ratios.efficiency_test()
            profitability_grades = ratios.profitability_test()
            value_grades = ratios.market_value_test()
            chosen_companies.update({company: {'growth': ratios.growth.ratios.mean(),
                                               'liquidity': liquidity_grades,
                                               'leverage': leverage_grades,
                                               'efficiency': efficiency_grades,
                                               'profitability': profitability_grades,
                                               'value': value_grades}})

    time.sleep(0.1)
    print("Analyze Completed")
    print("=============================")

    if plot_result:
        for company, grades in chosen_companies.items():
            print(company + ':')
            print(grades['efficiency'], '\n')

    if save is not None:
        timeout = time.time()
        saved = False
        message = False

        while not saved and time.time() - timeout < 20:
            try:
                with pd.ExcelWriter(save) as writer:
                    for symbol, grades in chosen_companies.items():
                        grades = pd.concat(list(grades.values()))
                        pd.DataFrame(grades).to_excel(writer, sheet_name=symbol)
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
