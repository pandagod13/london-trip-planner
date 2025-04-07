import streamlit as st
import requests

# Replace with your actual Google API key
GOOGLE_API_KEY = "AIzaSyCWqqJyD_7N7uQsfoajJRARmdvy-MXEvAA"

def get_nearby_places(location, place_type):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": location,
        "radius": 1500,
        "type": place_type,
        "key": GOOGLE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get('results', [])

def get_journey_data(from_location, to_lat_lng):
    url = f"https://api.tfl.gov.uk/journey/journeyresults/{from_location}/to/{to_lat_lng}"
    params = {
        "mode": "tube,overground"
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

# --- Streamlit UI ---
st.title("London Day Trip Route Planner")

# Step 1: User Location & Interest
user_location = st.text_input("Enter your current location (lat,lng)", value="51.5007,-0.1246")
place_type = st.selectbox("What kind of place are you looking for?", ["museum", "park", "cafe", "library", "art_gallery", "zoo"])

## ------------------------
# Initialize session state
# ------------------------
if "places" not in st.session_state:
    st.session_state.places = []
if "selected_place_index" not in st.session_state:
    st.session_state.selected_place_index = None
if "show_dropdown" not in st.session_state:
    st.session_state.show_dropdown = False
if "show_route" not in st.session_state:
    st.session_state.show_route = False

# ------------------------
# Step 1: Find Nearby Places
# ------------------------
if st.button("Find Nearby Places"):
    st.session_state.places = get_nearby_places(user_location, place_type)
    st.session_state.show_dropdown = True
    st.session_state.show_route = False  # Reset route view on new search
    st.session_state.selected_place_index = None

# ------------------------
# Step 2: Show Dropdown
# ------------------------
if st.session_state.show_dropdown and st.session_state.places:
    place_names = [
        f"{p['name']} - {p.get('vicinity', 'unknown')}"
        for p in st.session_state.places
    ]

    selected = st.selectbox(
        "Select a destination:",
        options=list(range(len(place_names))),
        format_func=lambda i: place_names[i],
        key="place_selector"
    )

    st.session_state.selected_place_index = selected

    # ------------------------
    # Step 3: Get Route
    # ------------------------
    if st.button("Get TfL Route"):
        st.session_state.show_route = True  # Persist flag to show route
        selected_place = st.session_state.places[selected]
        dest_coords = f"{selected_place['geometry']['location']['lat']},{selected_place['geometry']['location']['lng']}"
        st.session_state.destination_coords = dest_coords  # Save for rerun

# ------------------------
# Step 4: Display Route
# ------------------------
if st.session_state.show_route and "destination_coords" in st.session_state:
    data = get_journey_data(user_location, st.session_state.destination_coords)

    if "journeys" in data:
        journey = data["journeys"][0]
        display_journey(journey)
    else:
        st.error("TfL could not generate a route. Try a different location.")
