import datetime
import pandas as pd
import plotly.express as px

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
lead_days = canceled[["lead_time"]].rename({"lead_time": "Days"}, axis=1)
lead_days["source"] = "Lead Days"
cancellation_days = canceled[["days_diff"]].rename({"days_diff": "Days"}, axis=1)
cancellation_days["source"] = "Cancellation Days"

final_df = pd.concat([lead_days, cancellation_days])

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
    fig = px.histogram(data_frame=final_df[final_df["source"].isin(attributes)], x="Days", color="source",
                       opacity=0.5, title="Lead and cancellation days before arrival",
                       color_discrete_map={"Cancellation Days": 'red', "Lead Days": 'blue'}
                       )
    fig.update_xaxes(title_text="Days")
    fig.update_yaxes(title_text="Amount")
    return fig


if __name__ == "__main__":
    # get_cancellation_days_scatter().show()
    get_cancellation_lead_hist(["Lead Days", "Cancellation Days"]).show()