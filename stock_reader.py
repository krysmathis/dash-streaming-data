import datetime
import fix_yahoo_finance as yf
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


def get_yahoo_data(symbols, start_date, end_date):
    """Read stock data (adjusted close) for given symbols from CSV files."""

    dates = pd.date_range(start_date, end_date)
    df = pd.DataFrame(index=dates)
    
    includes_spy = True if 'SPY' in symbols else False
    
    if not includes_spy:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:

        print('getting data..' + symbol)
        df_yahoo = yf.download(symbol, start_date, end_date)
        df_yahoo = df_yahoo.rename(columns={'Adj Close': symbol})
        df_yahoo = df_yahoo[symbol]

        df = df.join(df_yahoo)
        
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])
        
    if not includes_spy: 
        symbols.remove('SPY')
    return df[symbols]

if __name__=="__main__":

    _symbols = ['SPY', 'XOM','GOOG','DG','GLD']

    start_date = datetime.today() - timedelta(days=720)
    start_date = start_date.strftime('%Y-%m-%d')

    end_date = datetime.today().strftime('%Y-%m-%d')
    end_date
    # df_test = yf.download('AAPL', start_date, end_date, usecols=['Adj Close'])
    panel_data = get_yahoo_data(_symbols, start_date, end_date)