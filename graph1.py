import datetime

import pandas as pd
import plotly.express as px

hotel_bookings = pd.read_csv("hotel_bookings.csv")


def sort_months(ser):
    res = []
    for m in ser:
        res.append(mtn(m))
    return pd.Series(res)


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


# reservation_date = []
# for i in hotel_bookings.index:
#     reservation_date.append(datetime.date(hotel_bookings.at[i, "arrival_date_year"], mtn(hotel_bookings.at[i, "arrival_date_month"]), hotel_bookings.at[i, "arrival_date_day_of_month"]))
# hotel_bookings["arrival_date"] = reservation_date

hotel_bookings["count"] = 1
city_hotel = hotel_bookings[hotel_bookings["hotel"] == "City Hotel"][["arrival_date_month", "count", "is_canceled"]]
resort_hotel = hotel_bookings[hotel_bookings["hotel"] == "Resort Hotel"][["arrival_date_month", "count", "is_canceled"]]

city_hotel_all = city_hotel[["arrival_date_month", "count"]].groupby("arrival_date_month").count().reset_index()
city_hotel_all["source"] = "City Hotel All"
city_hotel_canceled = city_hotel[city_hotel["is_canceled"] == 1][["arrival_date_month", "count"]].groupby("arrival_date_month").count().reset_index()
city_hotel_canceled["source"] = "City Hotel Canceled"
city_hotel_not_canceled = city_hotel[city_hotel["is_canceled"] == 0][["arrival_date_month", "count"]].groupby("arrival_date_month").count().reset_index()
city_hotel_not_canceled["source"] = "City Hotel Not Canceled"

resort_hotel_all = resort_hotel[["arrival_date_month", "count"]].groupby("arrival_date_month").count().reset_index()
resort_hotel_all["source"] = "Resort Hotel All"
resort_hotel_canceled = resort_hotel[resort_hotel["is_canceled"] == 1][["arrival_date_month", "count"]].groupby("arrival_date_month").count().reset_index()
resort_hotel_canceled["source"] = "Resort Hotel Canceled"
resort_hotel_not_canceled = resort_hotel[resort_hotel["is_canceled"] == 0][["arrival_date_month", "count"]].groupby("arrival_date_month").count().reset_index()
resort_hotel_not_canceled["source"] = "Resort Hotel Not Canceled"

final_df = pd.concat([city_hotel_all.reset_index(), city_hotel_canceled.reset_index(), city_hotel_not_canceled.reset_index(),
                      resort_hotel_all.reset_index(), resort_hotel_canceled.reset_index(), resort_hotel_not_canceled.reset_index()])
final_df = final_df.sort_values("arrival_date_month", key=lambda x: sort_months(x))


def get_reservations_per_month_graph(filters: dict = None):
    sources = []
    if 'City Hotel' in filters['hotel']:
        if filters['is_canceled'] == 1:
            sources.append('City Hotel Canceled')
        elif filters['is_canceled'] == 0:
            sources.append('City Hotel Not Canceled')
        else:
            sources.append('City Hotel All')
    if 'Resort Hotel' in filters['hotel']:
        if filters['is_canceled'] == 1:
            sources.append('Resort Hotel Canceled')
        elif filters['is_canceled'] == 0:
            sources.append('Resort Hotel Not Canceled')
        else:
            sources.append('Resort Hotel All')

    fig = px.line(final_df[final_df['source'].isin(sources)], x="arrival_date_month", y="count", color="source")
    fig.update_xaxes(title="Month")
    fig.update_yaxes(title="Amount")
    return fig

if __name__ == "__main__":
    get_reservations_per_month_graph({"hotel": ['City Hotel', 'Resort Hotel'], "is_canceled": 1}).show()
