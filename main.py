import argparse
import dash
import yfinance as yf
import plotly.graph_objs as go
import pandas as pd

from dash import dcc, html
from dash.dependencies import Input, Output


def fetch_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df


def create_candlestick_chart(df):
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close']
            )
        ]
    )
    fig.update_layout(title='S&P 500 Candlestick Chart', xaxis_rangeslider_visible=False)
    return fig


def main():
    parser = argparse.ArgumentParser(description="Shows S&P 500 Candlestick Chart within ")
    parser.add_argument("-s", "--start", help="The first date to show (YYYY-MM-DD)", default="1990-01-01")
    parser.add_argument("-e", "--end", help="The last day to show (YYYY-MM-DD)", default="today")
    args = parser.parse_args()

    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1('S&P 500 Candlestick Chart'),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=pd.to_datetime(args.start).date(),
            end_date=pd.to_datetime(args.end).date(),
            display_format='YYYY-MM-DD'
        ),
        dcc.Graph(id='candlestick-chart'),
    ])

    @app.callback(
        Output('candlestick-chart', 'figure'),
        [Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')]
    )
    def update_graph(start_date, end_date):
        df = fetch_data('^GSPC', start_date, end_date)
        fig = create_candlestick_chart(df)
        return fig

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
