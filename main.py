
import streamlit as st
import graph1
import graph2
import graph3
import graph4

st.set_page_config(layout="wide")


# Set up the app layout
st.title("Hotels Booking Cancellations")

st.header("Reservations and cancellations per month")
hotel, isCanceled = st.columns(2)
with hotel:
    hotel_selection = st.multiselect(
            "Select Hotel:",
            ['City Hotel', 'Resort Hotel']
        )

with isCanceled:
    isCanceled_radio = st.selectbox(
        "Select Canceled or Not Canceled:",
        ('All', 'Canceled', 'Not Canceled'),
        index=0
    )

if len(hotel_selection) == 0:
    hotel_selection = ['City Hotel', 'Resort Hotel']
if isCanceled_radio == 'Canceled':
    selected_graph1 = graph1.get_reservations_per_month_graph({"hotel": hotel_selection, "is_canceled": 1})
elif isCanceled_radio == 'Not Canceled':
    selected_graph1 = graph1.get_reservations_per_month_graph({"hotel": hotel_selection, "is_canceled": 0})
else:
    selected_graph1 = graph1.get_reservations_per_month_graph({"hotel": hotel_selection, "is_canceled": -1})


st.plotly_chart(selected_graph1, use_container_width=True)

st.header("Correlation between attributes and cancellations")
att_select, _ = st.columns(2)
attributes = ['lead_time', 'arrival_date_year', 'arrival_date_week_number',
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

st.plotly_chart(graph2.get_corr_heatmap(selected_attributes), use_container_width=True)

st.header("Reservations and cancellations days before arrival")
hist_select, _ = st.columns(2)

hists = ['Lead Days', 'Cancellation Days']
with hist_select:
    hists_selection = st.multiselect(
        "Select Histograms",
        hists
    )

if len(hists_selection) == 0:
    hists_selection = hists

hist, scatter = st.columns(2)

with hist:
    st.plotly_chart(graph3.get_cancellation_lead_hist(hists_selection), use_container_width=True)

with scatter:
    st.plotly_chart(graph3.get_cancellation_days_scatter(), use_container_width=True)

st.header("Reservations and cancellations per country")
country_count_slider, country_attribute_select = st.columns(2)
with country_count_slider:
    topX = st.slider("Number of counties to show:", min_value=5, max_value=50, step=5, value=25)
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

st.plotly_chart(graph4.get_cancellations_by_country(column, topX), use_container_width=True)

