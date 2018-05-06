

```python
import json
import requests as req
from citipy import citipy
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import seaborn as sns
import numpy as np
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-15-5c2b7152725e> in <module>()
          1 import json
          2 import requests as req
    ----> 3 from citipy import citipy
          4 import pandas as pd
          5 import matplotlib.pyplot as plt
    

    ModuleNotFoundError: No module named 'citipy'



```python
base_url = 'http://api.openweathermap.org/data/2.5/weather'
APIKEY = 'ad3eeb24a921df30f22dd6e80a21583f'
```

__cities = []
query_units = 'imperial'
weather_info = []
__max_temp = []
__humidity = []
__wind_speed = []
__lon = []
__lat = []
__cloudiness  = []
__qcities  = []
__country = []
__date = []


```python
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
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-5-656c4f580b6d> in <module>()
          2 name=[]
          3 cod=[]
    ----> 4 lt=180 * np.random.random_sample((num_query)) - 90 #latitude [-90, 90)
          5 lg=360 * np.random.random_sample((num_query)) - 180 #longtitude [-180, 180)
          6 geo_coord=list(zip(lt,lg))
    

    NameError: name 'np' is not defined



```python

x=0
print('\n Beginning Data Retrieval\n'+'-'*26)
for qcity, qcd in __qcities:

    # Perform API Call
    query_url = base_url + '?apikey=' + APIKEY + \
        '&q=' + qcity + ',' + qcd + '&units=' + query_units
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
```

    
     Beginning Data Retrieval
    --------------------------
    
    ----------------------------
     Data Retrieval complete
    ----------------------------
    


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-6-ef36791849d5> in <module>()
         40                 'Date': __date}
         41 
    ---> 42 weather_info = pd.DataFrame(weather_info)
    

    NameError: name 'pd' is not defined



```python
weather_info.to_csv('weather_info.csv')
weather_info.count()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-7-7c59b187d8f2> in <module>()
    ----> 1 weather_info.to_csv('weather_info.csv')
          2 weather_info.count()
    

    AttributeError: 'dict' object has no attribute 'to_csv'



```python
weather_info.head()
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-8-e36ae15bb7b3> in <module>()
    ----> 1 weather_info.head()
    

    AttributeError: 'dict' object has no attribute 'head'



```python
plot_data('Humidity Plot ', '(%)', df['Humidity'])
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-9-a661b253a041> in <module>()
    ----> 1 plot_data('Humidity Plot ', '(%)', df['Humidity'])
    

    NameError: name 'plot_data' is not defined



```python
plot_data('Cloudiness ', '(%)', df['Cloudiness'])
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-10-5ab659b0cc8a> in <module>()
    ----> 1 plot_data('Cloudiness ', '(%)', df['Cloudiness'])
    

    NameError: name 'plot_data' is not defined



```python
plot_data('Wind Speed ', '(mph)', df['Wind Speed'])
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-11-86311f34afa3> in <module>()
    ----> 1 plot_data('Wind Speed ', '(mph)', df['Wind Speed'])
    

    NameError: name 'plot_data' is not defined

