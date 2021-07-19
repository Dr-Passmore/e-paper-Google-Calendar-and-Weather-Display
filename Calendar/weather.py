import requests
from datetime import datetime as dt
import math
from requests.api import options

#API and city info needed
#api_key = 'add your API here'
#city = 'CITY'
units = 'metric'
url = 'http://api.openweathermap.org/data/2.5/weather'

request = requests.get('{}?q={}&units={}&appid={}'.format(url, city, units, api_key))
        
data = request.json()

# Weather Description
description = data['weather'][0].get('description'),
print (description)

# Sunrise and Sunset.
sunrise = dt.fromtimestamp(data['sys'].get('sunrise')).strftime('%I:%M%p')
sunset  = dt.fromtimestamp(data['sys'].get('sunset')).strftime('%I:%M%p')
print("Today Sunrise - " + sunrise)
print ("Today Sunset - " + sunset)

# Temp
temp_min = int(math.ceil(data['main'].get('temp_min')))
temp_max = int(math.ceil(data['main'].get('temp_max')))
temp_curr = int(math.ceil(data['main'].get('temp')))
temp_feels = int(math.ceil(data['main'].get('feels_like')))

print ("Today min temp - ", temp_min)
print ("Today max temp - ", temp_max)
print ("Today current temp - ", temp_curr)
print ("Today feels like - ", temp_feels)
 
# Humidity
humidity = data['main'].get('humidity'),

print ("Humidity ", humidity)

# wind
direction = int(data['wind'].get('deg')),
speed = int(round(data['wind'].get('speed')))

print ("Wind direction - ", direction)
print ("Wind speed - ", speed)

#wind to cardinal directions
wind =int(direction[0])
print (wind)
val=int((wind/22.5)+.5)
arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]   
print (val)
cardinal =  arr[(val % 16)]
print (cardinal)

#get icon 
icon = data['weather'][0].get('icon')

