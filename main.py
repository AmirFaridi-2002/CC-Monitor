import pandas, ccxt, time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import requests, json, time, datetime, os, sys
import threading

from colorit import *
init_colorit()
def outp(text : str, c : str = 'green', endl : bool = True) -> None:
    """ Outputs a colored text """
    try: print(color(text, getattr(Colors, c)), end = "\n" if endl else "", flush = True)
    except: print(f'Invalid color: {c}\n Valid colors: {", ".join([i for i in dir(Colors) if not i.startswith("__")])}')
    
FIG_FLAG = True
DEFAULT_DF = pandas.DataFrame
DEFAULT_SYMBOLS = [symbol + "/USDT" for symbol in ['BTC', 'DOGE', 'ONT', 'FTM', 'APT', 'ETH', 'TRB', 'INJ', 'WLD', 'BNB', 'OP', 'SHIB', 'BCH', 'DOT']]
try: DEFAULT_DF = pandas.read_csv('data.csv')
except: raise FileNotFoundError("data.csv not found")

RESOLUTION = (1280, 720, 6)
FORMAT = 'png'
FORMATS = ['png', 'jpeg', 'webp', 'svg', 'pdf']
CHART_MUTEX = threading.Lock()       # Mutex lock for format and resolution

URL      = "https://api.telegram.org/bot6615328187:AAF_LGRnTJrmPJsh_A4xR6EIOmmJmsBGuPY"
ADMIN    = "1830034753"
AUTHORIZED = [ADMIN]
EXCHANGE = ccxt.bingx()

SYMBOLS  = []   # symbol, thread id pair
SYMBOLS_MUTEX = threading.Lock()

ALERTS   = []   # symbol, thread id pair
ALERTS_MUTEX = threading.Lock()

TOLERANCE = 0.05


def send_image(chat_id, img_path, caption):
    url = f"{URL}/sendPhoto"
    files = {'photo': open(img_path, 'rb')}
    data = {'chat_id' : chat_id, 'caption': caption}
    requests.post(url, files=files, data=data)
    
def send_message(chat_id, message):
    url = f"{URL}/sendMessage"
    data = {'chat_id' : chat_id, 'text': message}
    requests.post(url, data=data)
    
def send_file(chat_id, file_path, caption):
    url = f"{URL}/sendDocument"
    files = {'document': open(file_path, 'rb')}
    data = {'chat_id' : chat_id, 'caption': caption}
    requests.post(url, files=files, data=data)
    
