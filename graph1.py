import datetime

import pandas as pd
import plotly.graph_objs as go

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

city_hotel = hotel_bookings[hotel_bookings["hotel"] == "City Hotel"]
resort_hotel = hotel_bookings[hotel_bookings["hotel"] == "Resort Hotel"]

city_hotel_all = city_hotel.groupby("arrival_date_month").count()
city_hotel_all = city_hotel_all.reindex(sorted(city_hotel_all.index, key=lambda x: mtn(x)))
city_hotel_canceled = city_hotel[city_hotel["is_canceled"] == 1].groupby("arrival_date_month").count()
city_hotel_canceled = city_hotel_canceled.reindex(sorted(city_hotel_canceled.index, key=lambda x: mtn(x)))
city_hotel_not_canceled = city_hotel[city_hotel["is_canceled"] == 0].groupby("arrival_date_month").count()
city_hotel_not_canceled = city_hotel_not_canceled.reindex(sorted(city_hotel_not_canceled.index, key=lambda x: mtn(x)))
scatter_city_all = go.Scatter(x=city_hotel_all.index, y=city_hotel_all["hotel"], name="City Hotel", marker=dict(color='blue'))
scatter_city_canceled = go.Scatter(x=city_hotel_canceled.index, y=city_hotel_canceled["hotel"], name="City Hotel", marker=dict(color='blue'))
scatter_city_not_canceled = go.Scatter(x=city_hotel_not_canceled.index, y=city_hotel_not_canceled["hotel"], name="City Hotel", marker=dict(color='blue'))

resort_hotel_all = resort_hotel.groupby("arrival_date_month").count()
resort_hotel_all = resort_hotel_all.reindex(sorted(resort_hotel_all.index, key=lambda x: mtn(x)))
resort_hotel_canceled = resort_hotel[resort_hotel["is_canceled"] == 1].groupby("arrival_date_month").count()
resort_hotel_canceled = resort_hotel_canceled.reindex(sorted(resort_hotel_canceled.index, key=lambda x: mtn(x)))
resort_hotel_not_canceled = resort_hotel[resort_hotel["is_canceled"] == 0].groupby("arrival_date_month").count()
resort_hotel_not_canceled = resort_hotel_not_canceled.reindex(sorted(resort_hotel_not_canceled.index, key=lambda x: mtn(x)))
scatter_resort_all = go.Scatter(x=resort_hotel_all.index, y=resort_hotel_all["hotel"], name="Resort Hotel", marker=dict(color='orange'))
scatter_resort_canceled = go.Scatter(x=resort_hotel_canceled.index, y=resort_hotel_canceled["hotel"], name="Resort Hotel", marker=dict(color='orange'))
scatter_resort_not_canceled = go.Scatter(x=resort_hotel_not_canceled.index, y=resort_hotel_not_canceled["hotel"], name="Resort Hotel", marker=dict(color='orange'))

layout = go.Layout(
    title='Amount of reservations per month',
    xaxis=dict(
        title='Month',
        titlefont=dict(size=16, color='#000000'),
        tickfont=dict(size=14, color='#000000'),
    ),
    yaxis=dict(
        title='Amount of reservations',
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
    barmode='group',
    bargap=0.15,
    bargroupgap=0.1
)


def get_reservations_per_month_graph(filters: dict = None):
    data = []
    if filters is not None:
        if "is_canceled" in filters:
            if filters["is_canceled"] == 1:
                city_plot = scatter_city_canceled
                resort_plot = scatter_resort_canceled
            else:
                city_plot = scatter_city_not_canceled
                resort_plot = scatter_resort_not_canceled
        else:
            city_plot = scatter_city_all
            resort_plot = scatter_resort_all
        if "hotel" in filters:
            if "City Hotel" in filters["hotel"]:
                data.append(city_plot)
            if "Resort Hotel" in filters["hotel"]:
                data.append(resort_plot)
        else:
            data.append(city_plot)
            data.append(resort_plot)
    else:
        data = [scatter_city_all, scatter_resort_all]
    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == "__main__":
    get_reservations_per_month_graph({"hotel": ['City Hotel', 'Resort Hotel'], "is_canceled": 1}).show()
