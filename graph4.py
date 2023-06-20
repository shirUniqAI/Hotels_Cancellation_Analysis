import pandas as pd
import plotly.express as px

hotel_bookings = pd.read_csv("hotel_bookings.csv")
hotel_bookings = hotel_bookings[['country', 'is_canceled']]
hotel_bookings['total_reservations'] = 1
hotel_bookings['total_cancellations'] = 1
hotel_bookings_by_country = pd.DataFrame(
    hotel_bookings[['country', 'total_reservations']].groupby("country").count())
canceled = hotel_bookings[hotel_bookings["is_canceled"] == 1]
canceled_by_country = pd.DataFrame(canceled[['country', 'total_cancellations']].groupby('country').count())
hotel_bookings_by_country = hotel_bookings_by_country.join(canceled_by_country)
hotel_bookings_by_country = hotel_bookings_by_country.fillna(0)
hotel_bookings_by_country['cancellation_ratio'] = hotel_bookings_by_country['total_cancellations'] / \
                                                  hotel_bookings_by_country['total_reservations']
sorted_by_reserv = hotel_bookings_by_country.sort_values("total_reservations", ascending=False).copy()
sorted_by_cancel = hotel_bookings_by_country.sort_values("total_cancellations", ascending=False).copy()
sorted_by_ratio = hotel_bookings_by_country.sort_values("cancellation_ratio", ascending=False).copy()


def get_cancellations_by_country(column, topX):
    if column == "total_reservations":
        fig = px.treemap(names=sorted_by_reserv.head(topX).index,
                         path=[sorted_by_reserv.head(topX).index],
                         values=sorted_by_reserv.head(topX)[column],
                         color=sorted_by_reserv.head(topX)[column],
                         color_continuous_scale='RdBu_r')
    elif column == "total_cancellations":
        fig = px.treemap(names=sorted_by_cancel.head(topX).index,
                         path=[sorted_by_cancel.head(topX).index],
                         values=sorted_by_cancel.head(topX)[column],
                         color=sorted_by_cancel.head(topX)[column],
                         color_continuous_scale='RdBu_r')
    else:
        fig = px.treemap(names=sorted_by_ratio.head(topX).index,
                         path=[sorted_by_ratio.head(topX).index],
                         values=sorted_by_ratio.head(topX)[column],
                         color=sorted_by_ratio.head(topX)[column],
                         color_continuous_scale='RdBu_r')
    return fig


if __name__ == "__main__":
    get_cancellations_by_country("total_reservations", 25).show()
