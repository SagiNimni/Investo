`**STOCKS FILTER:**`

This section purpose is to find good stocks with the use of companies' fundamentals analyze.

The data is extracted from the 10K financial reports of the SEC(U.S. Securities and Exchange Commission)
using the sec-api.

**The code is divided into two main parts:**

* **The Data Extractor:**
  iterates through global stocks lists to find a number possible candidates for analyze. The extractor finds 
  a number of stocks that pass the threshold conditions defined by user parameters:
    * minimum market cap
    * minimum volume
    * sectors 
    * price
    * quantity of stocks to find
   
   after finding enough stocks it extracts the 10K reports of these companies from the SEC and saves it in 
   a line for stocks pending for analyze.
  
 * **The Analyzer:**
 
    analyzes each stock from the list in the pending database. it checks few important parts from the data:
    
    
     * high and good consistency in the stock financial over a few years
     
     Income Statment:
      
        * Good Gross margin- the profit divided by revenue (over 40% is strong)
      
        * Good Net margin- the net income divided by revenue (over 20% is strong)
     
     Balance Sheet:
     
        * Growing retained earnings(Money that the company keeps in order to keep expanding)
        
        * good ROE(return on equity) which tells us how good the company uses it's money
        
        * Low long term debt (how money years would it take for a company to pay all it's debt)
       
     Cash Flow:
        
        * Low net income devided by capital expenditure (less than 25% is good less than 50% is acceptable)
          but be aware of expections like one time investments to grow the buisness        
          
        * Low PE(price to earning) ratio suggesting that the stock is not overbought.
    
   
   
   
   keep in mind that the analyzer and extractor works in parallel for efficacy. Once a stock gets in the pending line
   the analyzer immediately starts to analyze it and moves it either the the chosen stocks database or deletes it.