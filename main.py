#This program asks for your workout and takes that text analzing it using
# Nutritionix API to get the values of the workout
# Then using Sheety API writes it onto a Google sheet
import requests
import datetime
from dotenv import load_dotenv
import os
load_dotenv()


# necessities for Nutritionix API
app_id = os.environ["APP_ID"]
nutri_key = os.environ["NUTRI_KEY"] = os.environ["NUTRI_KEY"]
exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
# necessities for sheety Api
sheety_url = "https://api.sheety.co/54b7524fcadb4bc6d5fd8dbf47a95eea/myWorkouts/workouts"
header = {"Authorization": os.environ["SHEETY_AUTH"]}
# header for nutri
headers = {
    "x-app-id": app_id,
    "x-app-key": nutri_key
}
# parameters for nutri asking for what exercises were done
# then sends it to their api and gets back a json with the
# information needed for the spreadsheet
parameters = {
    'query': input("What exercises did you do today? "),
    "gender": "Male",
    "weight_kg": "79",
    "height_cm": "177",
    "age": "24",
}
response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()

# Get today's date and time for the spread sheet
today = datetime.date.today().strftime("%d/%m/%Y")
time_rn = datetime.datetime.now().strftime("%H:%M")
# go through the json that was returned before and take the information it gave
# to add to the spread sheet using sheety
for activity in result["exercises"]:
    sheety_param = {
        "workout": {
            "date": today,
            "time": time_rn,
            "exercise": activity["name"].title(),
            "duration": activity["duration_min"],
            "calories": activity["nf_calories"]
        }

    }
    response = requests.post(url=sheety_url, headers=header, json=sheety_param)
    print(response.text)
