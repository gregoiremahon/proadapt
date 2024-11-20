from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # Autoriser CORS pour toutes les routes

DB_NAME = "sensor_data.db"

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table for sensor data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            Timer INTEGER PRIMARY KEY,
            Accel1X INTEGER, Accel1Y INTEGER, Accel1Z INTEGER,
            Gyro1X INTEGER, Gyro1Y INTEGER, Gyro1Z INTEGER,
            Accel2X INTEGER, Accel2Y INTEGER, Accel2Z INTEGER,
            Gyro2X INTEGER, Gyro2Y INTEGER, Gyro2Z INTEGER
        )
    ''')

    # Create table for GPX data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gpx_data (
            Timer INTEGER PRIMARY KEY,
            Latitude REAL, Longitude REAL, Altitude REAL,
            Vitesse REAL, Orientation REAL, Satellites INTEGER, HDOP REAL
        )
    ''')

    conn.commit()
    conn.close()

# API route for sensor data
@app.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT Timer, Accel1X, Accel1Y, Accel1Z, Accel2X, Accel2Y, Accel2Z FROM sensor_data')
    rows = cursor.fetchall()
    conn.close()

    data = [{"Timer": row[0], "Accel1X": row[1], "Accel1Y": row[2], "Accel1Z": row[3], "Accel2X": row[4], "Accel2Y": row[5], "Accel2Z": row[6],} for row in rows]
    return jsonify(data)

# API route for GPX data
@app.route('/api/gpx-data', methods=['GET'])
def get_gpx_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT Timer, Latitude, Longitude, Altitude FROM gpx_data')
    rows = cursor.fetchall()
    conn.close()

    data = [{"Timer": row[0], "Latitude": row[1], "Longitude": row[2], "Altitude": row[3]} for row in rows]
    return jsonify(data)

# API route for GPS trace
@app.route('/api/gps-trace', methods=['GET'])
def get_gps_trace():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT Latitude, Longitude FROM gpx_data')
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries with Latitude and Longitude
    data = [{"Latitude": row[0], "Longitude": row[1]} for row in rows if row[0] is not None and row[1] is not None]
    return jsonify(data)


# Redirect all other routes to the Vue.js development server
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # Redirige toutes les autres requêtes vers le serveur Vue.js
    return redirect(f"http://localhost:3000/{path}", code=307)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
