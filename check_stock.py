from pywebio import *
from pywebio.output import *
from pywebio.input import *

import pandas as pd
import yfinance as yf
import plotly.express as px


def analysis_html(stock_ticker):
    
    df = yf.Ticker(stock_ticker).history(period='1d', interval='1m')
    #plot data
    fig = px.line(df[['Close']], title=stock_ticker)
    
    #add upper and lower control limits
    fig.add_hline(df.Close.quantile(0.95), line_width=1)
    fig.add_hline(df.Close.mean(), line_width=2, line_dash="dash")
    fig.add_hline(df.Close.quantile(0.05), line_width=1)
    fig.add_hrect(y0=df.Close.quantile(0.68),
                  y1=df.Close.quantile(0.32),
                  line_width=0, fillcolor="green", opacity=0.1)
    #move legend inside plot
    fig.update_layout( # customize font and legend orientation & position
        font_family="Rockwell",
        legend=dict(
            title=None, orientation="h", y=1, yanchor="bottom", x=0.5, 
            xanchor="center"
        )
    )
    #convert px fig to html format, easy to be added to website
    return fig.to_html(include_plotlyjs="require", full_html=True)

def main():
    session.set_env(title='Check stock price')
    ticker = input('Input a stock ticker, and see latest data', 
                   help_text='try TSLA or AAPL')
    put_markdown('# 👋 Hi there! Check your stock.')
    #put_text(ticker)
    #put_row([
    #    put_html(analysis_html('INTC')),
    #    put_html(analysis_html('TSLA')), 
    #    ])
    put_collapse(ticker, [
    put_html(analysis_html(ticker))], open=True)
