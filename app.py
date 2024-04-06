
from flask import Flask, request, jsonify

app = Flask(__name__)

# Store received data
data_store = []
@app.route('/data', methods=['POST'])
def receive_data():
    data = request.json
    data_store.append(data)  # Store data
    print('Received data:', data)
    return jsonify({'message': 'Data received successfully'}), 200

@app.route('/')
def index():
    
    latest_data = data_store[-1] if data_store else {'temperature': 'N/A', 'humidity': 'N/A'}
    return f"Temperature: {latest_data['temperature']}C, Humidity: {latest_data['humidity']}%"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  
