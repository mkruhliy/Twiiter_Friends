"""
Parsing JSON and building MAP
"""

import json
import ssl
import requests
import folium
import json
from geopy.geocoders import Nominatim
import os
import twurl

def search(acct):

    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': 10})
    response = requests.get(url)
    data = response.json()

    with open(os.path.join(os.getcwd(), "friends.json"), "w", encoding="utf-8") as file:
        return json.dump(data, file, ensure_ascii=False, indent=4)


def data_read(name):
    """
    Reading json into nicknames and locations
    """
    search(name)
    with open(os.path.join(os.getcwd(), 'friends.json'), "r", encoding="utf-8") as file:
        data = json.load(file)
    data = data['users']
    names = []
    locations = []
    for dictionary in data:
        name = dictionary['screen_name']
        names.append(name)
        location = dictionary['location']
        locations.append(location)
    return names, locations

def change_map(name):
    """
    Creating Map
    """
    geolocator = Nominatim(user_agent="UCU")
    names, locations = data_read(name)
    lat = []
    lon = []
    for i in locations:
        try:
            lat_str = str(geolocator.geocode(i).latitude)
            lon_str = str(geolocator.geocode(i).longitude)
            lat.append(lat_str)
            lon.append(lon_str)
        except AttributeError:
            lat.append('NODATA')
            lon.append('NODATA')

    Map = folium.Map([45,45], zoom_start=2)

    for lt, ln, nm in zip(lat, lon, names):
        if lt != "NODATA" and ln != "NODATA":
            try:
                try:
                    Map.add_child(folium.Marker(location=[lt, ln],
                                            popup=nm,
                                            icon=folium.Icon(color='red')))
                except ValueError:
                    continue
            except IndexError:
                continue
    Map.save(os.path.join(os.getcwd(), 'templates', 'Map.html'))
