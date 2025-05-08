# nb default colors for plots and excel
default_color1 = '#179297'
default_color2 = '#BFCE28'

sidebar_indicators2 = ["Fear & Greed", "Stock Market indicators", "Euribor rates, €STR & Key ECB interest rates",
"Property prices", "Inflation - Portugal", "Currency exchange rates", "Commodities"]

dashboard_main_title = "Market Risk Dashboard"

travel_logo_url = "https://raw.githubusercontent.com/TRAVEL-GVM/TRAVEL-MARKET-RISK/refs/heads/main/TRAVEL_Market_Risk/travel_logo.webp"

# Alphavantage API Key
alpha_api_key = 'EW4A338V8YGLZI3G'
# FRED API KEY
fred_api_key = 'eff3c719d275248bf5cdcfc836400e53'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
}

key_ecb_str = """
    <p>The Governing Council of the ECB sets the key interest rates for the euro area. These are as follows:</p>

    <h3>Deposit facility</h3>
    <p>The rate on the deposit facility, which banks may use to make overnight deposits with the Eurosystem at a pre-set interest rate. 
    The Governing Council decided in March 2024 to continue to steer the monetary policy stance through this rate.</p>

    <h3>Main refinancing operations</h3>
    <p>The interest rate on the main refinancing operations. In these operations banks can borrow funds from the ECB against broad collateral 
    on a weekly basis at a pre-determined interest rate. The rate is set above the deposit facility rate.</p>

    <h3>Marginal lending facility</h3>
    <p>The rate on the marginal lending facility, which offers overnight credit to banks against broad collateral at a pre-set interest rate. 
    The rate is set above the main refinancing operations rate.</p>
    """

sofr_str = """
    **SOFR - Secured Overnight Financing Rate**

    The **SOFR (Secured Overnight Financing Rate)** is a reference rate for short-term loans in the U.S. financial market.
     It reflects the cost of credit secured by high-quality assets, such as U.S. government securities, in overnight transactions. 
     The SOFR was introduced by the Federal Reserve (the U.S. central bank) as an alternative to **LIBOR** (London Interbank Offered Rate) 
     after LIBOR was affected by manipulation scandals and a loss of confidence in the rate-setting process.

    SOFR is calculated based on actual secured financing transactions, making it a more transparent and market-representative rate.
     It is used as a reference rate for various financial products, including loans, derivatives, and bonds. 
     SOFR reflects the financing costs in a highly liquid, low-risk market, providing a more stable and reliable rate for market participants.
    """

ir_str_str = """
**€STR - Euro Short Term Rate**

<p>
The €STR (Euro Short Term Rate) is the overnight euro money market reference rate and is also considered the euro risk-free interest rate. This rate was first published by the ECB, its administrator, on 2 October 2019.

The €STR is based on daily borrowing transactions in the euro unsecured overnight money market, with transactions not only in the interbank market, but also with financial entities other than banks, such as insurers, pension funds and money market funds. </p>
"""

cme_tool_str = f"""<h5 style=color:{default_color1}>What is the likelihood that the Fed will change the Federal target rate at upcoming FOMC meetings, according to interest rate traders?</h5>
Use CME FedWatch to track the probabilities of changes to the Fed rate, as implied by 30-Day Fed Funds futures prices.
<br><br>"""

euribor_str = """
The EURIBOR rates (short for Euro Interbank Offered Rate) are the benchmark rates of the euro money market for maturities ranging from one week to one year. 

These rates are also used as reference rates in a wide range of financial products, such as variable-rate housing loans and interest rate instruments (bonds and derivatives). They correspond to rates at which credit institutions in EU and EFTA countries can borrow in euro in the wholesale unsecured money market for the various maturities.

In August 2016, EURIBOR rates were declared a critical benchmark of systemic importance for the financial system by the European Commission.

The EURIBOR rates are calculated under a hybrid methodology which prioritises, where possible, the use of real transactions in the money market. When no transactions are conducted, the hybrid methodology relies on other market price sources and expert judgement to guarantee the robustness of rates.

The European Money Markets Institute (EMMI) is the administrator of these rates. This institute performs an annual assessment of the determination methodology for EURIBOR rates.

The EURIBOR rates are considered compliant with the EU Benchmark Regulation.

"""

