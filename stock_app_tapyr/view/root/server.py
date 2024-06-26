from pathlib import Path

import cufflinks as cf
import pandas as pd
import yfinance as yf
from faicons import icon_svg
from shiny import Inputs, Outputs, Session, reactive, render
from shinywidgets import render_plotly

# Default to the last 6 months
end = pd.Timestamp.now()
start = end - pd.Timedelta(weeks=26)

app_dir = Path(__file__).parent


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.calc
    def get_ticker():
        return yf.Ticker(input.ticker())

    @reactive.calc
    def get_data():
        dates = input.dates()
        return get_ticker().history(start=dates[0], end=dates[1])

    @reactive.calc
    def get_change() -> float:
        close = get_data()["Close"]
        return close.iloc[-1] - close.iloc[-2]

    @reactive.calc
    def get_change_percent():
        close = get_data()["Close"]
        change = close.iloc[-1] - close.iloc[-2]
        return change / close.iloc[-2] * 100

    @render.ui
    def price():
        close = get_data()["Close"]
        return f"{close.iloc[-1]:.2f}"

    @render.ui
    def change():
        return f"${get_change():.2f}"

    @render.ui
    def change_icon():
        change = get_change()
        icon = icon_svg("arrow-up" if change >= 0 else "arrow-down")
        icon.add_class(f"text-{('success' if change >= 0 else 'danger')}")
        return icon

    @render.ui
    def change_percent():
        return f"{get_change_percent():.2f}%"

    @render_plotly
    def price_history():
        qf = cf.QuantFig(
            get_data(),
            name=input.ticker(),
            up_color="#44bb70",
            down_color="#040548",
            legend="top",
        )
        qf.add_sma()
        qf.add_volume(up_color="#44bb70", down_color="#040548")
        fig = qf.figure()
        fig.update_layout(
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    @render.data_frame
    def latest_data():
        x = get_data()[:1].T.reset_index()
        x.columns = ["Category", "Value"]
        x["Value"] = x["Value"].apply(lambda v: f"{v:.1f}")
        return x
