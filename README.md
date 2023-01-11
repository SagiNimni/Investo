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
   
* **GUI:**
    The program also provides a GUI that the user can use to run analayzers maualuy and watch their results in charts. And watch the protfolio managed by the Bot.
   
* **Server:**
    The server will let the user access the bot remotely from cellphone or PC (HTML view) and check on it's decisions. The server and client communication is encrypted and protected by password.
    

**`Thechnical info`:**
* The Investment Bot and Market Analayzers are provided by a python library called InvestoAnalayzers.

* The GUI is built in .NET WPF framework so in order to connect the C# Desktop App with the python library we will use the IronPython compiler instead of the default Cpython interpreter.

* The website is only used for get requests and is built with Flask server as backend, React node server as frontend and nginx serves as reverse proxy server. 
all of these are connected in a docker container.

* For maximum efficiency the AI of the market analyzer
 should study with GPU and run on FPGA.