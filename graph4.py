import pandas as pd
import plotly.express as px

# hotel_bookings = pd.read_csv("hotel_bookings.csv")
# hotel_bookings = hotel_bookings[['country', 'is_canceled']]
# hotel_bookings['total_reservations'] = 1
# hotel_bookings['total_cancellations'] = 1
# hotel_bookings_by_country = pd.DataFrame(hotel_bookings[['country', 'total_reservations']].groupby("country").count())
# canceled = hotel_bookings[hotel_bookings["is_canceled"] == 1]
# canceled_by_country = pd.DataFrame(canceled[['country', 'total_cancellations']].groupby('country').count())
# hotel_bookings_by_country = hotel_bookings_by_country.join(canceled_by_country)
# hotel_bookings_by_country = hotel_bookings_by_country.fillna(0)
# hotel_bookings_by_country['cancellation_ratio'] = hotel_bookings_by_country['total_cancellations'] / hotel_bookings_by_country['total_reservations']


def get_cancellations_by_country(column, topX):
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
    hotel_bookings_by_country = hotel_bookings_by_country.sort_values(column, ascending=False).head(topX)
    fig = px.treemap(names=hotel_bookings_by_country.index,
                     path=[hotel_bookings_by_country.index],
                     values=hotel_bookings_by_country[column],
                     color=hotel_bookings_by_country[column])
    return fig


if __name__ == "__main__":
    get_cancellations_by_country("cancellation_ratio", 25).show()
