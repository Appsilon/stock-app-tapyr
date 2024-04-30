from pathlib import Path

import pandas as pd
from faicons import icon_svg
from shiny import ui
from shinywidgets import output_widget

from stock_app_tapyr.logic.stocks import stocks

# Default to the last 6 months
end = pd.Timestamp.now()
start = end - pd.Timedelta(weeks=26)

app_dir = Path(__file__).parent


def get_dashboard_ui() -> ui.Tag:
    return ui.page_sidebar(
        ui.sidebar(
            ui.input_selectize("ticker", "Select Stocks", choices=stocks, selected="AAPL"),
            ui.input_date_range("dates", "Select dates", start=start, end=end),
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Current Price",
                ui.output_ui("price"),
                showcase=icon_svg("dollar-sign"),
            ),
            ui.value_box(
                "Change",
                ui.output_ui("change"),
                showcase=ui.output_ui("change_icon"),
            ),
            ui.value_box(
                "Percent Change",
                ui.output_ui("change_percent"),
                showcase=icon_svg("percent"),
            ),
            fill=False,
        ),
        ui.layout_columns(
            ui.card(
                ui.card_header("Price history"),
                output_widget("price_history"),
                full_screen=True,
            ),
            ui.card(
                ui.card_header("Latest data"),
                ui.output_data_frame("latest_data"),
            ),
            col_widths=[9, 3],
        ),
        title="Stock explorer",
        fillable=True,
    )