def fetch_data(symbol : str = 'BTC/USDT', timeframe : str = '5m', limit : int = 100):
    try:
                data = EXCHANGE.fetch_ohlcv(symbol = symbol, timeframe = timeframe, limit = limit)
                data = pandas.DataFrame(data, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                data['timestamp'] = pandas.to_datetime(data['timestamp'], unit='ms')
                data['timestamp'] = data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                data.set_index('timestamp', inplace=True)
                return data
    except Exception as e:
                outp(text = e, c = 'red')
                return None
            
def get_weekly_map(symbol : str = 'BTC/USDT', flag : bool = True):
    """ flag: if set, fetch data from the default dataframe. Otherwise, fetch data from the exchange (This part is not implemented yet...) """
    if flag:
            high, upper_mid, mid, lower_mid, low = 0, 0, 0, 0, 0
            data = DEFAULT_DF[DEFAULT_DF['symbol'] == symbol]
            data = data.iloc[0]
                
    """ Weekly MAP calculation """
    high, low = data['high'], data['low']
    mid = (high + low) / 2
    upper_mid = (high + mid) / 2
    lower_mid = (low + mid) / 2
    return high, upper_mid, mid, lower_mid, low

def get_current_price(symbol : str = 'BTC/USDT'):
    data = fetch_data(symbol = symbol, timeframe = '1m', limit = 1)
    return data['close'].iloc[0]

def create_chart(symbol : str, data : pandas.DataFrame, high : int, low : int, 
                    mid : int, lower_mid : int, upper_mid : int, current_price : int, FIG_FLAG : bool = FIG_FLAG):
    # TODO : Implement matplotlib option
    """ If the flag is set, use go.Figure(). Otherwise, use matplotlib (Matplotlib option is not implemented yet...) """
    if FIG_FLAG:
                fig = go.Figure()
                fig.update_layout(width=1000, height=500)
                fig.add_trace(go.Candlestick(x=data.index, open=data['open'], high=data['high'], low=data['low'], close=data['close'], name = 'candlestick'))
                fig.add_hline(y=high, line_dash="dot", line_color="red", annotation_text="High", annotation_position="bottom right")
                fig.add_hline(y=mid, line_dash="dot", line_color="blue", annotation_text="Mid", annotation_position="bottom right")
                fig.add_hline(y=upper_mid, line_dash="dot", line_color="green", annotation_text="Upper Mid", annotation_position="bottom right")
                fig.add_hline(y=lower_mid, line_dash="dot", line_color="green", annotation_text="Lower Mid", annotation_position="bottom right")
                fig.add_hline(y=low, line_dash="dot", line_color="red", annotation_text="Low", annotation_position="bottom right")
                fig.add_hline(y=current_price, line_dash="dot", line_color="black", annotation_text="", annotation_position="bottom right")
                fig.update_layout(title_text=f"{symbol} Chart")
                fig.update_layout(hovermode="x unified")
                fig.update_layout(xaxis_rangeslider_visible=False)
                return fig

def remove_symbol(symbol):
    """ Remove a symbol from the lists """
    SYMBOLS_MUTEX.acquire()
    for idx in range(len(SYMBOLS)):
        if SYMBOLS[idx][0] == symbol:
            SYMBOLS.pop(idx)
            break
    SYMBOLS_MUTEX.release()
    
    ALERTS_MUTEX.acquire()
    for idx in range(len(ALERTS)):
        if ALERTS[idx][0] == symbol:
            ALERTS.pop(idx)
            break
    ALERTS_MUTEX.release()
    outp(text = f"Removed {symbol} from the list", c = 'orange')
    return

           
def send_details(symbol, timeframe, limit):
    data = fetch_data(symbol = symbol, timeframe = timeframe, limit = limit)
    outp(text = "fetched data. \t", c = "orange", endl = False)
    
    data = pandas.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    high, upper_mid, mid, lower_mid, low = get_weekly_map(symbol = symbol, flag = True if ARG == "import" else False)
    outp("fetched weekly map. \t", c = "orange", endl = False)
    
    current_price = get_current_price(symbol = symbol)
    outp("fetched current price. \t", c = "orange", endl = False)
    
    name = symbol.split('/')[0]
    
    # TODO : Check the flag and handle the matplotlib option
    fig = create_chart(symbol, data, high, low, mid, lower_mid, upper_mid, current_price)
    outp("created chart. \t", c = "orange", endl = False)
    
    fig.write_image(f"{name}.{FORMAT}", width=RESOLUTION[0], height=RESOLUTION[1], scale=RESOLUTION[2], engine="kaleido")
    outp("saved image. \t", c = "orange", endl = False)
    
    send_file(ADMIN, f"{name}.png", f"Symbol: {symbol}\nTimeframe: {timeframe}\nLimit: {limit}\nCurrent Price: {current_price}\nHigh: {high}\nUpper Mid: {upper_mid}\nMid: {mid}\nLower Mid: {lower_mid}\nLow: {low}")
    outp("sent image.", c = "orange")
    
    os.remove(f"{name}.png")
    return



def main(symbol):
    SYMBOLS_MUTEX.acquire()
    if symbol not in [pair[0] for pair in SYMBOLS]:
        SYMBOLS.append((symbol, threading.get_ident()))
        outp(text = f"Added {symbol} to the list", c = 'green')
    else:
        SYMBOLS_MUTEX.release()
        send_message(ADMIN, f"{symbol} is already in the list")
        outp(text = f"{symbol} is already in the list", c = 'orange')
        return
    SYMBOLS_MUTEX.release()
    
    high, upper_mid, mid, lower_mid, low = get_weekly_map(symbol = symbol, flag = True if ARG == "import" else False)
    tolerance_interval = (high - low) / 4 * TOLERANCE
    while True:
        try:
            SYMBOLS_MUTEX.acquire()
            if symbol not in [pair[0] for pair in SYMBOLS]:
                SYMBOLS_MUTEX.release()
                return
            SYMBOLS_MUTEX.release()
            
            current_price = get_current_price(symbol = symbol)
            
            if ((low - tolerance_interval <= current_price <= low + tolerance_interval) or (high - tolerance_interval <= current_price <= high + tolerance_interval)
                or (mid - tolerance_interval <= current_price <= mid + tolerance_interval) or (upper_mid - tolerance_interval <= current_price <= upper_mid + tolerance_interval)
                    or (lower_mid - tolerance_interval <= current_price <= lower_mid + tolerance_interval)):
                ALERTS_MUTEX.acquire()
                if (symbol, threading.get_ident()) not in ALERTS:
                    ALERTS.append((symbol, threading.get_ident()))
                ALERTS_MUTEX.release()
            else:
                ALERTS_MUTEX.acquire()
                if (symbol, threading.get_ident()) in ALERTS:
                    ALERTS.remove((symbol, threading.get_ident()))
                ALERTS_MUTEX.release()
        except Exception as e:
            outp(text = e, c = 'red')

            
""" TODO :
        - Add commands below
        /set_tolerance
        /set_resolution
        /set_format
        /set_chart  
"""
HELP = """
    Commands:
    /add <symbol> - Add a symbol to the list
    
    /remove <symbol> - Remove a symbol from the list
    
    /list_symbols - List all symbols
    
    /list_alerts - List all alerts
    
    /clear_symbols - Clear all symbols
    
    /clear_alerts - Clear all alerts
    
    /details <symbol> <timeframe> <limit> - Get details of a symbol (chart and whether it is in alerts list or not)
    
    /default_symbols - Adds default symbols to the list
        
    /help - Get help
    """

def run():
    outp(text = "Bot is running", c = 'purple')
    DEFAULT_SYMBOLS = DEFAULT_DF['symbol'].tolist()
    
    get_updates = URL + "/getUpdates"
    response = requests.get(get_updates + "?offset=-1")
    update_id = json.loads(response.text)["result"][0]["update_id"]
    while True:
        get_updates = URL + f"/getUpdates?offset={update_id + 1}"
        response = requests.get(get_updates)
        updates = json.loads(response.text)["result"]
        for update in updates:
            update_id = update["update_id"]
            message = update["message"]
            chat_id = message["chat"]["id"]
            text = message["text"]
            outp(text = f"Received message \"{text}\" from {chat_id}", c = 'blue')
            
            if str(chat_id) != ADMIN:
                send_message(chat_id, "You are not authorized to use this bot")
                continue
            
            if text.startswith("/add"):
                symbol = (text.split(" ")[1] + "/USDT").upper()
                threading.Thread(target = main, args = (symbol,)).start()
                send_message(chat_id, f"Added {symbol} to the list")
                
            elif text.startswith("/remove"):
                symbol = (text.split(" ")[1] + "/USDT").upper()
                threading.Thread(target = remove_symbol, args = (symbol,)).start()
            
            elif text == "/list_symbols":
                SYMBOLS_MUTEX.acquire()
                send_message(chat_id, f"Symbols: {', '.join([pair[0] for pair in SYMBOLS])}")
                SYMBOLS_MUTEX.release()
                
            elif text == "/list_alerts":
                ALERTS_MUTEX.acquire()
                send_message(chat_id, f"Alerts: {', '.join([pair[0] for pair in ALERTS])}")
                ALERTS_MUTEX.release()
                
            elif text == "/clear_symbols":
                SYMBOLS_MUTEX.acquire()
                SYMBOLS.clear()
                SYMBOLS_MUTEX.release()
                send_message(chat_id, "Cleared all symbols")
            
            elif text == "/clear_alerts":
                ALERTS_MUTEX.acquire()
                ALERTS.clear()
                ALERTS_MUTEX.release()
                send_message(chat_id, "Cleared all alerts")
                
            elif text.startswith("/details"):
                symbol, timeframe, limit = text.split(" ")[1:]
                symbol = (symbol + "/USDT").upper()
                threading.Thread(target = send_details, args = (symbol, timeframe, int(limit))).start()
                                
            elif text == "/help":
                send_message(chat_id, HELP)
            
            elif text == "/default_symbols":
                for symbol in DEFAULT_SYMBOLS:
                    threading.Thread(target = main, args = (symbol,)).start()
                send_message(chat_id, "Added default symbols to the list")               
                
            else:
                send_message(chat_id, "Invalid command")
                outp(text = "Invalid command", c = 'red')
                send_message(chat_id, HELP)

                


if __name__ == '__main__':
    # TODO : Currently, the only argument is 'import'. Implement other arguments
    if len(sys.argv) == 2:
        ARG = sys.argv[1]
        DEFAULT_SYMBOLS = DEFAULT_DF['symbol'].tolist() if ARG == 'import' else []
        if ARG == 'import': run()        
    else:   outp(text = "Invalid argument \nUsage: python main.py <import/optional>", c = 'red')
    
    # cd D:\workspace\Projects\; & ./venv/Scripts/activate; cd CC-Monitor
