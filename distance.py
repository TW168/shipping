import pandas as pd
from haversine import haversine

# define the threshold distance in miles
threshold_distance = 120

# create a pandas dataframe with order number, lat and lon columns
df = pd.DataFrame({'order_number': [1, 2, 3, 4, 5, 6, 7,8],
                   'lat': [37.7749, 34.0522, 40.7128, 39.9042, 41.8781, 32.7157, 42.3601, 38.0687],
                   'lon': [-122.4194, -118.2437, -74.0060, -75.1652, -87.6298, -117.1611, -71.0589, -121.4991]})

# create a list to hold the groups
groups = []

# loop through each location
for i in range(len(df)):
    # create a new group for the current location
    group = [df.iloc[i]]
    # loop through the remaining locations
    for j in range(i+1, len(df)):
        # calculate the distance between the current location and the next location
        distance = haversine((df['lat'][i], df['lon'][i]), (df['lat'][j], df['lon'][j]))
        # if the distance is less than the threshold, add the next location to the group
        if distance <= threshold_distance:
            group.append(df.iloc[j])
    # add the group to the list of groups
    groups.append(group)

# print the groups
for i, group in enumerate(groups):
    print(f"Group {i+1}:")
    for j, location in enumerate(group):
        print(f"\t{j+1}. Order Number: {location['order_number']}, Lat: {location['lat']}, Lon: {location['lon']}")
