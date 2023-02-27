import pandas as pd
from geopy.geocoders import Nominatim

# create a pandas dataframe with city and state columns
df = pd.DataFrame({'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'BETHEL'],
                   'state': ['NY', 'CA', 'IL', 'TX', 'PA']})

# create a geolocator object using Nominatim
geolocator = Nominatim(user_agent='my_app')

# create empty lists to hold the latitude and longitude values
latitudes = []
longitudes = []

# loop through each city and state and get the latitude and longitude using Geopy
for i in range(len(df)):
    location = geolocator.geocode(f"{df['city'][i]}, {df['state'][i]}")
    if location is not None:
        latitudes.append(location.latitude)
        longitudes.append(location.longitude)
    else:
        latitudes.append(None)
        longitudes.append(None)

# add the latitude and longitude values to the dataframe
df['latitude'] = latitudes
df['longitude'] = longitudes

# print the dataframe
print(df)
