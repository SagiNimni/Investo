from tqdm import tqdm
import time


def execute_analyze(financial_ratios, plot=False):
    print("=============================")
    print("Starts Analysis...")
    time.sleep(0.1)
    chosen_companies = []
    for company, ratios in tqdm(financial_ratios.items(), colour='white'):
        try:
            # ratios.liquidity_test()
            # ratios.leverage_test()
            # ratios.efficiency_test()
            # ratios.profitability_test()
            # ratios.market_value_test()
            growth_test = ratios.growth_rate_test(plot)

            if all(value[3] for value in growth_test.values()):
                chosen_companies.append(company)

        except KeyError:
            continue

    time.sleep(0.1)
    print("Analyze Completed")
    print("=============================")
    return chosen_companies

