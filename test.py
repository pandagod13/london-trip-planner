import requests
import json  # just for pretty printing

url = "https://api.tfl.gov.uk/Line/Mode/tube/Status"
response = requests.get(url)

# Convert the response to a Python object (list of dictionaries)
data = response.json()

# # Print the name and status of each line
for line in data:
    # name = line['name']
    # status = line['lineStatuses'][0]['statusSeverityDescription']
    # print(f"{name}: {status}")
    for status in line['lineStatuses']:
        print(status['statusSeverityDescription'])



