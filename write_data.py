import pandas as pd

class Symbol:
    def __init__(self, name, high, low) -> None:
        self.symbol = name
        self.high = high
        self.low = low
        
        
data_list = [   # name,                  high,            low
                Symbol("BTC/USDT"       , 64715.3        , 56537.5 ),
                Symbol("ETH/USDT"       , 3287           , 2814),
                Symbol("DOGE/USDT"      , 0.17022        , 0.12003),
                Symbol("ADA/USDT"       , 0.47568        , 0.41769),
                Symbol("BNB/USDT"       , 604            , 536),
                Symbol("TRB/USDT"       , 98.800         , 44.121),
                Symbol("FTM/USDT"       , 0.7281         , 0.6090),
                Symbol("ONT/USDT"       , 0.4195         , 0.3251),
                Symbol("APT/USDT"       , 9.2983         , 8.1278),
                Symbol("INJ/USDT"       , 26.207         ,   21.901),
                Symbol("WLD/USDT"       , 5.8454         , 4.1743),
                Symbol("OP/USDT"        , 3.0383         , 2.2688),
                Symbol("SHIB/USDT"      , 0.000026307    , 0.000020493),
                Symbol("BCH/USDT"       , 480.25         , 399.41),
                Symbol("DOT/USDT"       , 7.410          , 6.026 ),
                Symbol("FRONT/USDT"     , 1.1729         , 0.7407),
                # Symbol("AVAX/USDT"      , 75.000         , 60.000),
                # Symbol("WIF/USDT"       , 0.0000000000001, 0.0000000000001),
                # Symbol("MATIC/USDT"     , 1.500          , 1.200),
]

data_frame = pd.DataFrame([vars(symbol) for symbol in data_list])
data_frame.to_csv("data.csv", index=False)
data_frame