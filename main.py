# ----------------------------------- TERMINAL INSTALL REQUIREMENTS -----------------------------------
# pip install mysql-connector-python

# ----------------------------------- IMPORTS -----------------------------------
import requests
from bs4 import BeautifulSoup
import time

# ----------------------------------- GET LATITUDE AND LONGITUDE OF ALL NC CITIES -----------------------------------
URL = "https://www.mapsofworld.com/usa/states/north-carolina/lat-long.html" # This site has a list of latitude and longitude of NC cities
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
table = soup.find('div', class_="table-scroll") # Webscrape the table from the website

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

# Remove the extra information at the end of the city name (For example, 'Aberdeen town' turns into 'Aberdeen')
for i in range(0, len(nc_cities["location"])):
    city = nc_cities["location"][i]
    if " city" in city:
        city = city.split(" city")[0]
    elif " City" in city:
        city = city.split(" City")[0]
    elif " town" in city:
        city = city.split(" town")[0]
    elif " village" in city:
        city = city.split(" village")[0]
    elif " Village" in city:
        city = city.split(" Village")[0]
    else:
        pass
    nc_cities["location"][i] = city

# ----------------------------------- SEND API REQUEST TO OPEN-METEO WEATHER API TO GET CITY TEMPERATURE -----------------------------------
endpoint = "https://api.open-meteo.com/v1/forecast"

nc_cities_temp = [] # Create a new list to have the (city name, city temperature)

print("Hang tight, the API call will take ~10 mins to receive the temperatures of the 739 NC cities")

for i in range(0, len(nc_cities["location"])): # Iterate through each city's latitude & longitude to get the city's current temperature in farenheight
    params = {
        "latitude": nc_cities["latitude"][i],
        "longitude": nc_cities["longitude"][i],
        "current_weather": True,
        "temperature_unit": "fahrenheit"
    }

    response = requests.get(url=endpoint, params=params) # Do a get request to fetch the temperature data
    response.raise_for_status()
    weather_data = response.json() # Receive the data from the API call

    city_temperature = weather_data["current_weather"]["temperature"] # Get the temperature for the specific city
    nc_cities_temp.append((nc_cities['location'][i], city_temperature)) # Append the (city, city temperature) to nc_cities_temp

# ----------------------------------- CONNECT TO MySQL TO STORE THE DATA IN A DATABASE -----------------------------------
import mysql.connector

# To find out your MySQL 'host' and 'user' type this in the MySQL workbench:
# SELECT user();
# It will return the 'host' and 'username' in this format:
# user@host
# For example: root@local host where 'root' is the 'user' and 'localhost' is the 'host'

db = mysql.connector.connect(
  host="Your Hostname", # Replace this with your hostname
  user="Your Username", # Replace this with your username
  password="Your Password" # Replace this with your password
)

# The following is my credentials:
# db = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="******"
# )

cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS nc_weather") # If the database already exists, delete it and create a new database
cursor.execute("CREATE DATABASE nc_weather")
cursor.execute("USE nc_weather")
cursor.execute("CREATE TABLE weather (location VARCHAR(255), temperature VARCHAR(5))")

query = "INSERT INTO weather (location, temperature) VALUES (%s, %s)"
cursor.executemany(query, nc_cities_temp)
db.commit()

print("The data has now been sent to the database: 'nc_weather', table name: 'weather' in MySQL")

