from flask import Flask, request, jsonify, redirect
import requests
from flask_cors import CORS
import sqlite3
import os

from tools import get_vue_port

OPEN_ELEVATION_API_URL = "https://api.open-elevation.com/api/v1/lookup"

class Server:
    def __init__(self, db_name="sensor_data.db"):
        self.app = Flask(__name__)
        CORS(self.app)
        self.db_name = db_name
        self._initialize_routes()

    def _initialize_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                Timer INTEGER PRIMARY KEY,
                Accel1X INTEGER, Accel1Y INTEGER, Accel1Z INTEGER,
                Gyro1X INTEGER, Gyro1Y INTEGER, Gyro1Z INTEGER,
                Accel2X INTEGER, Accel2Y INTEGER, Accel2Z INTEGER,
                Gyro2X INTEGER, Gyro2Y INTEGER, Gyro2Z INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gpx_data (
                Timer INTEGER PRIMARY KEY,
                Latitude REAL, Longitude REAL, Altitude REAL,
                Vitesse REAL, Orientation REAL, Satellites INTEGER, HDOP REAL
            )
        ''')

        conn.commit()
        conn.close()

    def _initialize_routes(self):
        app = self.app

        @app.route('/api/sensor-data', methods=['GET'])
        def get_sensor_data():
            query = '''
                SELECT Timer, Accel1X, Accel1Y, Accel1Z, Accel2X, Accel2Y, Accel2Z 
                FROM sensor_data
            '''
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            data = [{"Timer": row[0], "Accel1X": row[1], "Accel1Y": row[2], "Accel1Z": row[3],
                     "Accel2X": row[4], "Accel2Y": row[5], "Accel2Z": row[6]} for row in rows]
            return jsonify(data)

        @app.route('/api/gpx-data', methods=['GET'])
        def get_gpx_data():
            query = '''
                SELECT Timer, Latitude, Longitude, Altitude 
                FROM gpx_data
            '''
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            data = [{"Timer": row[0], "Latitude": row[1], "Longitude": row[2], "Altitude": row[3]} for row in rows]
            return jsonify(data)

        @app.route('/api/gps-trace', methods=['GET'])
        def get_gps_trace():
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT Timer, Latitude, Longitude 
                FROM gpx_data 
                WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL
            ''')
            rows = cursor.fetchall()
            conn.close()

            # Inclure le champ Timer dans chaque point GPS
            trace_data = [{"Timer": row[0], "Latitude": row[1], "Longitude": row[2]} for row in rows if row[1] and row[2]]
            return jsonify(trace_data)


        # Catch all route to redirect to Vue.js frontend
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def catch_all(path):
            if path.startswith("api"):
                return jsonify({"error": "Not Found"}), 404
            vue_port = int(get_vue_port())
            return redirect(f"http://localhost:{vue_port}/{path}", code=307)

        @app.route('/api/calculate-altitude', methods=['POST'])
        def calculate_altitude():
            try:
                data = request.get_json()  # Récupère les données envoyées dans la requête
                gps_points = data.get("gps_points", [])

                # Vérifier si les données sont valides
                if not gps_points or not isinstance(gps_points, list):
                    return jsonify({"error": "Invalid GPS data format"}), 400

                # Assurez-vous que chaque point GPS contient les clés nécessaires
                for point in gps_points:
                    print("point", point)
                    if "Latitude" not in point or "Longitude" not in point or "Timer" not in point:
                        return jsonify({"error": "Missing required keys in GPS points"}), 400

                # Exemple : Utiliser une API ou une fonction fictive pour calculer l'altitude
                # Ici, nous supposons que chaque point retourne une altitude fictive
                altitudes = [
                    {"Timer": point["Timer"], "Altitude": point["Latitude"] + point["Longitude"] * 0.1}
                    for point in gps_points
                ]

                return jsonify(altitudes), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500



    def run(self, port=None):
        if port is None:
            port = int(os.environ.get("FLASK_RUN_PORT", 5000))
        self._initialize_database()
        print(f"Starting Flask server on port {port}...")
        self.app.run(debug=True, port=port, use_reloader=False)


if __name__ == "__main__":
    server = Server()
    server.run()
