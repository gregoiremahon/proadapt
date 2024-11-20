import sqlite3
import csv
import os

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def initialize_database(self):
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            self.create_table(cursor, 'sensor_data', [
                'Timer INTEGER',
                'Accel1X INTEGER', 'Accel1Y INTEGER', 'Accel1Z INTEGER',
                'Gyro1X INTEGER', 'Gyro1Y INTEGER', 'Gyro1Z INTEGER',
                'Accel2X INTEGER', 'Accel2Y INTEGER', 'Accel2Z INTEGER',
                'Gyro2X INTEGER', 'Gyro2Y INTEGER', 'Gyro2Z INTEGER'
            ])
            self.create_table(cursor, 'gpx_data', [
                'Timer INTEGER',
                'Latitude REAL', 'Longitude REAL', 'Altitude REAL',
                'Vitesse REAL', 'Orientation REAL', 'Satellites INTEGER', 'HDOP REAL'
            ])
            connection.commit()

    def create_table(self, cursor, table_name, fields):
        fields_definition = ', '.join(fields)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_definition})"
        cursor.execute(create_table_query)

    def load_csv_to_db(self, csv_file_path):
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            with open(csv_file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                for row in csv_reader:
                    self.insert_into_table(cursor, 'sensor_data', [
                        row['Timer'], row['Accel1X'], row['Accel1Y'], row['Accel1Z'],
                        row['Gyro1X'], row['Gyro1Y'], row['Gyro1Z'],
                        row['Accel2X'], row['Accel2Y'], row['Accel2Z'],
                        row['Gyro2X'], row['Gyro2Y'], row['Gyro2Z']
                    ])
                    self.insert_into_table(cursor, 'gpx_data', [
                        row['Timer'], row.get('Latitude', None), row.get('Longitude', None),
                        row.get('Altitude', None), row.get('Vitesse', None),
                        row.get('Orientation', None), row.get('Satellites', None),
                        row.get('HDOP', None)
                    ])
            connection.commit()

    def insert_into_table(self, cursor, table_name, values):
        placeholders = ', '.join(['?'] * len(values))
        insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cursor.execute(insert_query, values)
