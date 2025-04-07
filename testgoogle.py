

import requests
import math

GOOGLE_API_KEY = "AIzaSyCWqqJyD_7N7uQsfoajJRARmdvy-MXEvAA"

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

params = {
    "location": "51.5007,-0.1246",  # Big Ben
    "radius": 1000,
    "type": "museum",
    "key": GOOGLE_API_KEY
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


response = requests.get(url, params=params)
data = response.json()

# for place in data['results']:
#     print(place['name'], "-", place.get("vicinity", "No address"))

places = data.get('results', [])
# Filter out ones without a rating
rated_places = [p for p in places if 'rating' in p]

# Sort them by rating, descending
sorted_places = sorted(rated_places, key=lambda x: x['rating'], reverse=True)

# Display top 5
for place in sorted_places[:5]:
    print(f"{place['name']} ({place['rating']}⭐) - {place.get('vicinity', 'No address')}")

user_lat, user_lng = 51.5007, -0.1246  # Big Ben

for place in sorted_places[:5]:
    name = place['name']
    rating = place['rating']
    address = place.get('vicinity', 'No address')

    open_now = place.get('opening_hours', {}).get('open_now', True)
    types = place.get('types', [])
    lat = place['geometry']['location']['lat']
    lng = place['geometry']['location']['lng']
    distance = haversine_distance(user_lat, user_lng, lat, lng)


    print(f"{name} ({rating}⭐) - {address}")
    print(f"  Type: {types}")
    print(f"  Open: {open_now}")
    print(f"  ~{int(distance)}m away\n")
    
