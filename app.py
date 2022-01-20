from asyncio import Event, events
from distutils.log import set_verbosity
from werkzeug.utils import secure_filename
import weather_data
import scrape_states
import pandas as pd
from flask import Flask, render_template, request, redirect, jsonify, make_response
app = Flask(__name__)

state_codes = scrape_states.scrape()
print("This is the state code list:", state_codes)

@app.route("/data/<state>")
def data(state):
    feature_response = weather_data.json(state)
    return feature_response

@app.route("/", methods = ['POST', 'GET'])
def index():
    #home page for info and navigation
    return render_template("index.html", states = state_codes)

@app.route("/charts")
def charts():
    #display drop down menu with states list
    #accept the state selection and display charts
    return  render_template("charts.html", states= state_codes)

@app.route("/map")
def map():
    #display drop down menu with states list
    #accept the state selection and display map
    return render_template("map.html", states= state_codes)    

if __name__ == '__main__':
    app.run()
