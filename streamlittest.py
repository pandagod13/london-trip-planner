import streamlit as st
import requests

def get_journey_data(from_location, to_location):
    url = f"https://api.tfl.gov.uk/journey/journeyresults/{from_location}/to/{to_location}"
    params = {
        "mode": "bus,tube,overground"
    }
    response = requests.get(url, params=params)
    return response.json()

def display_journey(journey):
    st.subheader("Trip Summary")
    st.write(f"Total Duration: {journey['duration']} minutes")

    st.subheader("Steps")
    for i, leg in enumerate(journey['legs'], 1):
        mode = leg['mode']['name']
        instruction = leg['instruction']['summary']
        duration = leg['duration']
        st.write(f"Step {i}: {mode.title()} - {instruction} ({duration} min)")

    if 'fare' in journey:
        st.subheader("Fare")
        total_cost = journey['fare']['totalCost'] / 100
        st.write(f"Estimated Fare: £{total_cost:.2f}")
        for fare in journey['fare'].get('fares', []):
            if fare.get('isHopperFare'):
                st.write("Hopper Fare Applied: Free second ride")

    st.subheader("Disruptions")
    disruptions = []
    for leg in journey['legs']:
        disruptions.extend(d.get('description') for d in leg.get('disruptions', []))
    if disruptions:
        for d in disruptions:
            st.write("-", d)
    else:
        st.write("None")

# Streamlit UI
st.title("London Day Trip Route Planner")

from_location = st.text_input("Enter your start location (lat,lng)", value="51.5007,-0.1246")
to_location = st.text_input("Enter your destination stop ID", value="1003794")

if st.button("Get Route"):
    data = get_journey_data(from_location, to_location)
    if 'journeys' in data:
        journey = data['journeys'][0]
        display_journey(journey)
    else:
        st.error("Could not find a valid route. TfL may need a more specific location.")
