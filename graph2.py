import pandas as pd
import plotly.express as px


hotel_bookings = pd.read_csv("hotel_bookings.csv")


def get_corr_heatmap(columns: list = None):
    df = hotel_bookings.copy()
    if columns is not None and len(columns) > 1:
        df = df[columns]

    corr = df.corr()
    fig = px.imshow(corr,
                    title="Attributes Correlation Matrix",
                    )
    return fig
