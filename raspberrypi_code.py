import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import datetime
import MySQLdb

hostname = '192.168.1.63'
username = 'Alex'
password = 'alexmak889'
database = 'temp'

dht_sensor_port = 4
dht_sensor_type = Adafruit_DHT.DHT11
led = 18

device = 'raspberry_pi'

GPIO.setmode(GPIO.BCM)              
GPIO.setup(led, GPIO.OUT)
GPIO.setup(dht_sensor_port, GPIO.IN)


def insert_record(device, temp_date, temp_time, temp, hum):
    query = "INSERT INTO sensor_data (device, temp_date, temp_time, temp, hum) VALUES (%s, %s, %s, %s, %s)"       
    args = (device, temp_date, temp_time, temp, hum)

    try:
        conn = MySQLdb.connect(host=hostname, user=username, passwd=password, db=database)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()

    except Exception as error:
        print(error)

    finally:
        cursor.close()
        conn.close()


print('[{0:s}] starting on {1:s}...'.format('prog_name', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')))


try:
    while True:
        hum, temp = Adafruit_DHT.read_retry(dht_sensor_type, dht_sensor_port)
        now = datetime.datetime.now()
        temp_date = now.strftime('%Y-%m-%d')
        temp_time = now.strftime('%H:%M:%S')
        insert_record(device, temp_date, temp_time, format(temp, '.2f'), format(hum, '.2f'))
        time.sleep(1800)

except (IOError, TypeError) as e:
    print("Exiting...")

except KeyboardInterrupt:
    print("Stopping...")

finally:
    print("Cleaning up...")
    GPIO.cleanup() 