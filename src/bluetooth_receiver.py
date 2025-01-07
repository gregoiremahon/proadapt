import serial
import sqlite3
import os
import csv
import sys

HEADERS = [
    "Timer", "Accel1X", "Accel1Y", "Accel1Z", 
    "Gyro1X", "Gyro1Y", "Gyro1Z", "Accel2X", 
    "Accel2Y", "Accel2Z", "Gyro2X", "Gyro2Y", 
    "Gyro2Z", "Flexion", "Latitude", "Longitude", 
    "Altitude", "Vitesse", "Orientation", "Satellites", "HDOP"
]

def delete_file_if_exists(file_path):
    """
    Supprime un fichier s'il existe.
    
    :param file_path: Chemin du fichier à supprimer
    """
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Fichier supprimé : {file_path}")
        else:
            print(f"Le fichier n'existe pas : {file_path}")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier : {e}")


class BluetoothReceiver:
    def __init__(self, port="/dev/tty.ESP32SYL", baudrate=9600, db_name="sensor_data.db", csv_file="./data/sensor_data.csv"):
        self.port = port
        self.baudrate = baudrate
        self.db_name = db_name
        self.csv_file = csv_file
        delete_file_if_exists(file_path=self.csv_file) # Supprime le fichier s'il existe déjà
        self.serial_connection = None

    def connect(self):
        """
        Connecte au périphérique Bluetooth ESP32.
        """
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            print(f"Connected to ESP32 on {self.port} at {self.baudrate} baudrate.")
        except Exception as e:
            print(f"Failed to connect to ESP32: {e}")
    
    def insert_data_to_db(self, data):
        """
        Insère les données dans les tables 'sensor_data' et 'gpx_data'.
        """
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                
                # Insérer dans la table sensor_data (les 13 premières colonnes)
                cursor.execute('''
                    INSERT INTO sensor_data (
                        Timer, Accel1X, Accel1Y, Accel1Z, 
                        Gyro1X, Gyro1Y, Gyro1Z, 
                        Accel2X, Accel2Y, Accel2Z, 
                        Gyro2X, Gyro2Y, Gyro2Z
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data[:13])
                
                # Insérer dans la table gpx_data (les données GPS)
                cursor.execute('''
                    INSERT INTO gpx_data (
                        Timer, Latitude, Longitude, Altitude, Vitesse, Orientation, Satellites, HDOP
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', [data[0], data[14], data[15], data[16], data[17], data[18], data[19], data[20]])
                
                conn.commit()
                print("Données insérées dans la base de données :", data)
        except Exception as e:
            print(f"Erreur lors de l'insertion dans la base de données : {e}")

    def write_data_to_csv(self, data):
        """
        Écrit les données dans un fichier CSV, ajoute les en-têtes si nécessaires.
        """
        file_exists = os.path.isfile(self.csv_file)
        
        with open(self.csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Ajoute les données
            writer.writerow(data)

    def listen(self):
        """
        Écoute les données transmises par l'ESP32, gère l'envoi de la commande '18' 
        et traite les données reçues jusqu'à recevoir 186.
        """
        if not self.serial_connection:
            print("Not connected to any device.")
            return

        try:
            # Envoie de la commande '18' pour demander les données
            self.serial_connection.write(b'18\n')
            print("Sent '18' to request data.")

            data_started = False

            while True:
                # Lecture d'une ligne de données
                raw_data = self.serial_connection.readline().decode('utf-8').strip()

                if not raw_data:
                    continue  # Ignore les lignes vides

                print(f"Received: {raw_data}")

                if raw_data == "184":  # Début de la transmission
                    print("Start of data transmission.")
                    data_started = True
                    continue

                if raw_data == "186":  # Fin de la transmission
                    print("End of data transmission.")
                    break

                if not data_started:
                    # Avant 184, on ignore les données
                    continue

                # Les données doivent correspondre aux en-têtes
                data = raw_data.split(";")
                print("ICI : ", len(data) == len(HEADERS))
                print("LEN DATA et LEN HEADERS : ", len(data), len(HEADERS))
                if len(data) == len(HEADERS):
                    self.write_data_to_csv(data)  # Écriture dans le fichier CSV
                    self.insert_data_to_db(data)  # Ajout dans la base de données
                else:
                    print(f"Unexpected data format: {raw_data}")

        except KeyboardInterrupt:
            print("Stopped listening.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if self.serial_connection:
                self.serial_connection.close()
                print("Connection closed.")

if __name__ == "__main__":
    receiver = BluetoothReceiver()
    receiver.connect()
    receiver.listen()
