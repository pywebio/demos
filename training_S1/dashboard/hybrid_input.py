from pywebio import *
from pywebio.output import *
from pywebio.input import *
from pywebio.pin import *

import threading
import pandas as pd
import plotly.express as px

def output_analysis(df, x_label, y_label, color_label="C"):
    try:
        with use_scope('plot', clear=True):
            with put_loading():
                fig = px.scatter(df, x=x_label, y=y_label, color=color_label, trendline='lowess')
                put_html(fig.to_html(include_plotlyjs="require", full_html=True))
    except: 
        toast('Some data points are not valid for plotting, select other columns', color='error', duration=6)

def auto_plot(df):
    while True:
        pin_wait_change(['x', 'y', 'legend'])
        output_analysis(df, pin.x, pin.y, pin.legend)

def main():
    path = 'data.csv'
    df = pd.read_csv(path)
    col_list = df.columns.values.tolist()

    # Grab user input   
    put_row([
        put_select('x', label='X column', options=col_list),
        None,
        put_select('y', label='Y column', options=col_list),
        None,
        put_select('legend', label='Legen column', options=col_list),
    ])
    
    #open a new thread to run the while-true loop
    plotting_thread = threading.Thread(target=auto_plot, kwargs={'df':df})
    session.register_thread(plotting_thread)
    plotting_thread.start()

    #add other functions to the app
    input('subscribe to receive plots once new data comes out')

    put_markdown('# Thanks you!')


if __name__ == '__main__':
    start_server(main, debug=True, port=8089)