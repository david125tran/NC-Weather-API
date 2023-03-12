# ----------------------------------- INSTALL REQUIREMENTS -----------------------------------
# pip install mysql-connector-python

# ----------------------------------- IMPORTS -----------------------------------
import requests
from bs4 import BeautifulSoup
import time

# ----------------------------------- LATITUDE AND LONGITUDE OF NC CITIES -----------------------------------
URL = "https://www.mapsofworld.com/usa/states/north-carolina/lat-long.html" # This site has a list of latitude and longitude of NC cities
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
table = soup.find('div', class_="table-scroll")
# Iterate through each row and get either header or row values to webscrape the table:
header = []
rows = []
for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])
rows.pop(0)  # Remove the 1st empty list entry

nc_cities = {
    "location": [],
    "latitude": [],
    "longitude": []
}

for row in rows: # Append the broken up table into an organized dictionary
    nc_cities["location"].append(row[0])
    nc_cities["latitude"].append(row[1])
    nc_cities["longitude"].append(row[2])

# ----------------------------------- SEND API REQUEST TO FREE WEATHER API -----------------------------------
endpoint = "https://api.open-meteo.com/v1/forecast"

nc_cities_weather = {
    "location": [],
    "temperature": []
}

print("Hang tight, the API call will take ~10 mins to receive the temperature of the 739 NC cities")

for i in range(0, 5): #len(nc_cities["location"])   # REPLACE THIS WITH 5 LATERda
    params = {
        "latitude": nc_cities["latitude"][i],
        "longitude": nc_cities["longitude"][i],
        "current_weather": True,
        "temperature_unit": "fahrenheit"
    }

    response = requests.get(url=endpoint, params=params)
    response.raise_for_status()
    weather_data = response.json() # Receive the data from the API call

    city_temperature = weather_data["current_weather"]["temperature"] # Get the temperature for the specific city
    nc_cities_weather["location"].append(nc_cities["location"][i]) # Append the city name and current temperature to a new list
    nc_cities_weather["temperature"].append(city_temperature)

print(nc_cities_weather)

import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)
