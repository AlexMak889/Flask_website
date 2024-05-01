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


app = Flask(__name__)
app.config['SECRET_KEY'] = 'alexmak889'

#used for search page
class SearchForm(FlaskForm):
    searched = StringField("searched", validators=[DataRequired()])
    submit = SubmitField("submit")
    
#main page
@app.route('/')
def index():
    return render_template('index.html')

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
    cur.execute("SELECT temp_date, temp FROM sensor_data WHERE temp_date BETWEEN '2024-01-01' AND '2024-12-31' AND temp_time BETWEEN '12:00:00' AND '12:10:00'")
    data = cur.fetchall()
    cur.close()
    # conn.close()  # Consider uncommenting this line to close the connection
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



""" @app.route('/day', methods=['GET'])
def index2():
    try:
        conn = db.conn
        cur = conn.cursor()

        cur.execute("SELECT temp FROM sensor_data WHERE temp_date BETWEEN '2024-01-01' AND '2024-12-31' AND temp_time BETWEEN '12:00:00' AND '12:10:00'")
        data_x = [item[0] for item in cur.fetchall()]

        cur.execute("SELECT temp_date FROM sensor_data WHERE temp_date BETWEEN '2024-01-01' AND '2024-12-31' AND temp_time BETWEEN '12:00:00' AND '12:10:00'")
        data_y = [item[0] for item in cur.fetchall()]
        

        return render_template('day.html', data_x=data_x, data_y=data_y)
    except mariadb.Error as e:
        # Handle database errors
        print(f"Error: {e}")
        return "Database error occurred"
if __name__ == '__main__':
    import webbrowser
 """