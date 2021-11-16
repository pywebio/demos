from pywebio import *
from pywebio.output import *
from pywebio.input import *

import pandas as pd
import plotly.express as px

def output_analysis(df, x_label, y_label, color_label):
    fig = px.scatter(df, x=x_label, y=y_label, color=color_label, trendline='lowess')
    put_html(fig.to_html(include_plotlyjs="require", full_html=True))

def main():
    path = 'data.csv'
    df = pd.read_csv(path)
    col_list = df.columns.values.tolist()

    # Grab user input
    plot_config = input_group("Select data to plot",[
        select(name='x', label='X column', options=col_list),
        select(name='y', label='Y column', options=col_list),
        select(name='legend', label='Legen column', options=col_list),
    ])
        
    output_analysis(df, plot_config['x'], plot_config['y'], plot_config['legend'])

if __name__ == '__main__':
    start_server(main, debug=True, port=8089)