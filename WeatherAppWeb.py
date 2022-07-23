import requests
import json
import math
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, render_template


def configure():
  load_dotenv()
  
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    configure()

    if request.method == 'POST':
        
        location = request.form['city']

        
        URL = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv('api_key')}&units=metric"

        weatherData = requests.get(url = URL)                                       
        weather = weatherData.json() 

        if int(weather['cod']) >= 400:
            return render_template('invalid.html')

        if int(weather['cod']) == 200:
            place = location                                             
            temp = round(weather['main']['temp'])                                   
            humid = round(weather['main']['humidity'])                              
            sRise = weather['sys']['sunrise']
            sSet = weather['sys']['sunset']
            
        def formatTime(timestamp, tz_offset):
            tz_offs_system = round((datetime.now() - datetime.utcnow()).total_seconds())
            tz_offs_local  = tz_offset

            adjusted = timestamp + tz_offs_local - tz_offs_system
        
            return datetime.fromtimestamp(adjusted).strftime("at %H:%M")
        
        formattedRise = formatTime(sRise, weather['timezone'])
        formattedSet = formatTime(sSet, weather['timezone']) 

        return render_template('weather.html', place=place, temp=temp, humid=humid, sRiseF=formattedRise, sSetF=formattedSet) 

    else:
        return render_template('index.html')

@app.route('/<location>/f')
def cityF(location):
    configure()

    URL = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={os.getenv('api_key')}&units=imperial"

    weatherData = requests.get(url = URL)                                       
    weather = weatherData.json() 

    if int(weather['cod']) == 200:
        place = location                                             
        temp = round(weather['main']['temp'])                                   
        humid = round(weather['main']['humidity'])                              
        sRise = weather['sys']['sunrise']
        sSet = weather['sys']['sunset']
        
    def formatTime(timestamp, tz_offset):
        tz_offs_system = round((datetime.now() - datetime.utcnow()).total_seconds())
        tz_offs_local  = tz_offset

        adjusted = timestamp + tz_offs_local - tz_offs_system
    
        return datetime.fromtimestamp(adjusted).strftime("at %H:%M")
    
    formattedRise = formatTime(sRise, weather['timezone'])
    formattedSet = formatTime(sSet, weather['timezone']) 

    return render_template('weather.html', place=place, temp=temp, humid=humid, sRiseF=formattedRise, sSetF=formattedSet)
    

if __name__ == '__main__':
    app.run()