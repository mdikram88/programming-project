import requests
import datetime

APPLICATION_ID = "3674a83a"
API_KEY = "802ae675806a764b1b0fedd8d1e8f5e6"
API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEET_ENDPOINT = "https://api.sheety.co/3e1c37848fe1aadca4eb14ef010bf0fd/myWorkoutsPython/workouts"
SHEET_TOKEN = "bWRpa3JhbTg4OjEyMzQ1Njc4OTA"
SHEET_USERNAME = "mdikram88"
SHEET_PASSWORD = "1234567890"

GENDER = "female"
WEIGHT_KG = "50"
HEIGHT_CM = "177"
AGE = "22"

# Getting Current Time
time = datetime.datetime.now().time()
format_time = time.strftime("%H:%M:%S")
# print(format_time)

# Getting Current Date
date = datetime.datetime.now().date()
format_date = date.strftime("%d/%m/%Y")
# print(format_date)

sentence = input("Tell me Which exercise you did?  ")

query_params = {
    "query": sentence,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

headers = {
    "x-app-id": APPLICATION_ID,
    "x-app-key": API_KEY,
}

# Getting transformed data from nutritionix
response = requests.post(url=API_ENDPOINT, json=query_params, headers=headers)
exercises = response.json()["exercises"]
# print(entry_record["exercises"])


# Getting Data from Google Sheets
# response = requests.get(url=SHEET_ENDPOINT, auth=(SHEET_USERNAME, SHEET_PASSWORD))
# print(response.text)

sheet_headers = {"Authorization": f"Basic {SHEET_TOKEN}"}

for exercise in exercises:
    sheet_inputs = {
            "workout": {
                "date": format_date,
                "time": format_time,
                "exercise": exercise["name"].title(),
                "duration": int(exercise["duration_min"]),
                "calories": int(exercise["nf_calories"])
            }
        }

    response = requests.post(url=SHEET_ENDPOINT, json=sheet_inputs, headers=sheet_headers)
    print(response.status_code)