inflation_str = """
**The Consumer Price Index (CPI)** measures inflation in Portugal based on a set of goods and services representative of the expenditure of resident households. 
The reference year of these time series is 2012.
"""

md_botao_cme = """
    <style>
        .center-button {
            display: flex;
            justify-content: center;
        }
    </style>
    <div class="center-button">
        <a href="https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html" target="_blank">
            <button>Click to open the CME FedWatch Tool</button>
        </a>
    </div>
"""

index_str = """

The elements shown in the image are benchmarks, meaning indices or ETFs that serve as performance references for specific markets or groups of assets. Here’s a brief explanation of each one:

- **MSCI World ETF:** A global benchmark that tracks the stocks of companies from developed countries.
- **STOXX50E:**  A benchmark index of the 50 largest companies in the Eurozone.
- **Euronext 100 Index:** Represents the top 100 companies listed on Euronext, one of the largest stock exchanges in Europe.
- **FTSE:** A benchmark index that tracks the largest companies listed on the London Stock Exchange.
- **S&P500 ETF:** Tracks the 500 largest companies in the U.S. and is used as a benchmark for the U.S. market.
- **PSI20 Index:** A benchmark index for the 20 largest companies in Portugal.

These indices serve as benchmarks to assess the performance of regional or global markets.
"""

vix_str = """
The **VIX, or Volatility Index**, is a real-time market index that represents the market's expectations for volatility over the next 30 days. 
It is often **referred to as the "fear gauge" because it reflects investor sentiment and uncertainty.**
The VIX is calculated using the prices of S&P 500 options and is expressed as an annualized percentage.

A higher VIX value suggests that investors expect significant market swings, often due to uncertainty or fear of a downturn.
Conversely, a lower VIX indicates a more stable market with lower anticipated volatility. While the VIX doesn't predict the market direction, it provides insights into how volatile traders think the market will be.
"""

fear_greed_str = """
The Fear and Greed Index is a sentiment indicator that measures the emotions driving the stock market.
It analyzes seven different factors, such as stock price momentum, market volatility, and trading volume, to gauge whether investors are feeling fearful or greedy.

A score close to 0 indicates extreme fear, suggesting that investors are cautious and more likely to sell,
potentially driving prices down. A score close to 100 indicates extreme greed, meaning investors are confident and likely to buy more, pushing prices higher.
The index helps traders understand market sentiment and identify potential buying or selling opportunities.
"""

warren_str = """
The Warren Buffett Indicator, also known as the "market cap to GDP ratio," compares the total market capitalization of a country's stock market to its gross domestic product (GDP).
It is often used to assess whether a stock market is overvalued or undervalued.

If the ratio is above 100%, it suggests that the stock market is overvalued relative to the economy, indicating potential for a correction. A ratio below 100% indicates that the market may be undervalued, presenting potential buying opportunities.
Investors use this indicator to evaluate whether market prices align with the underlying economic fundamentals, helping guide long-term investment decisions.
"""

resi_str = """
Residential property prices in Portugal and the Euro Area track the changes in the value of housing over time.
These indices measure the price trends of homes, helping investors, homeowners, and policymakers assess the real estate market's health and its potential for growth or correction.

Rising residential property prices indicate increasing demand and confidence in the housing market, which can be driven by factors like economic growth, low interest rates, and favorable borrowing conditions.
Falling prices may signal weakening demand or economic instability. 
Comparing property price trends between Portugal and the broader Euro Area allows for insights into regional economic differences, helping stakeholders make informed decisions about real estate investments and housing policies.
"""

cpp_str = """
Commercial property prices track the value of non-residential real estate, such as office buildings, retail spaces, and industrial properties. 
These prices reflect the demand for commercial spaces and are influenced by factors like economic growth, interest rates, and business investment.

Rising commercial property prices suggest strong demand for business infrastructure, often driven by economic expansion and increased corporate activity. 
Declining prices can indicate weaker economic conditions or reduced business confidence.
Investors and businesses monitor commercial property prices to assess the health of the real estate market and make informed decisions regarding investment in commercial real estate or leasing strategies.
"""