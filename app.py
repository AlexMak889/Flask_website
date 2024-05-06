from flask import Flask, render_template, request, Response, url_for, redirect, flash
from flask_wtf import FlaskForm
import db
from datetime import timedelta
import io
import random
import os
import numpy as np
import mariadb
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, equal_to, length
from wtforms.widgets import TextArea    
import datetime as dt
import requests
from math import ceil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alexmak889'

def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    return celsius

#used for search page
class SearchForm(FlaskForm):
    searched = StringField("searched", validators=[DataRequired()])
    submit = SubmitField("submit")
    
#main page
@app.route('/')
def index():
    #day
    d_icon_mapping = {
        'clear sky': 'http://openweathermap.org/img/wn/01d@2x.png',
        'few clouds': 'http://openweathermap.org/img/wn/02d@2x.png',
        'scattered clouds': 'http://openweathermap.org/img/wn/03d@2x.png',
        'broken clouds': 'http://openweathermap.org/img/wn/04d@2x.png',
        'shower rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'rain': 'http://openweathermap.org/img/wn/10d@2x.png',
        'thunderstorm': 'http://openweathermap.org/img/wn/11d@2x.png',
        'snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'mist': 'http://openweathermap.org/img/wn/50d@2x.png',
        'overcast clouds': 'http://openweathermap.org/img/wn/04d@2x.png',
        'thunderstorm with light rain': 'http://openweathermap.org/img/wn/11d@2x.png',
        'thunderstorm with rain': 'http://openweathermap.org/img/wn/11d@2x.png',
        'thunderstorm with heavy rain': 'http://openweathermap.org/img/wn/11d@2x.png',
        'light thunderstorm': 'http://openweathermap.org/img/wn/11d@2x.png',
        'thunderstorm': 'http://openweathermap.org/img/wn/11d@2x.png',
        'heavy thunderstorm': 'http://openweathermap.org/img/wn/11d@2x.png',
        'ragged thunderstorm': 'http://openweathermap.org/img/wn/11d@2x.png',
        'thunderstorm with light drizzle': 'http://openweathermap.org/img/wn/11d@2x.png',
        'thunderstorm with drizzle': 'http://openweathermap.org/img/wn/11d@2x.png',
        'thunderstorm with heavy drizzle': 'http://openweathermap.org/img/wn/11d@2x.png',
        'light intensity drizzle': 'http://openweathermap.org/img/wn/09d@2x.png',
        'drizzle': 'http://openweathermap.org/img/wn/09d@2x.png',
        'heavy intensity drizzle': 'http://openweathermap.org/img/wn/09d@2x.png',
        'light intensity drizzle rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'drizzle rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'heavy intensity drizzle rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'shower rain and drizzle': 'http://openweathermap.org/img/wn/09d@2x.png',
        'heavy shower rain and drizzle': 'http://openweathermap.org/img/wn/09d@2x.png',
        'shower drizzle': 'http://openweathermap.org/img/wn/09d@2x.png',
        'light rain': 'http://openweathermap.org/img/wn/10d@2x.png',
        'moderate rain': 'http://openweathermap.org/img/wn/10d@2x.png',
        'heavy intensity rain': 'http://openweathermap.org/img/wn/10d@2x.png',
        'very heavy rain': 'http://openweathermap.org/img/wn/10d@2x.png',
        'extreme rain': 'http://openweathermap.org/img/wn/10d@2x.png',
        'freezing rain': 'http://openweathermap.org/img/wn/13d@2x.png',
        'light intensity shower rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'shower rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'heavy intensity shower rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'ragged shower rain': 'http://openweathermap.org/img/wn/09d@2x.png',
        'light snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'heavy snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'sleet': 'http://openweathermap.org/img/wn/13d@2x.png',
        'light shower sleet': 'http://openweathermap.org/img/wn/13d@2x.png',
        'shower sleet': 'http://openweathermap.org/img/wn/13d@2x.png',
        'light rain and snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'rain and snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'light shower snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'shower snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'heavy shower snow': 'http://openweathermap.org/img/wn/13d@2x.png',
        'mist': 'http://openweathermap.org/img/wn/50d@2x.png',
        'smoke': 'http://openweathermap.org/img/wn/50d@2x.png',
        'haze': 'http://openweathermap.org/img/wn/50d@2x.png',
        'sand/dust whirls': 'http://openweathermap.org/img/wn/50d@2x.png',
        'fog': 'http://openweathermap.org/img/wn/50d@2x.png',
        'sand': 'http://openweathermap.org/img/wn/50d@2x.png',
        'dust': 'http://openweathermap.org/img/wn/50d@2x.png',
        'volcanic ash': 'http://openweathermap.org/img/wn/50d@2x.png',
        'squalls': 'http://openweathermap.org/img/wn/50d@2x.png',
        'tornado': 'http://openweathermap.org/img/wn/50d@2x.png',
        'clear sky': 'http://openweathermap.org/img/wn/01d@2x.png',
        'few clouds': 'http://openweathermap.org/img/wn/02d@2x.png',
        'scattered clouds': 'http://openweathermap.org/img/wn/03d@2x.png',
        'broken clouds': 'http://openweathermap.org/img/wn/04d@2x.png',
        'overcast clouds': 'http://openweathermap.org/img/wn/04d@2x.png'

    }
    #nigt
    n_icon_mapping = {
        'clear sky': 'http://openweathermap.org/img/wn/01n@2x.png',
        'few clouds': 'http://openweathermap.org/img/wn/02n@2x.png',
        'scattered clouds': 'http://openweathermap.org/img/wn/03n@2x.png',
        'broken clouds': 'http://openweathermap.org/img/wn/04n@2x.png',
        'shower rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'rain': 'http://openweathermap.org/img/wn/10n@2x.png',
        'thunderstorm': 'http://openweathermap.org/img/wn/11n@2x.png',
        'snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'mist': 'http://openweathermap.org/img/wn/50n@2x.png',
        'thunderstorm with light rain': 'http://openweathermap.org/img/wn/11n@2x.png',
        'thunderstorm with rain': 'http://openweathermap.org/img/wn/11n@2x.png',
        'thunderstorm with heavy rain': 'http://openweathermap.org/img/wn/11n@2x.png',
        'light thunderstorm': 'http://openweathermap.org/img/wn/11n@2x.png',
        'thunderstorm': 'http://openweathermap.org/img/wn/11n@2x.png',
        'heavy thunderstorm': 'http://openweathermap.org/img/wn/11n@2x.png',
        'ragged thunderstorm': 'http://openweathermap.org/img/wn/11n@2x.png',
        'thunderstorm with light drizzle': 'http://openweathermap.org/img/wn/11n@2x.png',
        'thunderstorm with drizzle': 'http://openweathermap.org/img/wn/11n@2x.png',
        'thunderstorm with heavy drizzle': 'http://openweathermap.org/img/wn/11n@2x.png',
        'light intensity drizzle': 'http://openweathermap.org/img/wn/09n@2x.png',
        'drizzle': 'http://openweathermap.org/img/wn/09n@2x.png',
        'heavy intensity drizzle': 'http://openweathermap.org/img/wn/09n@2x.png',
        'light intensity drizzle rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'drizzle rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'heavy intensity drizzle rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'shower rain and drizzle': 'http://openweathermap.org/img/wn/09n@2x.png',
        'heavy shower rain and drizzle': 'http://openweathermap.org/img/wn/09n@2x.png',
        'shower drizzle': 'http://openweathermap.org/img/wn/09n@2x.png',
        'light rain': 'http://openweathermap.org/img/wn/10n@2x.png',
        'moderate rain': 'http://openweathermap.org/img/wn/10n@2x.png',
        'heavy intensity rain': 'http://openweathermap.org/img/wn/10n@2x.png',
        'very heavy rain': 'http://openweathermap.org/img/wn/10n@2x.png',
        'extreme rain': 'http://openweathermap.org/img/wn/10n@2x.png',
        'freezing rain': 'http://openweathermap.org/img/wn/13n@2x.png',
        'light intensity shower rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'shower rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'heavy intensity shower rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'ragged shower rain': 'http://openweathermap.org/img/wn/09n@2x.png',
        'light snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'heavy snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'sleet': 'http://openweathermap.org/img/wn/13n@2x.png',
        'light shower sleet': 'http://openweathermap.org/img/wn/13n@2x.png',
        'shower sleet': 'http://openweathermap.org/img/wn/13n@2x.png',
        'light rain and snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'rain and snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'light shower snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'shower snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'heavy shower snow': 'http://openweathermap.org/img/wn/13n@2x.png',
        'mist': 'http://openweathermap.org/img/wn/50n@2x.png',
        'smoke': 'http://openweathermap.org/img/wn/50n@2x.png',
        'haze': 'http://openweathermap.org/img/wn/50n@2x.png',
        'sand/dust whirls': 'http://openweathermap.org/img/wn/50n@2x.png',
        'fog': 'http://openweathermap.org/img/wn/50n@2x.png',
        'sand': 'http://openweathermap.org/img/wn/50n@2x.png',
        'dust': 'http://openweathermap.org/img/wn/50n@2x.png',
        'volcanic ash': 'http://openweathermap.org/img/wn/50n@2x.png',
        'squalls': 'http://openweathermap.org/img/wn/50n@2x.png',
        'tornado': 'http://openweathermap.org/img/wn/50n@2x.png',
        'clear sky': 'http://openweathermap.org/img/wn/01n@2x.png',
        'few clouds': 'http://openweathermap.org/img/wn/02n@2x.png',
        'scattered clouds': 'http://openweathermap.org/img/wn/03n@2x.png',
        'broken clouds': 'http://openweathermap.org/img/wn/04n@2x.png',
        'overcast clouds': 'http://openweathermap.org/img/wn/04n@2x.png'
    }
    default_icon = 'default.png'

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = open('api_key', 'r').read().strip()
    CITY = "Ängelholm"

    url = BASE_URL + "appid=" + API_KEY + "&q=" + CITY

    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celsius = ceil(kelvin_to_celsius_fahrenheit(temp_kelvin))
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius = ceil(kelvin_to_celsius_fahrenheit(feels_like_kelvin))
    wind_speed = response['wind']['speed']
    description = response['weather'][0]['description']
    sunrise_time = dt.datetime.utcfromtimestamp(response['sys']['sunrise'] + response['timezone'])
    sunset_time = dt.datetime.utcfromtimestamp(response['sys']['sunset'] + response['timezone'])
    
    current_time = dt.datetime.now().time()
    is_daytime = sunrise_time.time() <= current_time <= sunset_time.time()
    icon_mapping = d_icon_mapping if is_daytime else n_icon_mapping

    icon_filename = icon_mapping.get(description, default_icon)



    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT temp FROM sensor_data ORDER BY temp_date DESC, temp_time DESC LIMIT 1")
    latest_temp_row = cur.fetchone()
    latest_temp = latest_temp_row[0] if latest_temp_row else None
    
    return render_template('index.html', icon_filename=icon_filename, feels_like_celsius=feels_like_celsius, latest_temp=latest_temp, sunrise_time=sunrise_time, sunset_time=sunset_time,description=description, wind_speed=wind_speed, temp_celsius=temp_celsius)

