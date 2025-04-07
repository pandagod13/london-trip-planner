import requests

from_location = "51.5007,-0.1246"  # Real Big Ben coords
to_location = "1003794"            # British Museum Stop ID

url = f"https://api.tfl.gov.uk/journey/journeyresults/{from_location}/to/{to_location}"
params = {
    "mode": "bus,tube,overground"
}

response = requests.get(url, params=params)
data = response.json()

if 'journeys' in data:
    journey = data['journeys'][0]
    legs = journey['legs']
    
    print("🧭 Trip from Big Ben to British Museum")
    print(f"🕒 Total Duration: {journey['duration']} minutes\n")

    for i, leg in enumerate(legs, 1):
        mode = leg['mode']['name']
        instruction = leg['instruction']['summary']
        duration = leg['duration']
        emoji = "🚶" if mode == "walking" else "🚌"
        print(f"Step {i}: {emoji} {instruction} ({duration} min)")

    print("\n💰 Fare Info:")
    if 'fare' in journey:
        total_cost = journey['fare']['totalCost'] / 100  # fare is in pennies
        print(f"  Total: £{total_cost:.2f}")
        if journey['fare'].get('fares'):
            for fare in journey['fare']['fares']:
                if fare.get('isHopperFare'):
                    print("  🟢 Hopper Fare Applied (Free second ride)")

    # Show planned disruptions
    print("\n⚠️ Disruptions:")
    found_disruptions = False
    for leg in legs:
        for disruption in leg.get('disruptions', []):
            found_disruptions = True
            print(f"- {disruption['description']}")
    if not found_disruptions:
        print("None 🎉")

else:
    print("TfL did not return journey data.")
    print("Status code:", response.status_code)
    print("Response:", data)
