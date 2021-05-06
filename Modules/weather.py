import http.client
from Modules.jsonHelper import readJ

def weather(city):
    conn = http.client.HTTPSConnection("api.collectapi.com")
    apikey = readJ("Databases/APIkey.json")
    headers = {
        'content-type': "application/json",
        'authorization': apikey['api_key']
        }

    conn.request("GET", f"/weather/getWeather?data.lang=tr&data.city={city.lower()}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    return data.decode("utf-8")
