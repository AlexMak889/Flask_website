import matplotlib.pyplot as plt
import db

def index():
    conn = db.conn
    cur = conn.cursor()
    cur.execute("SELECT temp FROM sensor_data")
    data = cur.fetchall()
    cur.close()
    conn.close()

    return [item[0] for item in data]  # Extracting values from tuples

data = index()

# Generating x values (assuming sequential)
x = list(range(1, len(data) + 1))

# Plotting the data
plt.plot(x, data, color='green')
plt.xlabel('Index')
plt.ylabel('Temperature')
plt.title(label="Sensor Data", fontsize=16, color="green")
plt.show()
