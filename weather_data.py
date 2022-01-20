import requests
import scrape_states
import json
import collections
from geojson import Point, Feature, FeatureCollection, dump
from bson import json_util
from bson.json_util import dumps
from pymongo import MongoClient

def api(state):
    city = []
    severity = []
    event = []
    urgency = []
    headline = []
    coordinates = []
    #states = scrape_states.scrape()
    error = 0
    
    
    try:
            query = f"https://api.weather.gov/alerts/active?status=actual&message_type=alert&area={state}&severity=Severe"
            weather_response = requests.get(query).json()
            print(state)
            print(query)
            if len(weather_response["features"]) > 0:
                impacts = len(weather_response["features"])
                for x in range(impacts):
                    city.append(weather_response["features"][x]["properties"]["areaDesc"])
                    severity.append(weather_response["features"][x]["properties"]["severity"])
                    event.append(weather_response["features"][x]["properties"]["event"])
                    urgency.append(weather_response["features"][x]["properties"]["urgency"])
                    headline.append(weather_response["features"][x]["properties"]["headline"])
                    coordinates.append(weather_response["features"][x]["geometry"]["coordinates"])
    except KeyError:
            error = error + 1
    except TypeError:
            error = error + 1
    return weather_response

def json(state):
    headline = []
    coordinates = []
    properties = {"headline":headline}
    geometry = {"type":"Polygon", "coordinates":coordinates}
    features = []
    #state = scrape_states.scrape()
    error = 0
    
    try:
            query = f"https://api.weather.gov/alerts/active?status=actual&message_type=alert&area={state}&severity=Severe"
            weather_response = requests.get(query).json()

            #validating inputs
            #print(state)
            #print(query)

            if len(weather_response["features"]) > 0:
                impacts = len(weather_response["features"])
                for x in range(impacts):
                    headline.append(weather_response["features"][x]["properties"]["headline"])
                    coordinates.append(weather_response["features"][x]["geometry"]["coordinates"])
    except KeyError:
            error = error + 1
    except TypeError:
            error = error + 1
    features.append(Feature(geometry=geometry, properties=properties))
    feature_collection = FeatureCollection(features)
    with open("feature_collection_geoJson.geojson", 'w') as g:
         dump(feature_collection, g)
    client = MongoClient("localhost", 27017)
    db = client["weather_db"]
    collection = db["collections"]
    collection.insert_one(feature_collection)
    client.close()
    feature_response = json_util.dumps(feature_collection)
    return feature_response
