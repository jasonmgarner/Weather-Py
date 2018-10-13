%matplotlib inline

# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
from config import api_key
import json

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


## Generate Cities List

# Starting URL for Weather Map API Call
base_url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" 

Query_url = base_url + api_key + "&q="
#print(base_url)
#print(Query_url)

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the [city count to confirm sufficient count
len(cities)



## Perform API Calls

Results = []
City_Name = []
Country = []
Latitude = []
Humidity = []
Max_Temperature = []
Cloudiness = []
Wind_Speed = []
Date_Time = []
Longitude = []

for city in cities:
   
    print(f"Retrieving record for {city}:")   
    response = requests.get(Query_url + city).json()
    City_ID = response.get("id")
    if response.get("id"):
        print(f"     Record found for City: {city}    City ID: {City_ID}")
        Results.append(response)
        Latitude.append(response['coord']['lat'])
        Longitude.append(response['coord']["lon"])
        Max_Temperature.append(response['main']['temp_max'])
        Humidity.append(response['main']['humidity'])
        Cloudiness.append(response['clouds']['all'])
        Wind_Speed.append(response['wind']['speed'])
        City_Name.append(response['name'])
        Country.append(response['sys']['country'])
        Date_Time.append(response["dt"])
        
    else:
        print(f"     No information found for city: {city}")
          
print("---------------------------------------")
print("Data Retrieval Complete")

Weather_Dict = {"City": City_Name, "Country": Country, "Latitude": Latitude, "Longitude": Longitude,
                "Max_Temperature": Max_Temperature,
                "Humidity": Humidity,
                "Cloudiness": Cloudiness,
                "Wind_Speed": Wind_Speed}

Weather_Data = pd.DataFrame(Weather_Dict)
Weather_Data = Weather_Data[["City", "Country", "Latitude", "Longitude", "Max_Temperature", "Humidity", "Cloudiness", "Wind_Speed"]]
Weather_Data.head()


print(Query_url)

Weather_Data.to_csv("Weather_Data.csv")

Above = Weather_Data.loc[Weather_Data['Latitude'] > 0]
Below = Weather_Data.loc[Weather_Data['Latitude'] < 0]

Above_Equator = len(Above)
Below_Equator = len(Below)

print(f'There are {Above_Equator} sample cities above the equator and {Below_Equator} sample cities below the equator')

Date = Date_Time[0]
Time_Stamp = time.strftime("%Z - %Y/%m/%d, %H:%M:%S", time.localtime(float(Date)))

# * Sample City Latitude and Longitude

Wind_Lat = plt.scatter(Weather_Data["Longitude"], Weather_Data["Latitude"], c="blue", 
                       marker="o", s=15, edgecolors="black", alpha=0.75)
plt.title(f"Sample City Longitude and Latitude {Time_Stamp}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.style.use('ggplot')
plt.yticks(np.arange(-80, 120, 20))
plt.xticks(np.arange(-180, 210, 30))
plt.axhline(linewidth=2, color='r')

plt.savefig("Sample City Latitude and Longitude.png")

# * Temperature (F) vs. Latitude

Temp_Lat = plt.scatter(Weather_Data["Latitude"], Weather_Data["Max_Temperature"], c="blue", 
                       marker="o", s=10, edgecolors="black", alpha=1)
plt.title(f"City Latitude vs. Max Temperature {Time_Stamp}")
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")
plt.tight_layout()
plt.style.use('ggplot')
plt.xticks(np.arange(-80, 120, 20))
plt.yticks(np.arange(0, 140, 20))

plt.savefig("City Latitude vs Max Temp.png")


# * Humidity (%) vs. Latitude

Hum_Lat = plt.scatter(Weather_Data["Latitude"], Weather_Data["Humidity"], c="blue", 
                      marker="o", s=20, edgecolors="black", alpha=0.95,)
plt.title(f"City Latitude vs. Humidity {Time_Stamp}")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.style.use('ggplot')
plt.xticks(np.arange(-80, 120, 20))
plt.yticks(np.arange(-20, 140, 20))

plt.savefig("City Latitude vs Humidity.png")


# * Cloudiness (%) vs. Latitude

Cloud_Lat = plt.scatter(Weather_Data["Latitude"], Weather_Data["Cloudiness"], c="blue", 
                        marker="o", s=10, edgecolors="black", alpha=1)
plt.title(f"City Latitude vs. Cloudiness {Time_Stamp}")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.tight_layout()
plt.style.use('ggplot')
plt.xticks(np.arange(-80, 120, 20))
plt.yticks(np.arange(-20, 140, 20))

plt.savefig("City Latitude vs Cloudiness.png")


# * Wind Speed (mph) vs. Latitude

Wind_Lat = plt.scatter(Weather_Data["Latitude"], Weather_Data["Wind_Speed"], c="blue", 
                       marker="o", s=15, edgecolors="black", alpha=0.75)
plt.title(f"City Latitude vs. Wind Speed {Time_Stamp}")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")
plt.style.use('ggplot')
plt.xticks(np.arange(-80, 120, 20))
plt.yticks(np.arange(-5, 45, 5))

plt.savefig("City Latitude vs Wind Speed.png")

# OBSERVATIONS:

#  1. Finding average or max yearly temperature and comparing to latitude would be 
#     interesting to graph when looking at this question. Depending on the time of year the current
#     data is pulled would slighlty modify these graphs depending on current which season is currently going on.

#  2. Latitude appeared to be important when looking at temperature, but wind speed 
#     and cloudiness did not to seem as critical to latitude 

#  3. For this given date sample, humidity appears to peak around 20-40 degrees of away 
#     from the equator, with a minimal amount of humidity noted closest to the equator
