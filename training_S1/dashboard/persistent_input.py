from pywebio import *
from pywebio.output import *
from pywebio.pin import *

import pandas as pd
import plotly.express as px

def output_analysis(df, x_label, y_label, color_label):
    with use_scope('plot', clear=True):
        fig = px.scatter(df, x=x_label, y=y_label, color=color_label, trendline='lowess')
        put_html(fig.to_html(include_plotlyjs="require", full_html=True))

def main():
    path = 'data.csv'
    df = pd.read_csv(path)
    col_list = df.columns.values.tolist()
    
    # Grab user input
    put_select(name='x', label='X column', options=col_list)
    put_select(name='y', label='Y column', options=col_list)
    put_select(name='legend', label='Legen column', options=col_list)

    while True:
        pin_wait_change(['x', 'y', 'legend'])
        output_analysis(df, pin.x, pin.y, pin.legend)

if __name__ == '__main__':
    start_server(main, debug=True, port=8089)