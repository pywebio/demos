from pywebio import *
from pywebio.output import *
from pywebio.input import *

import pandas as pd
import plotly.express as px

def output_analysis():
    path = 'data.csv'
    df = pd.read_csv(path)
    fig = px.scatter(df, x='BATCH', y='SAMPLE', color='E', trendline='lowess')
    put_html(fig.to_html(include_plotlyjs="require", full_html=True))

def main():
    output_analysis()

if __name__ == '__main__':
    start_server(main, debug=True, port=8089)