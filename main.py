import requests
import math
import os
import json

GOOGLE_API_KEY = "AIzaSyCWqqJyD_7N7uQsfoajJRARmdvy-MXEvAA"

url = "https://maps.googleapis.com/maps/api/geocode/json"

# params = {
#     "location": "51.5007,-0.1246",  # Big Ben
#     "radius": 1000,
#     "type": "museum",
#     "key": GOOGLE_API_KEY
# }

class location():
    def __init__(self):
        self.name = ""
        self.lat = 0.0
        self.lng = 0.0
    
    def get_coordinates(self,location_name):
        geocode_url = url
        geocode_params = {"address": location_name,
                          "key" : GOOGLE_API_KEY}
        try:
            response =requests.get(geocode_url, params = geocode_params)
            if response.status_code == 200:
                try: 
                    data = response.json()
                    # print("API response:", data) 
                    if data["results"]:
                        location = data["results"][0]["geometry"]["location"]
                        self.lat = location["lat"] 
                        self.lng = location["lng"]  
                        location = [self.lat, self.lng]
                        print(f"coordinates for {location_name}: Latitude = {self.lat} Longitude = {self.lng} {location} ")
                    else:
                        print("No results found")
                except json.JSONDecodeError:
                    print("Error: unable to parse JSON response.")
                    print("Raw Response Text:", response.text)
            else:
                print(f"Error: Received status code {response.status_code}")
                print("raw response text", response.text)
        except requests.RequestException as e:
            print(f"Error: unable to complete the request. {e}")
        return location

    def get_location(self):
        self.location_name = input("Enter location :")
        return self.location_name
    
class direction():
    def __init__(self, start, end):
        self.current_location = start
        self.destination = end

    def get_tfl_routes(self):
        tfl_url = f"https://api.tfl.gov.uk/journey/journeyresults/{self.current_location[0]},{self.current_location[1]}/to/{self.destination[0]},{self.destination[1]}"
        tfl_params = { "mode": "bus, tube, overground"}
        try:
            response = requests.get(tfl_url, params= tfl_params)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data["journeys"]:
                        return print(json.dumps(data, indent=4)) 
                    else:
                        print("No results found")
                except json.JSONDecodeError:
                    print("Error: unable to parse JSON request.")
                    print("raw response text", response.text)
            else:
                print(f"Error: received status code {response.status_code}")
                print("raw response text", response.text)
        except requests.RequestException as e:
            print(f"Error: unable to complete request. {e}")

        
        

user_location = location()
user_destination = location()
start = user_location.get_coordinates(user_location.get_location())
end = user_destination.get_coordinates(user_destination.get_location())
route = direction(start,end)
route.get_tfl_routes()


