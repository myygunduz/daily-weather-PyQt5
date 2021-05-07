import requests
from Modules.jsonHelper import readJ
import json
def weather(city):
    apikey = readJ("Databases/Jsons/APIkey.json")
    headers = {
        'content-type': "application/json",
        'authorization': apikey['api_key']
        }

    response = requests.get(f"https://api.collectapi.com/weather/getWeather?data.lang=tr&data.city={city.lower()}",headers=headers).json()

    return response
