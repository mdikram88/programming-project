import requests
import datetime as dt

PIXELA_USERNAME = "mdikram88"
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
PIXELA_TOKEN = "QWQfahugsd24acbSeqaerfnut"

GRAPH_ID = "graph1"
DATE = "20220417"

GRAPH_CREATE_ENDPOINT = f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs"
PIXEL_ENTRY_ENDPOINT = f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{GRAPH_ID}"
PIXEL_UPDATE_ENDPOINT = f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{GRAPH_ID}/{DATE}"
PIXEL_DELETE_ENDPOINT = f"{PIXELA_ENDPOINT}/{PIXELA_USERNAME}/graphs/{GRAPH_ID}/{DATE}"

user_params = {
    "token": PIXELA_TOKEN,
    "username": PIXELA_USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}
# response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
# print(response.text)

graph_creating_params = {
    "id": "graph1",
    "name": "Walking",
    "unit": "Kilometers",
    "type": "float",
    "color": "momiji"
}
headers = {
    "X-USER-TOKEN": PIXELA_TOKEN
}
# response = requests.post(url=GRAPH_CREATE_ENDPOINT, json=graph_creating_params, headers=headers)
# print(response.text)

date = dt.datetime.now()
formatted_date = date.strftime("%Y%m%d")
# print(formatted_date)

pixel_entry_param = {
    "date": formatted_date,
    "quantity": "5",
}

# response = requests.post(url=PIXEL_ENTRY_ENDPOINT, json=pixel_entry_param, headers=headers)
# print(response.text)

pixel_update_params = {
    "quantity": "4"
}

# response = requests.put(url=PIXEL_UPDATE_ENDPOINT, json=pixel_update_params, headers=headers)
# print(response.text)

response = requests.delete(url=PIXEL_DELETE_ENDPOINT, headers=headers)
print(response.text)