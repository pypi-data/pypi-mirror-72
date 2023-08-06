import pandas as pd
import requests
import requests_html
from bs4 import BeautifulSoup
import re
import string
import pandas
import plotly.graph_objs as go
import plotly.offline as offline_py
import numpy as np
import pandas_datareader.data as web

offline_py.init_notebook_mode(connected=True)

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

color_scheme = {
    'index': '#B6B2CF',
    'etf': '#2D3ECF',
    'tracking_error': '#6F91DE',
    'df_header': 'silver',
    'df_value': 'white',
    'df_line': 'silver',
    'heatmap_colorscale': [(0, '#6F91DE'), (0.5, 'grey'), (1, 'red')],
    'background_label': '#9dbdd5',
    'low_value': '#B6B2CF',
    'high_value': '#2D3ECF',
    'y_axis_2_text_color': 'grey',
    'shadow': 'rgba(0, 0, 0, 0.75)',
    'major_line': '#2D3ECF',
    'minor_line': '#B6B2CF',
    'main_line': 'black'}

def getSymbols(sector = 'ALL'):
    try:
        if sector == 'ALL':
            symbols = []
            url = 'https://www.set.or.th/set/commonslookup.do?language=th&country=TH&prefix={{key}}'
            key = ['NUMBER']
            key.extend(list(string.ascii_uppercase))
            for k in key:
                r = requests.get(url.replace('{{key}}',k), verify=False)
                soup = BeautifulSoup(r.content, "html.parser")
                for i in soup.findAll('a', href=re.compile('.*companyprofile.*')):
                    symbols.append(i.text)
            return symbols

        symbols = []
        url = 'https://marketdata.set.or.th/mkt/sectorquotation.do?sector=SET100&language=th&country=TH'
        if sector != 'SET100':
            url = url.replace('SET100', sector)
        r = requests.get(url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")
        for i in soup.findAll('a', href=re.compile('.*symbol.*')):
            symbols.append(i.text.strip())
        return symbols 
    finally:
        unwanted = {'ข้อมูลบริษัท/หลักทรัพย์', 'ข่าวบริษัท/หลักทรัพย์', 'ข่าววันนี้'}
        symbols = [ele for ele in symbols if ele not in unwanted]
        return symbols

def get_history_stock(set50_100, startdate, stopdate):
    dt=getSymbols(set50_100)
    aj_all_rows = pd.DataFrame()
    for n in dt:
        #print(n)
        aj_1=web.get_data_yahoo(("%s.BK" % n), start="2019-06-21", end="2020-06-21")
        aj_1.insert(0, 'Ticker', n)
        aj_all_rows = pd.concat([aj_all_rows, aj_1])
    return aj_all_rows

def resample_prices(close_prices, freq='M'):
    """
    Resample close prices for each ticker at specified frequency.
    
    Parameters
    ----------
    close_prices : DataFrame
        Close prices for each ticker and date
    freq : str
        What frequency to sample at
        For valid freq choices, see http://pandas.pydata.org/pandas-docs/stable/timeseries.html#offset-aliases
    
    Returns
    -------
    prices_resampled : DataFrame
        Resampled prices for each ticker and date
    """
    # TODO: Implement Function
    
    return close_prices.resample(freq).last()

def plot_resampled_prices(df_resampled, df, title):
    config = generate_config()
    layout = go.Layout(title=title)

    traces = _generate_traces([('monthly_close', df_resampled, color_scheme['major_line']), ('close', df, color_scheme['minor_line'])])

    offline_py.iplot({'data': traces, 'layout': layout}, config=config)

def generate_config():
    return {'showLink': False, 'displayModeBar': False, 'showAxisRangeEntryBoxes': True}

def _generate_traces(name_df_color_data):
    traces = []

    for name, df, color in name_df_color_data:
        traces.append(go.Scatter(
            name=name,
            x=df.index,
            y=df,
            mode='line',
            line={'color': color}))

    return traces

def _generate_stock_trace(prices):
    return go.Scatter(
        name='Index',
        x=prices.index,
        y=prices,
        line={'color': color_scheme['major_line']})

def plot_stock(prices, title):
    config = generate_config()
    layout = go.Layout(title=title)

    stock_trace = _generate_stock_trace(prices)

    offline_py.iplot({'data': [stock_trace], 'layout': layout}, config=config)

def compute_log_returns(prices):
    """
    Compute log returns for each ticker.
    
    Parameters
    ----------
    prices : DataFrame
        Prices for each ticker and date
    
    Returns
    -------
    log_returns : DataFrame
        Log returns for each ticker and date
    """
    
    log_returns = np.log(prices) - np.log(prices.shift(1))
    return log_returns

def plot_returns(returns, title):
    config = generate_config()
    layout = go.Layout(title=title)

    traces = _generate_traces([
        ('Returns', returns, color_scheme['major_line'])])

    offline_py.iplot({'data': traces, 'layout': layout}, config=config)

def shift_returns(returns, shift_n):
    """
    Generate shifted returns
    
    Parameters
    ----------
    returns : DataFrame
        Returns for each ticker and date
    shift_n : int
        Number of periods to move, can be positive or negative
    
    Returns
    -------
    shifted_returns : DataFrame
        Shifted returns for each ticker and date
    """
    # TODO: Implement Function
    #-----------------------------------------------------------------------------------
    # Ref Quiz: shift
    #-----------------------------------------------------------------------------------
    
    return returns.shift(shift_n)

def plot_shifted_returns(df_shited, df, title):
    config = generate_config()
    layout = go.Layout(title=title)

    traces = _generate_traces([
        ('Shifted Returns', df_shited, color_scheme['major_line']),
        ('Returns', df, color_scheme['minor_line'])])

    offline_py.iplot({'data': traces, 'layout': layout}, config=config)

def get_top_n(prev_returns, top_n):
    """
    Select the top performing stocks
    
    Parameters
    ----------
    prev_returns : DataFrame
        Previous shifted returns for each ticker and date
    top_n : int
        The number of top performing stocks to get
    
    Returns
    -------
    top_stocks : DataFrame
        Top stocks for each ticker and date marked with a 1
    """
    # TODO: Implement Function
    good_stocks = prev_returns.apply(lambda x: x.nlargest(top_n), axis=1)
    good_stocks = good_stocks.applymap(lambda x: 0 if pd.isna(x) else 1)
    good_stocks = good_stocks.astype(np.int64)

    return good_stocks

def print_top(df, name, top_n=10):
    print('{} Most {}:'.format(top_n, name))
    print(', '.join(df.sum().sort_values(ascending=False).index[:top_n].values.tolist()))

def portfolio_returns(df_long, df_short, lookahead_returns, n_stocks):
    """
    Compute expected returns for the portfolio, assuming equal investment in each long/short stock.
    
    Parameters
    ----------
    df_long : DataFrame
        Top stocks for each ticker and date marked with a 1
    df_short : DataFrame
        Bottom stocks for each ticker and date marked with a 1
    lookahead_returns : DataFrame
        Lookahead returns for each ticker and date
    n_stocks: int
        The number number of stocks chosen for each month
    
    Returns
    -------
    portfolio_returns : DataFrame
        Expected portfolio returns for each ticker and date
    """
    
    #print('long\n', df_long)
    #print('short\n', df_short)
    #print('lookahead\n', lookahead_returns)
    #print('n_stocks\n', n_stocks)
    
    portfolio = df_long - df_short
    portfolio_returns = portfolio * lookahead_returns / n_stocks
    
    print('portfolio_returns\n', portfolio_returns)
    
    return portfolio_returns

from scipy import stats

def analyze_alpha(expected_portfolio_returns_by_date):
    """
    Perform a t-test with the null hypothesis being that the expected mean return is zero.
    
    Parameters
    ----------
    expected_portfolio_returns_by_date : Pandas Series
        Expected portfolio returns for each date
    
    Returns
    -------
    t_value
        T-statistic from t-test
    p_value
        Corresponding p-value
    """
    null_hypothesis = 0.0
    t_statistic, p_value = stats.ttest_1samp(expected_portfolio_returns_by_date, null_hypothesis)
    # divide the p-value by 2 to get 1-sided p-value
    p_value = p_value / 2

    return t_statistic, p_value
