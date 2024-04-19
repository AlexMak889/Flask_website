from flask import Flask, render_template, request
import mariadb
import db
import matplotlib_code
from datetime import timedelta
import matplotlib.pyplot as plt




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
@app.route('/temp this week', methods=['GET'])
def index2():
    if request.method =='GET':
        data_x = index2()
        print("data_y length")
        print(len(data_x))
        data_y = index()
        print(len(data_y))
        x = list(range(1, len(data_x) + 1))
        y = list(range(1, len(data_y) + 1))


        plt.plot(data_x, data_y)  

        plt.xlabel('Index')
        plt.ylabel('Temperature')
        plt.title(label="Sensor Data", fontsize=16, color="green")
        plt.legend()
        plt.show()
    else:return render_template('temp_code_week.html')

if __name__ == '__main__':
    app.run(debug=True)
