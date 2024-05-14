"""
    Manually write data in the list and run the script to generate the csv file.
    The csv file will be used to read the data in the main script.
"""
import pandas as pd

class Symbol:
    def __init__(self, name, high, low) -> None:
        self.symbol = name
        self.high = high
        self.low = low
        
        
data_list = [   # name,                  high,            low
                Symbol("BTC/USDT"       , 65514        , 60141 ),
                Symbol("ETH/USDT"       , 3221           , 2878),
                Symbol("DOGE/USDT"      , 0.16914        , 0.13915),
                Symbol("ADA/USDT"       , 0.47515        , 0.43300),
                Symbol("BNB/USDT"       , 606            , 573),
                # Symbol("TRB/USDT"       , 98.800         , 44.121),
                Symbol("FTM/USDT"       , 0.7495         , 0.6503),
                # Symbol("ONT/USDT"       , 0.4195         , 0.3251),
                # Symbol("APT/USDT"       , 9.2983         , 8.1278),
                Symbol("INJ/USDT"       , 26.989         ,   22.802),
                Symbol("WLD/USDT"       , 6.5342         , 5.2089),
                # Symbol("OP/USDT"        , 3.0383         , 2.2688),
                # Symbol("SHIB/USDT"      , 0.000026307    , 0.000020493),
                # Symbol("BCH/USDT"       , 480.25         , 399.41),
                Symbol("DOT/USDT"       , 7.472          , 6.539 ),
                # Symbol("FRONT/USDT"     ,          , ),
                # Symbol("AVAX/USDT"      , 75.000         , 60.000),
                Symbol("WIF/USDT"       , 3.6803         , 2.7358),
                # Symbol("MATIC/USDT"     , 1.500          , 1.200),
]

data_frame = pd.DataFrame([vars(symbol) for symbol in data_list])
data_frame.to_csv("data.csv", index=False)
data_frame