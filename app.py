from flask import Flask, render_template, request
import db
from datetime import timedelta
import matplotlib.pyplot as plt
import io
import random
import numpy as np 
from matplotlib.figure import Figure
from flask import Flask, Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

def graph(num_x_points=50):
    """ Renders the plot on the fly."""
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return render_template('temp_code_week.html', image=output.getvalue())

app = Flask(__name__)

@app.route('/', methods=['get'])
def index():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data")
    data = cur.fetchall()
    cur.close()
    conn.close()
    processed_data = []
    for row in data:
        formatted_row = list(row)
        formatted_row[2] = str(timedelta(seconds=row[2].seconds))
        processed_data.append(tuple(formatted_row))

    return render_template('index.html', data=processed_data)

@app.route('/day', methods=['GET'])
def index2():
    plot = graph(num_x_points=50)
    plot.savefig(os.path.join('static', 'images', 'plot.png'))     
    return render_template('day.html') 

if __name__ == '__main__':
    import webbrowser

    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)