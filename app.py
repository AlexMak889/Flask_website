from flask import Flask, render_template
import mariadb
import db
app = Flask(__name__)

@app.route('/')
def index():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM sensor_data")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
