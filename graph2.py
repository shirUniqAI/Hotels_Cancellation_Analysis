import numpy as np
import pandas as pd
import plotly.express as px


hotel_bookings = pd.read_csv("hotel_bookings.csv")


def get_corr_heatmap(columns: list = None):
    df = hotel_bookings.copy()
    if "is_canceled" not in columns:
        columns.insert(0, "is_canceled")
    if columns is not None and len(columns) > 1:
        df = df[columns]
    corr = df.corr(numeric_only=True)
    fig = px.imshow(corr,
                    title="Attributes Correlation Matrix",
                    aspect="auto"
                    )
    return fig


if __name__ == "__main__":
    get_corr_heatmap().show()
