from flask import Flask, Response, send_file, jsonify
import Adafruit_DHT
import base64
from picamera import PiCamera
from flask_cors import CORS
from time import sleep
import json

app = Flask(__name__)
CORS(app)

# Adafruit_DHT.DHT22 sensor
sensor = Adafruit_DHT.DHT22
# connected to GPIO4.
pin = 4

# camera
try:
    camera = PiCamera()
except:
    camera = False

@app.route('/api/gettmp',methods=["GET"])
def get_temp_humi():
    humidity,temperature = Adafruit_DHT.read_retry(sensor, pin)
    while humidity is None or temperature is None:
        sleep(2) #DHT22 can only be read for every 2 seconds
        humidity,temperature = Adafruit_DHT.read_retry(sensor, pin)
    humidity = round(humidity,2)
    temperature = round(temperature,2)
    data = [temperature,humidity]
    resp = Response(json.dumps(data),  mimetype='application/json')
    return resp

@app.route('/api/capture, methods=["GET"])
def get_capture():
    if camera != False:
        camera.capture('./image.jpg')
        sleep(5)
        filename = "./image.jpg"
        with open(filename, 'rb') as f:
            im_b64 = base64.b64encode(f.read())
        return jsonify({'image' : im_b64})
    else:
        return jsonify({'image' : 'No camera available'})

if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)
