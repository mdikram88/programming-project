import requests

MY_LAT = 25.443920
MY_LONG = 81.825027


response = requests.get("http://api.open-notify.org/iss-now.json")
response.raise_for_status()

data = response.json()["iss_position"]
longitude = data["longitude"]
latitude = data["latitude"]
co_ord = longitude, latitude
print(co_ord)
