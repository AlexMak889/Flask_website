from flask import Flask, render_template
import mariadb

app = Flask(__name__)

@app.route('/')
def index():
    conn = mariadb.connect(
        user="username",
        password="pasword",
        host="raspberry pi ip adress",
        database="database name"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
