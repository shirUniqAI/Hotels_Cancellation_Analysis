import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

hotel_bookings = pd.read_csv("hotel_bookings.csv")

def mtn(x):
    months = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    a = x.strip()[:3].lower()
    return months[a]


reservation_date = []
for i in hotel_bookings.index:
    reservation_date.append(datetime.date(hotel_bookings.at[i, "arrival_date_year"], mtn(hotel_bookings.at[i, "arrival_date_month"]), hotel_bookings.at[i, "arrival_date_day_of_month"]))
hotel_bookings["arrival_date"] = reservation_date

canceled = hotel_bookings[hotel_bookings["is_canceled"] == 1]
canceled[['arrival_date', 'reservation_status_date']] = canceled[['arrival_date', 'reservation_status_date']].apply(pd.to_datetime)
canceled["days_diff"] = (canceled["arrival_date"] - canceled["reservation_status_date"]).dt.days

hist_layout = go.Layout(
    title='Days before arrival of reservation and cancellation',
    xaxis=dict(
        title='Days',
        titlefont=dict(size=16, color='#000000'),
        tickfont=dict(size=14, color='#000000'),
    ),
    yaxis=dict(
        title='Amount',
        titlefont=dict(size=16, color='#000000'),
        tickfont=dict(size=14, color='#000000'),
        showgrid=True, gridwidth=0.2, gridcolor='#D7DBDD'
    ),
    legend=dict(
        x=1,
        y=1.0,
        bgcolor='white',
        bordercolor='black'
    ),
    plot_bgcolor='white',
    barmode="overlay",
    bargap=0.0,
    bargroupgap=0.0,
)


def get_cancellation_days_scatter():
    fig = px.scatter(x=canceled["lead_time"], y=canceled["days_diff"],
                     trendline="ols",
                     opacity=0.5,
                     trendline_color_override="red",
                     title="Cancellation and order days before arrival"
                     )
    fig.update_xaxes(title_text='Reservation days before arrival')
    fig.update_yaxes(title_text='Cancellation days before arrival')

    return fig


def get_cancellation_lead_hist(attributes):
    data = []
    if "Lead Days" in attributes:
        hist1 = go.Histogram(x=canceled["days_diff"],
                             xbins=go.histogram.XBins(size=10),
                             marker=go.histogram.Marker(color="orange"),
                             opacity=0.5,
                             name="Lead Days")
        data.append(hist1)
    if "Cancellation Days" in attributes:
        hist2 = go.Histogram(x=canceled["lead_time"],
                             xbins=go.histogram.XBins(size=10),
                             marker=go.histogram.Marker(color="blue"),
                             opacity=0.5,
                             name="Cancellation Days")
        data.append(hist2)
    fig = go.Figure(data=data, layout=hist_layout)
    return fig


if __name__ == "__main__":
    # get_cancellation_days_scatter().show()
    get_cancellation_lead_hist(["Lead Days", "Cancellation Days"]).show()