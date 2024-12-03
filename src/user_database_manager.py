import sqlite3
import os

class UserDatabaseManager:
    def __init__(self, db_name="user_data.db"):
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """
        Initialise la base de données en créant les tables nécessaires si elles n'existent pas.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            # Table des utilisateurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL
                )
            ''')
            print("Table 'users' initialisée.")

            # Table des fichiers de courses
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    file_name TEXT NOT NULL,
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            print("Table 'courses' initialisée.")

            connection.commit()

    def register_user(self, email, password, name):
        """
        Inscrit un nouvel utilisateur dans la base de données.
        """
        try:
            with sqlite3.connect(self.db_name) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO users (email, password, name) VALUES (?, ?, ?)",
                    (email, password, name)
                )
                connection.commit()
                print(f"Utilisateur {email} enregistré avec succès.")
                return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print("Erreur SQLite :", e)
            return None

    def login_user(self, email, password):
        """
        Vérifie les identifiants de l'utilisateur.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
            user = cursor.fetchone()
            return user[0] if user else None

    def add_course_file(self, user_id, file_name):
        """
        Ajoute un fichier de course associé à un utilisateur.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO courses (user_id, file_name) VALUES (?, ?)", (user_id, file_name))
            connection.commit()

    def get_course_files(self, user_id):
        """
        Récupère les fichiers de course associés à un utilisateur.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT file_name, uploaded_at FROM courses WHERE user_id = ?", (user_id,))
            return cursor.fetchall()

    def get_user(self, email):
        """
        Récupère un utilisateur par son email.
        """
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "email": row[1], "password": row[2], "name": row[3]}
            return None


# Test de l'initialisation
if __name__ == "__main__":
    db_manager = UserDatabaseManager()
    print("Base de données initialisée.")
