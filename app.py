from flask import Flask, render_template, request, Response
import db
from datetime import timedelta
import io
import random
import os
import numpy as np
import mariadb
""" from matplotlib.figure import Figure
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt """

""" def graph(num_x_points=50):
    #Renders the plot on the fly.
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return plt
 """
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all_data', methods=['get'])
def data():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data")
    data = cur.fetchall()
    #cur.close()
    #conn.close()
    processed_data = []
    for row in data:
        formatted_row = list(row)
        formatted_row[2] = str(timedelta(seconds=row[2].seconds))
        processed_data.append(tuple(formatted_row))

    return render_template('all_data.html', data=processed_data)

@app.route('/day', methods=['GET'])
def index2():
    try:
        conn = db.conn
        cur = conn.cursor()

        cur.execute("SELECT temp FROM sensor_data WHERE temp_date BETWEEN '2024-01-01' AND '2024-12-31' AND temp_time BETWEEN '12:00:00' AND '12:10:00'")
        data_x = [item[0] for item in cur.fetchall()]

        cur.execute("SELECT temp_date FROM sensor_data WHERE temp_date BETWEEN '2024-01-01' AND '2024-12-31' AND temp_time BETWEEN '12:00:00' AND '12:10:00'")
        data_y = [item[0] for item in cur.fetchall()]

        cur.close()  # Close the cursor
        # Don't close the connection if you're using it elsewhere in your application

        return render_template('day.html', data_x=data_x, data_y=data_y)
    except mariadb.Error as e:
        # Handle database errors
        print(f"Error: {e}")
        return "Database error occurred"
if __name__ == '__main__':
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)

    
"""     plt.plot(data_x, data_y)  
     plt.xlabel('Index')
     plt.ylabel('Temperature')
     plt.title(label="Sensor Data", fontsize=16, color="green")
      plt.legend()
      plt.show() """
    