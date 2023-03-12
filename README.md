# NC-Weather-API  
About:  
  
This project sends calls to a free weather API https://open-meteo.com/ to get the current temperature (F) of all NC cities.  The API call requires a latitude & longitude of each city which I get by using BeautifulSoup webscraper to scrape into a list from https://www.mapsofworld.com/usa/states/north-carolina/lat-long.html  
  
I then take the city name & current temperature and send it to a database in MySQL.  

Instructions:  
  
Install MySQL: https://dev.mysql.com/downloads/installer/
Run main.py in a python IDE such as PyCharm.  
In the PyCharm terminal type the following: pip install mysql-connector-python  
In main.py, replace "host", "user", and "password" entries with your own unique MySQL information to connect to MySQL.  
The API call will take about 10 minutes to finish getting all NC cities current temperature
To see the database, open MySQL Workbench.  In the workbench, type the following:

SHOW databases;
USE nc_weather;
SHOW TABLES;
SELECT * FROM weather;
