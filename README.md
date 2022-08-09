**`_INVESTO_`**

Investo is project designed to analyze the stock market and invest wisely in the long term. This project is divided into four main parts 
each responsible for a different task:

* **Market Analyzer:**
    Looks for good stocks by analyzing financial reports like the 10K and finding companies with good fundamentals. 
    After finding a bunch of decent stocks it starts a technical analysis on their graphs and indicators using AI.
    And with a combination of news and market sentiments it spits out the probability for each stock to rise or fall.

* **Investment Bot:**
    This is the bot that actually makes trades using the Interactive Brokers API. It makes decision using the info provided
    by the market analyzer. The user defines how much money the bot is allowed and should ask permission in order to make transactions.
   
* **interactive GUI:**
    The program also provides a GUI that shows what transactions have been made. it helps manage the protfolio profits or losses
    and analyzes the efficiency of the algorithm.
   
* **Server:**
    The server will let the user access the bot remotely from cellphone and check on it's decision and give 
    permission for transactions. The server and client communication is encrypted and protected by password.
    

**`Thechnical info`:**
 The program is writen in python and the GUI is writen in Unity(C#). For maximum efficiency the AI of the market analyzer
 should study with GPU and run on FPGA.