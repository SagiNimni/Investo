from tqdm import tqdm
import time
import pandas as pd


def execute_analyze(financial_ratios, max_years='', save=None, plot_result=False, plot_graphs=False) -> pd.DataFrame:
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
    chosen_companies = []

    for company, ratios in tqdm(financial_ratios.items(), colour='white'):
        try:
            liquidity_grades = ratios.liquidity_test()
            # ratios.leverage_test()
            # ratios.efficiency_test()
            # ratios.profitability_test()
            # ratios.market_value_test()
            growth_test = ratios.growth_rate_test(max_years, plot_graphs)

            if all(list(growth_test.values())):
                chosen_companies.append((company, ratios.growth.concatenate_ratios_average(max_years)))
        except KeyError:
            continue

    time.sleep(0.1)
    print("Analyze Completed")
    print("=============================")

    if plot_result:
        for tup in chosen_companies:
            print(tup[0] + ':')
            print(tup[1], '\n')

    chosen_companies = pd.DataFrame([x[1] for x in chosen_companies], index=[x[0] for x in chosen_companies])
    if save is not None:
        chosen_companies.to_excel(save)

    return chosen_companies