#displays all the data
@app.route('/all_data', methods=['get'])
def data():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data")
    data = cur.fetchall()
    processed_data = []
    for row in data:
        formatted_row = list(row)
        formatted_row[2] = str(timedelta(seconds=row[2].seconds))
        processed_data.append(tuple(formatted_row))

    return render_template('all_data.html', data=processed_data)

#search page 
@app.context_processor
def base():
    if request.method == 'GET':
        form = SearchForm()
    else:
        form = None
    return dict(form=form)
@app.route('/search', methods=["POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        post_searched = form.searched.data
        
        return render_template("search.html", form=form, searched=post_searched)
    

#temprature every day att 12.00
@app.route('/days', methods=["GET"])
def day_data():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT temp_date, temp FROM sensor_data WHERE temp_date BETWEEN '2024-01-01' AND '2024-12-31' AND temp_time BETWEEN '12:00:00' AND '12:25:00'")
    data = cur.fetchall()
    cur.close()
    data_x = [item[0] for item in data]
    data_y = [item[1] for item in data]
    return render_template("days.html", data_x=data_x, data_y=data_y)

@app.route('/yesterday', methods=["GET"])
def yesterday_data():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT DATE_FORMAT(temp_time, '%Y-%m-%d %H:00:00') AS hour_time, temp FROM sensor_data WHERE temp_time BETWEEN '2024-01-01 00:00:00' AND '2024-12-31 23:59:59' GROUP BY hour_time")
    data = cur.fetchall()
    cur.close()
    # conn.close()  # Consider uncommenting this line to close the connection
    data2_x = [item[0] for item in data]
    data2_y = [item[1] for item in data]
    return render_template("yesterday.html", data2_x=data2_x, data2_y=data2_y)


if __name__ == '__main__':
    app.run(debug=True)


