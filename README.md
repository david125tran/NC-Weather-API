# US-Weather-API  
******************************About******************************
  
This project sends calls to a free weather API https://open-meteo.com/ to get the current temperature (F) of all 50 US states.  The API call requires a latitude & longitude of each state which I get by using BeautifulSoup webscraper to scrape into a list from https://www.latlong.net/category/states-236-14.html  

I then take the state name & current temperature and send it to a database in MySQL.  

******************************Instructions******************************
  
Install MySQL: https://dev.mysql.com/downloads/installer/
Run main.py in a python IDE such as PyCharm.  
In the PyCharm terminal type the following: pip install mysql-connector-python  
In main.py, replace "host", "user", and "password" entries with your own unique MySQL information to connect to MySQL.  
The API call will take about 10 minutes to finish getting all NC cities current temperature
To see the database, open MySQL Workbench.  In the workbench, type the following and hit execute:

SHOW databases;  
USE usa_weather;  
SHOW TABLES;  
SELECT * FROM usa_temperature;  
  
To find out your MySQL 'host' and 'user' type this in the MySQL workbench and execute:  
SELECT user();  
It will return the 'host' and 'user' in this format:  
user@host  
For example: root@local host where 'root' is the user and 'localhost' is the host
