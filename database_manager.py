import sqlite3
import csv
import os

class DatabaseManager:
    def __init__(self, db_name):
        # Vérifie si la base de données existe, sinon elle est créée automatiquement
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.initialize_database()

    def initialize_database(self):
        # Crée les tables nécessaires si elles n'existent pas déjà
        self.create_table(
            'sensor_data',
            [
                'Timer INTEGER',
                'Accel1X INTEGER', 'Accel1Y INTEGER', 'Accel1Z INTEGER',
                'Gyro1X INTEGER', 'Gyro1Y INTEGER', 'Gyro1Z INTEGER',
                'Accel2X INTEGER', 'Accel2Y INTEGER', 'Accel2Z INTEGER',
                'Gyro2X INTEGER', 'Gyro2Y INTEGER', 'Gyro2Z INTEGER'
            ]
        )
        self.create_table(
            'gpx_data',
            [
                'Timer INTEGER',
                'Latitude REAL', 'Longitude REAL', 'Altitude REAL',
                'Vitesse REAL', 'Orientation REAL', 'Satellites INTEGER', 'HDOP REAL'
            ]
        )

    def create_table(self, table_name, fields):
        fields_definition = ', '.join(fields)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_definition})"
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def load_csv_to_db(self, csv_file_path):
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                # Insertion dans la table sensor_data
                self.insert_into_table(
                    'sensor_data',
                    [
                        row['Timer'], row['Accel1X'], row['Accel1Y'], row['Accel1Z'],
                        row['Gyro1X'], row['Gyro1Y'], row['Gyro1Z'],
                        row['Accel2X'], row['Accel2Y'], row['Accel2Z'],
                        row['Gyro2X'], row['Gyro2Y'], row['Gyro2Z']
                    ]
                )
                # Insertion dans la table gpx_data
                self.insert_into_table(
                    'gpx_data',
                    [
                        row['Timer'], row.get('Latitude', None), row.get('Longitude', None),
                        row.get('Altitude', None), row.get('Vitesse', None),
                        row.get('Orientation', None), row.get('Satellites', None),
                        row.get('HDOP', None)
                    ]
                )

    def insert_into_table(self, table_name, values):
        placeholders = ', '.join(['?'] * len(values))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_query, values)
        self.connection.commit()

    def close(self):
        self.connection.close()

# Exemple d'utilisation :
db_manager = DatabaseManager('sensor_data.db')
db_manager.load_csv_to_db('./data/gpx-data.csv')
db_manager.close()
