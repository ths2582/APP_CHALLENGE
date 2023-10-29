import os

import json

import requests

from flask import Flask, flash, redirect, render_template, request, session

BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Home Page"""
    return render_template("index.html")


def get_coordinates(location):
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"

def find_grocery_stores(parameters):
    BingMapsKey = "AhkZGTzNUxseN5Tb-IxxOzQZ2k2IkXksXBua-LbD0FO_L-vXwg4yshTifpr0BF9H"
    type = "Grocers"
    r = requests.get(
        f"https://dev.virtualearth.net/REST/v1/LocalSearch/?type=Supermarkets&userCircularMapView={parameters}&key={BingMapsKey}")

    stores = r.json()
    lst = []
    if len(stores['resourceSets']) != 0:
        for store in stores['resourceSets'][0]['resources']:
            coordinates = (str(store['point']['coordinates'])[1:-1])
            address = str(store['Address']['formattedAddress'])
            store_name = str(store['name'])
            info = (store_name, address, coordinates)
            lst.append(info)
    else:
        return
    # returns information in a tuple
    return lst


def find_directions(user_location, destination):
    # user_location and destination can be address or coordinates
    r = requests.get(f"http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1={user_location}&wayPoint.2={destination}&key={BingMapsKey}&distanceUnit=mi&durationUnit=Minute&trafficDataUsed=FlowAndClosure")
    route = r.json()
    directions = []
    for direction in route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']:
        directions.append(direction['instruction']['text'])
    return directions


def find_distance(user_location, destination):
    # user_location and destination can be address or coordinates
    r = requests.get(f"http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1={user_location}&wayPoint.2={destination}&key={BingMapsKey}&distanceUnit=mi")
    route = r.json()
    travelDistance=0
    travelDuration=0
    if len(route['resourceSets']) != 0:
        for leg in route['resourceSets'][0]['resources'][0]['routeLegs'][0]['itineraryItems']:
            travelDistance += (leg['travelDistance'])
            travelDuration += (leg['travelDuration'])
        return round(travelDistance, 2), travelDuration
    else:
        return -1, -1


def get_map(user_location, destination):
    # user_location and destination can be address or coordinates
    r = requests.get(f"https://dev.virtualearth.net/REST/v1/Imagery/Map/imagerySet/centerPoint/zoomLevel/Routes/travelMode?waypoint.1={user_location}&waypoint.2={destination}&format={format}&key={BingMapsKey}")
    print(r)

@app.route("/location_query", methods=["GET", "POST"])
def location_query():
    """Show list of nearby grocery stores!"""
    if(request.method == "GET"):
        return render_template("location_query.html")
    elif (request.method == "POST"):
        location = request.form.get("location")
        stores = find_grocery_stores("39.6734332362205, -75.64806944984902, 5000")
        return render_template("stores.html", stores = stores)

