import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, jsonify
import requests
from shared import config


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/telemetry')
def telemetry():
    try:
        r = requests.get(f"http://{config.SATELLITE_HOST}:{config.SATELLITE_PORT}/telemetry")
        return r.json()
    except:
        return {"telemetry": ["🚫 Could not fetch satellite telemetry."]}

if __name__ == '__main__':
    app.run(port=5050)
