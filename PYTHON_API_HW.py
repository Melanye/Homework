
# coding: utf-8

# In[15]:


import json
import requests as req
from citipy import citipy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns
import numpy as np


# In[13]:


base_url = 'http://api.openweathermap.org/data/2.5/weather'
APIKEY = 'ad3eeb24a921df30f22dd6e80a21583f'


# __cities = []
# query_units = 'imperial'
# weather_info = []
# __max_temp = []
# __humidity = []
# __wind_speed = []
# __lon = []
# __lat = []
# __cloudiness  = []
# __qcities  = []
# __country = []
# __date = []

# In[5]:


num_query=1500
name=[]
cod=[]
lt=180 * np.random.random_sample((num_query)) - 90 #latitude [-90, 90)
lg=360 * np.random.random_sample((num_query)) - 180 #longtitude [-180, 180)
geo_coord=list(zip(lt,lg))

for lat, lon in geo_coord:
    city=citipy.nearest_city(lat, lon)
    name.append(city.city_name)
    cod.append(city.country_code)

__qcities=list(zip(name, cod))
__qcities=list(set(__qcities)) #unique cities and country codes
len(__qcities)


# In[6]:



x=0
print('\n Beginning Data Retrieval\n'+'-'*26)
for qcity, qcd in __qcities:

    # Perform API Call
    query_url = base_url + '?apikey=' + APIKEY +         '&q=' + qcity + ',' + qcd + '&units=' + query_units
    weather_info.append(req.get(query_url).json())

    try:
        __cities.append(weather_info[x]['name'])
        rcity=qcity
    except KeyError:
        print('City of %s in %s not found' % (qcity.title(), qcd.upper()))
        #citipy error handler
        #pass
    else:
        print('Processing Record %s | %s '  % (x, rcity.title() ))
        print(query_url)
        __max_temp.append(weather_info[x]['main']['temp_max'])
        __humidity.append(weather_info[x]['main']['humidity'])
        __wind_speed.append(weather_info[x]['wind']['speed'])
        __lon.append(weather_info[x]['coord']['lon'])
        __lat.append(weather_info[x]['coord']['lat'])
        __cloudiness.append(weather_info[x]['clouds']['all'])
        __country.append(weather_info[x]['sys']['country'])
        __date.append(weather_info[x]['dt'])
    
    x+=1

print('\n'+ '-'*28+'\n Data Retrieval complete\n'+'-'*28)
weather_info = {"Temperature": __max_temp, 
                "Humidity": __humidity,
                "Wind Speed": __wind_speed,
                'Lat': __lat,
                'Lng': __lon,
                'Cloudiness': __cloudiness,
                'City': __cities,
                'Country': __country,
                'Date': __date}

weather_info = pd.DataFrame(weather_info)


# In[7]:


weather_info.to_csv('weather_info.csv')
weather_info.count()


# In[8]:


weather_info.head()


# In[9]:


plot_data('Humidity Plot ', '(%)', df['Humidity'])


# In[10]:


plot_data('Cloudiness ', '(%)', df['Cloudiness'])


# In[11]:


plot_data('Wind Speed ', '(mph)', df['Wind Speed'])

