from flask import Flask, request, jsonify, redirect
import requests
from flask_cors import CORS
import sqlite3
import os
import hashlib
from user_database_manager import UserDatabaseManager
from database_manager import DatabaseManager
from tools import get_vue_port
import csv
import shutil
import gpxpy


def load_csv_file_to_database(csv_file_path, db_name="sensor_data.db"):
    db_manager = DatabaseManager(db_name)
    db_manager.initialize_database()
    db_manager.load_csv_to_db(csv_file_path=csv_file_path)

OPEN_ELEVATION_API_URL = "https://api.open-elevation.com/api/v1/lookup"

class Server:
    def __init__(self, db_name="sensor_data.db", user_db_name="user_data.db"):
        self.app = Flask(__name__)
        CORS(self.app)
        self.db_name = db_name
        self.user_db_manager = UserDatabaseManager(user_db_name)
        self.user_db_manager._initialize_database()
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
            return redirect(f"http://127.0.0.1:{vue_port}/{path}", code=307)

        # Route to calculate altitude using Open Elevation API
        @app.route('/api/calculate-altitude', methods=['POST'])
        def calculate_altitude():
            """
            Calcule les altitudes pour les points GPS fournis en utilisant l'API Open Elevation.
            Les données GPS doivent être envoyées sous forme de liste de points GPS, chaque point contenant les clés "Latitude", "Longitude" et "Timer".
            ATTENTION : Cette route nécessite une connexion Internet pour fonctionner. L'API Open Elevation peut être sujette à des blocages ou des limitations.
            """
            try:
                data = request.get_json()  # Récupère les données envoyées dans la requête
                gps_points = data.get("gps_points", [])

                # Vérifier si les données sont valides
                if not gps_points or not isinstance(gps_points, list):
                    return jsonify({"error": "Invalid GPS data format"}), 400

                # Vérifiez que chaque point GPS contient les clés nécessaires
                for point in gps_points:
                    if "Latitude" not in point or "Longitude" not in point or "Timer" not in point:
                        return jsonify({"error": "Missing required keys in GPS points"}), 400

                # Préparer les données pour l'API Open Elevation
                locations = [{"latitude": point["Latitude"], "longitude": point["Longitude"]} for point in gps_points]

                # Envoyer une requête POST à l'API Open Elevation
                response = requests.post(
                    OPEN_ELEVATION_API_URL,
                    json={"locations": locations},
                    timeout=10  # Timeout de 10 secondes pour éviter les blocages
                )

                if response.status_code != 200:
                    return jsonify({"error": "Failed to fetch altitude data from Open Elevation API"}), 502

                elevation_data = response.json().get("results", [])

                # Construire la réponse contenant les altitudes avec les timers correspondants
                altitudes = [
                    {
                        "Timer": gps_points[i]["Timer"],
                        "Altitude": elevation_data[i].get("elevation", 0)
                    }
                    for i in range(len(elevation_data))
                ]

                return jsonify(altitudes), 200

            except requests.exceptions.RequestException as e:
                return jsonify({"error": f"Request to Open Elevation API failed: {str(e)}"}), 500
            except Exception as e:
                return jsonify({"error": str(e)}), 500


        @app.route('/api/signup', methods=['POST'])
        def signup():
            print("Requête reçue pour /api/signup")
            try:
                data = request.get_json()
                print("Données reçues :", data)

                if not data:
                    return jsonify({"error": "Requête invalide, données manquantes."}), 400

                email = data.get("email")
                password = data.get("password")
                name = data.get("name")

                if not email or not password or not name:
                    print("Erreur : Champs requis manquants.")
                    return jsonify({"error": "Tous les champs sont requis."}), 400

                # Vérifier si l'utilisateur existe déjà
                if self.user_db_manager.get_user(email):
                    print("Erreur : L'adresse e-mail est déjà utilisée.")
                    return jsonify({"error": "L'adresse e-mail est déjà utilisée."}), 409

                # Hacher le mot de passe
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                print("Mot de passe haché :", hashed_password)

                # Ajouter l'utilisateur dans la base de données
                self.user_db_manager.register_user(email, hashed_password, name)
                print("Utilisateur inscrit :", email)
                return jsonify({"message": "Inscription réussie."}), 201

            except sqlite3.IntegrityError as e:
                print("Erreur SQLite :", str(e))
                return jsonify({"error": "Erreur dans la base de données."}), 500
            except Exception as e:
                print("Erreur inattendue :", str(e))
                return jsonify({"error": "Erreur du serveur."}), 500


        @app.route('/api/login', methods=['POST'])
        def login():
            """
            Route pour connecter un utilisateur existant.
            """
            data = request.get_json()
            email = data.get("email")
            password = data.get("password")

            # Vérifier les données
            if not email or not password:
                return jsonify({"error": "Email et mot de passe sont requis."}), 400

            # Hacher le mot de passe pour la comparaison
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Vérifier l'utilisateur dans la base de données
            user = self.user_db_manager.get_user(email)
            if user and user["password"] == hashed_password:
                # Renvoi de l'email comme identifiant utilisateur
                return jsonify({"message": "Connexion réussie.", "userId": email}), 200
                # return jsonify({"message": "Connexion réussie.", "user": {"email": user["email"], "name": user["name"]}}), 200
            return jsonify({"error": "E-mail ou mot de passe incorrect."}), 401
            
        @app.route('/api/clear-csv', methods=['POST'])
        def clear_csv_file():
            try:
                # Chemin vers le fichier CSV
                project_root = os.getcwd()  # Chemin racine du projet
                temp_file_path = os.path.join(project_root, "esp32_data.csv")  # Fichier directement dans la racine

                # Vérifier si le fichier existe
                if os.path.isfile(temp_file_path):
                    # Vérifier si le fichier n'est pas vide
                    if os.path.getsize(temp_file_path) > 0:
                        # Ouvrir le fichier en mode 'w' pour vider son contenu
                        with open(temp_file_path, mode='w', newline='') as file:
                            file.write("")  # Effacer tout le contenu du fichier
                        print(f"Le fichier {temp_file_path} a été vidé avec succès.")
                        return jsonify({"message": "Fichier vidé avec succès."}), 200
                    else:
                        return jsonify({"message": "Le fichier est déjà vide."}), 200
                else:
                    return jsonify({"error": "Fichier non trouvé."}), 404

            except Exception as e:
                print(f"Erreur lors de la suppression du contenu du fichier : {e}")
                return jsonify({"error": str(e)}), 500


        # Endpoint pour recevoir un fichier CSV
        @app.route('/api/upload-csv', methods=['POST'])
        def upload_csv():
            if 'file' not in request.files:
                return jsonify({"error": "Aucun fichier envoyé."}), 400

            file = request.files['file']
            print(f"Fichier reçu : {file.filename}")

            # Sauvegarde du fichier dans un dossier temporaire
            csv_file_path = os.path.join(os.getcwd(), "uploaded_esp32_data.csv")
            file.save(csv_file_path)

            # Charger le fichier CSV dans la base de données
            try:
                load_csv_file_to_database(csv_file_path=csv_file_path)
                return jsonify({"message": "Fichier CSV chargé dans la base de données avec succès."}), 200
            except Exception as e:
                return jsonify({"error": f"Erreur lors du chargement du fichier CSV : {str(e)}"}), 500

        
        @app.route('/api/receive-bluetooth-data', methods=['POST'])
        def receive_bluetooth_data():
            try:
                data = request.get_json().get("data", [])

                if not data:
                    return jsonify({"error": "Aucune donnée reçue."}), 400

                # Définir les en-têtes pour le fichier CSV
                headers = [
                    "Timer", "Accel1X", "Accel1Y", "Accel1Z", "Gyro1X", "Gyro1Y", "Gyro1Z",
                    "Accel2X", "Accel2Y", "Accel2Z", "Gyro2X", "Gyro2Y", "Gyro2Z",
                    "Flexion", "Latitude", "Longitude", "Altitude", "Vitesse", "Orientation", "Satellites", "HDOP"
                ]

                # Créer le fichier CSV à la racine du projet
                project_root = os.getcwd()  # Chemin racine du projet
                temp_file_path = os.path.join(project_root, "esp32_data.csv")  # Fichier directement dans la racine

                # Vérifier si le fichier existe déjà
                file_exists = os.path.isfile(temp_file_path)
                
                with open(temp_file_path, mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")

                    # Écrire l'en-tête uniquement si le fichier n'existe pas encore
                    if not file_exists:
                        writer.writeheader()

                    # Écrire les données reçues
                    for entry in data:
                        writer.writerow({
                            "Timer": entry.get("Timer"),
                            "Accel1X": entry.get("Accel1X"),
                            "Accel1Y": entry.get("Accel1Y"),
                            "Accel1Z": entry.get("Accel1Z"),
                            "Gyro1X": entry.get("Gyro1X"),
                            "Gyro1Y": entry.get("Gyro1Y"),
                            "Gyro1Z": entry.get("Gyro1Z"),
                            "Accel2X": entry.get("Accel2X"),
                            "Accel2Y": entry.get("Accel2Y"),
                            "Accel2Z": entry.get("Accel2Z"),
                            "Gyro2X": entry.get("Gyro2X"),
                            "Gyro2Y": entry.get("Gyro2Y"),
                            "Gyro2Z": entry.get("Gyro2Z"),
                            "Flexion": entry.get("Flexion"),
                            "Latitude": entry.get("Latitude"),
                            "Longitude": entry.get("Longitude"),
                            "Altitude": entry.get("Altitude"),
                            "Vitesse": entry.get("Vitesse"),
                            "Orientation": entry.get("Orientation"),
                            "Satellites": entry.get("Satellites"),
                            "HDOP": entry.get("HDOP")
                        })

                print(f"Fichier CSV mis à jour à la racine du projet : {temp_file_path}")
                return jsonify({"message": "Fichier CSV mis à jour avec succès.", "file_path": temp_file_path}), 200

            except Exception as e:
                print(f"Erreur lors de la mise à jour du fichier CSV : {e}")
                return jsonify({"error": str(e)}), 500

        @app.route('/api/save-course', methods=['POST'])
        def save_course():
            try:
                data = request.get_json()
                print("Données reçues par le serveur :", data)  # Ajout du log

                user_id = data.get('userId')
                file_name = data.get('file_name')
                uploaded_at = data.get('uploaded_at')

                if not user_id or not file_name or not uploaded_at:
                    return jsonify({"error": "Données manquantes pour l'enregistrement."}), 400

                # Connexion à la base de données
                conn = sqlite3.connect("user_data.db")
                cursor = conn.cursor()

                # Création de la table courses si elle n'existe pas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        file_name TEXT,
                        uploaded_at TEXT
                    )
                ''')

                # Insertion des données de la course
                cursor.execute('''
                    INSERT INTO courses (user_id, file_name, uploaded_at)
                    VALUES (?, ?, ?)
                ''', (user_id, file_name, uploaded_at))

                conn.commit()
                conn.close()

                return jsonify({"message": "Course enregistrée avec succès."}), 201

            except Exception as e:
                return jsonify({"error": f"Erreur lors de l'enregistrement : {str(e)}"}), 500



        @app.route('/api/get-courses', methods=['GET'])
        def get_courses():
            user_id = request.args.get('userId')
            if not user_id:
                return jsonify({"error": "ID utilisateur manquant."}), 400

            conn = sqlite3.connect("user_data.db")
            cursor = conn.cursor()

            cursor.execute('''
                SELECT file_name, uploaded_at FROM courses WHERE user_id = ?
            ''', (user_id,))
            rows = cursor.fetchall()
            conn.close()

            courses = [{"file_name": row[0], "uploaded_at": row[1]} for row in rows]
            return jsonify(courses)


        # Route pour charger le fichier CSV dans la base de données
        @app.route('/api/load-csv-to-db', methods=['POST'])
        def load_csv_to_db():
            try:
                # Chemin racine du projet
                project_root = os.getcwd()
                csv_file_path = os.path.join(project_root, "esp32_data.csv")

                # Vérifier si le fichier CSV existe
                if not os.path.isfile(csv_file_path):
                    return jsonify({"error": "Fichier CSV non trouvé."}), 404

                # Charger les données du fichier CSV dans la base de données
                load_csv_file_to_database(csv_file_path=csv_file_path)

                print(f"Le fichier CSV {csv_file_path} a été chargé dans la base de données.")
                return jsonify({"message": "Fichier CSV chargé avec succès dans la base de données."}), 200

            except Exception as e:
                print(f"Erreur lors du chargement du fichier CSV dans la base de données : {e}")
                return jsonify({"error": str(e)}), 500

        @app.route('/api/gpx-to-csv', methods=['POST'])
        def gpx_to_csv():
            if 'file' not in request.files:
                return jsonify({"error": "Aucun fichier GPX envoyé."}), 400

            file = request.files['file']
            gpx_data = file.read().decode('utf-8')

            # Analyse du fichier GPX
            gpx = gpxpy.parse(gpx_data)

            # Préparer les données pour le CSV
            data = []
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        data.append({
                            "Timer": point.time.strftime("%Y-%m-%d %H:%M:%S") if point.time else "",
                            "Latitude": point.latitude,
                            "Longitude": point.longitude,
                            "Altitude": point.elevation
                        })

            # Sauvegarde en CSV
            csv_file_path = os.path.join(os.getcwd(), "converted_gpx_data.csv")
            with open(csv_file_path, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=["Timer", "Latitude", "Longitude", "Altitude"], delimiter=";")
                writer.writeheader()
                writer.writerows(data)

            print(f"Fichier CSV créé : {csv_file_path}")
            return jsonify({"message": "Fichier GPX converti en CSV avec succès.", "file_path": csv_file_path}), 200

    def run(self, port=None):
        if port is None:
            port = int(os.environ.get("FLASK_RUN_PORT", 5000))
        self._initialize_database()
        print(f"Starting Flask server on port {port}...")
        self.app.run(debug=True, port=port, use_reloader=False)


if __name__ == "__main__":
    server = Server()
    server.run()