
import streamlit as st
import pandas as pd
import graph1
import graph2
import graph3
from PIL import Image


from plotly.subplots import make_subplots

import graph4

st.set_page_config(layout="wide")


# Set up the app layout
st.title("Hotels Booking Cancellations")

hotel, isCanceled = st.columns(2)
with hotel:
    hotel_selection = st.multiselect(
            "Select Hotel:",
            ['City Hotel', 'Resort Hotel']
        )

with isCanceled:
    isCanceled_radio = st.selectbox(
        "Select Canceled or Not Canceled:",
        ('Canceled', 'Not Canceled'),
        index=0
    )

if len(hotel_selection) == 0:
    hotel_selection = ['City Hotel', 'Resort Hotel']
if isCanceled_radio == 'Canceled':
    selected_graph1 = graph1.get_reservations_per_month_graph({"hotel": hotel_selection, "is_canceled": 1})
elif isCanceled_radio == 'Not Canceled':
    selected_graph1 = graph1.get_reservations_per_month_graph({"hotel": hotel_selection, "is_canceled": 0})
else:
    selected_graph1 = graph1.get_reservations_per_month_graph({"hotel": hotel_selection})


st.plotly_chart(selected_graph1, use_container_width=True)


att_select, heatmap = st.columns(2)
attributes = ['lead_time', 'arrival_date_year',
       'arrival_date_month', 'arrival_date_week_number',
       'arrival_date_day_of_month', 'stays_in_weekend_nights',
       'stays_in_week_nights', 'adults', 'children', 'babies',
       'is_repeated_guest', 'previous_cancellations',
       'previous_bookings_not_canceled', 'booking_changes', 'agent',
       'company', 'days_in_waiting_list', 'adr',
       'required_car_parking_spaces', 'total_of_special_requests']
with att_select:
    selected_attributes = st.multiselect(
            "Select Attributes",
            attributes)
if len(selected_attributes) == 0:
    selected_attributes = attributes
with heatmap:
    st.plotly_chart(graph2.get_corr_heatmap(selected_attributes))


hist_select, hist, scatter = st.columns(3)

hists = ['Lead Days', 'Cancellation Days']
with hist_select:
    hists_selection = st.multiselect(
        "Select Histograms",
        hists
    )

if len(hists_selection) == 0:
    hists_selection = hists
with hist:
    st.plotly_chart(graph3.get_cancellation_lead_hist(hists))

with scatter:
    st.plotly_chart(graph3.get_cancellation_days_scatter())


country_count_slider, country_attribute_select = st.columns(2)
with country_count_slider:
    topX = st.slider("Number of counties to show:", min_value=5, max_value=50, step=5)
with country_attribute_select:
    column = st.selectbox(
        "Select attribute to show:",
        ("Amount of Reservations", "Amount of Cancellations", "Cancellations Ratio")
    )
    if column == "Amount of Reservations":
        column = "total_reservations"
    elif column == "Amount of Cancellations":
        column = "total_cancellations"
    else:
        column = "cancellation_ratio"

country_plot = st.columns(1)

with country_plot:
    st.plotly_chart(graph4.get_cancellations_by_country(column, topX))

