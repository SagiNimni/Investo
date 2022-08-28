`**STOCKS FILTER:**`

This section purpose is to find good stocks with the use of companies' fundamentals analyze.

The data is extracted from the 10K financial reports of the SEC(U.S. Securities and Exchange Commission)
using the sec-api.

**The code is divided into two main parts:**

* **The Data Extractor:**
  iterates through global stocks lists and converts their finencial reports into pandas dataframes to find a number possible 
  candidates for analyze. The extractor finds a number of stocks that pass the threshold conditions defined by user parameters:
    * minimum market cap
    * minimum volume
    * sectors 
    * price
    * quantity of stocks to find
   
   after finding enough stocks it extracts the 10K reports of these companies from the SEC and saves it in 
   a line for stocks pending for analyze.
  
 * **The Analyzer:**
 
    analyzes each stock from the list in the pending database. it checks few important parts from the data:
    
    
     * high and good consistency in the stock's financial over a long peroid of time
     
     * Balance sheet:
     
        1. growing retained earnings - in order to check the growth of the company
        2. low long term debt - to make sure the company manages it's lowns properly
       

     * Liquidity Ratios - measure a company’s capacity to meet its short-term obligations and are a vital
      indicator of its financial health:
              
            1. Current Ratio (Current Assets / Current Liabilities)- Measers how current assets of the company can settle
                current liabilities.
            2. Quick Ratio (Current Assets – Inventories / Current Liabilities)- Measers the abillity to pay for liabiliteis
                with more liquid assets.
            3. Cash Ratio (Cash and cash equivalents / Current Liabilities) - Measers how quickly can a company settle current
                obligations
      
      * Leverage Ratios - measure how much debt a company has
      
            1. Debt Ratio (Total Debt / Total Assets)- high debt ratio indicates that a company is highly leveraged. 
            2. Debt To Equity Ratio (Total Debt / Total Equity)- This ratio is important for investors because debt obligations 
                often have a higher priority if a company goes bankrupt meaning the investent is high risk.
            3. Interest coverage ratio (Operating income / Interest expenses)- The ability of a company to pay their interest on time 
                and keep some extra cash for providing the product. a low ratio means the company struggles with payments
            
       *  Efficiency Ratios - how effectively a company uses working capital to generate sales
        
            1. Inventory Turnover(Cost of goods sold / Average inventory) - measeres how often inventory is replaced
            2. Assets Turnover Ratio(Net sales / Average total assets) - how much sales are made from assets
            3. Days sales in inventory ratio (365 days / Inventory turnover ratio)- how long a business holds inventories before 
                they are converted to finished products or sold to customers.
            4. Payables turnover ratio (net credit purchases / Average Accounts Payable)- The payables turnover ratio calculates how 
                quickly a business pays its suppliers and creditors.
            5. Days payables outstanding (Average Accounts Payable / Cost of Goods Sold)- This ratio shows how many days it takes a 
                company to pay off suppliers and vendors.
            6. Receivables turnover ratio (Net credit sales / Average accounts receivable)- The receivables turnover ratio helps 
                companies measure how quickly they turn customers’ invoices into cash
        
        * Profitability ratios - measure how a company generates profits using available resources over a given period:
            
            1. Gross Margin(Gross profit / Net sales)- measures how much profit a business makes after the
                cost of goods and services compared to net sales.
            2. Operating Margin(Operating income / Net sales) - measures how much profit a company generates from net sales
                after the oprating expenses
            3. Return on Assets(Net income / Total assets) - determine how much profits they generate from total assets or resources,
            4. Return on equity(Net income / Total equity) - measures how much profit a business generates from shareholders’ equity
        
       * Market Value Ratios- measers how valuable a company acctualy is:
            
            1. Earning Per Share Ratio(Net earnings / Total shares outstanding) - shows how much profit is attributable 
                to each company share.
            2. Price Earning Ratio(Share price / Earnings per share) - The PE ratio is a key investor ratio that measures how valuable
                a company is relative to its book value earnings per share.
            3. Book Value Per Share Ratio(Total Shareholder Equity / Total shares outstanding) - This ratio helps determine wheter 
                the company is overvalued or undervalued
            4. Dividend Yield Ratio( Dividend per share / Share price) - measures the value of a company’s dividend per 
                share compared to the market share price
   
   
   
   keep in mind that the analyzer and extractor works in parallel for efficacy. Once a stock gets in the pending line
   the analyzer immediately starts to analyze it and moves it either the the chosen stocks database or deletes it.