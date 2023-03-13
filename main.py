# ----------------------------------- TERMINAL INSTALL REQUIREMENTS -----------------------------------
# pip install mysql-connector-python

# ----------------------------------- IMPORTS -----------------------------------
import requests
from bs4 import BeautifulSoup
import time

# ----------------------------------- GET LATITUDE AND LONGITUDE OF ALL US STATES -----------------------------------
URL = "https://www.latlong.net/category/states-236-14.html" # This site has a list of latitude and longitude of all 50 US States
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")
table = soup.find("table") # Webscrape the table from the website

# Iterate through each row and get either header or row values to webscrape the table:
header = []
rows = []
for i, row in enumerate(table.find_all('tr')):
    if i == 0:
        header = [el.text.strip() for el in row.find_all('th')]
    else:
        rows.append([el.text.strip() for el in row.find_all('td')])

states = {
    "location": [],
    "latitude": [],
    "longitude": []
}

for row in rows: # Append the broken up table into an organized dictionary
    states["location"].append(row[0])
    states["latitude"].append(row[1])
    states["longitude"].append(row[2])

# Remove the extra information at the end of the state names
for i in range(0, len(states["location"])):

    state = states["location"][i]
    if ", USA" in state:
        state = state.split(", USA")[0]
    elif ", the USA" in state:
        state = state.split(", the USA")[0]
    elif ", USA" in state:
        state = state.split(", USA")[0]
    elif ", the US" in state:
        state = state.split(", the US")[0]
    else:
        pass
    states["location"][i] = state

# ----------------------------------- SEND API REQUEST TO OPEN-METEO WEATHER API TO GET EACH STATE'S TEMPERATURE -----------------------------------
endpoint = "https://api.open-meteo.com/v1/forecast"

usa_states_temp = [] # Create a new list to have the (state name, state temperature)

print("Hang tight, the API call will take ~1 min to receive all of the state's temperature data")

for i in range(0, len(states["location"])): # Iterate through each state's latitude & longitude to get the state's current temperature in farenheight
    params = {
        "latitude": states["latitude"][i],
        "longitude": states["longitude"][i],
        "current_weather": True,
        "temperature_unit": "fahrenheit"
    }

    response = requests.get(url=endpoint, params=params) # Do a get request to fetch the temperature data
    response.raise_for_status()
    weather_data = response.json() # Receive the data from the API call

    state_temperature = weather_data["current_weather"]["temperature"] # Get the temperature for the specific state
    usa_states_temp.append((states['location'][i], state_temperature)) # Append the (state, state temperature)

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
#   password="***"
# )

cursor = db.cursor()
cursor.execute("DROP DATABASE IF EXISTS usa_weather") # If the database already exists, delete it and create a new database
cursor.execute("CREATE DATABASE usa_weather")
cursor.execute("USE usa_weather")
cursor.execute("CREATE TABLE usa_temperature (location VARCHAR(255), temperature VARCHAR(5))")

query = "INSERT INTO usa_temperature (location, temperature) VALUES (%s, %s)"
cursor.executemany(query, usa_states_temp)
db.commit()

print("The data has now been sent to the database: 'usa_weather', table name: 'usa_temperature' in MySQL")

