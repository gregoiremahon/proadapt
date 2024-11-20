import logging
from multiprocessing import Process
from database_manager import DatabaseManager
from tools import find_free_port
import os
import subprocess

class Application:
    def __init__(self, db_name="sensor_data.db"):
        self.db_name = db_name
        self.csv_file_path = "./data/GPS_OK.csv"
        self.server_port = find_free_port()
        self.vue_port = 5173  # Port par défaut pour Vue.js

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger("ProAdaptApp")

    def initialize_database(self):
        self.logger.info("Initializing the database...")
        db_manager = DatabaseManager(self.db_name)
        db_manager.initialize_database()
        db_manager.load_csv_to_db(csv_file_path=self.csv_file_path)

    def start_server(self):
        self.logger.info(f"Starting Flask server on port {self.server_port}...")
        os.environ["FLASK_RUN_PORT"] = str(self.server_port)
        os.system("python3 server.py")

    def start_vue(self):
        self.logger.info(f"Starting Vue.js dev server on port {self.vue_port}...")
        os.environ["VUE_DEV_PORT"] = str(self.vue_port)
        subprocess.run(["npm", "run", "dev"], cwd="./", check=True)

    def run(self):
        self.setup_logging()
        self.logger.info("Starting the ProAdapt application...")

        try:
            self.initialize_database()

            # Démarrer le serveur Flask dans un processus séparé
            server_process = Process(target=self.start_server)
            server_process.start()
            self.logger.info(f"Server process started with PID {server_process.pid}")

            # Démarrer le serveur Vue.js dans un autre processus séparé
            vue_process = Process(target=self.start_vue)
            vue_process.start()
            self.logger.info(f"Vue.js dev server started with PID {vue_process.pid}")

            # Attendre que les processus se terminent
            server_process.join()
            vue_process.join()

        except KeyboardInterrupt:
            self.logger.info("Application interrupted. Shutting down gracefully...")
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
        finally:
            self.logger.info("ProAdapt application stopped.")


if __name__ == "__main__":
    app = Application()
    app.run()
