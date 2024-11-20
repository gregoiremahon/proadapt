# Utils functions for the ProAdapt project

import os
import socket

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Demande un port libre
        port = int(s.getsockname()[1])  # Récupère le port attribué
        # On ne ferme pas le socket immédiatement pour éviter la réutilisation
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        write_flask_port_to_file(port)  # Écrit le port dans flask-port.txt
        return port

def get_vue_port():
    try:
        # Lit le port depuis le fichier généré par Vue.js
        with open('dev-port.txt', 'r') as f:
            port = int(f.read().strip())
            return port
    except FileNotFoundError:
        # Port par défaut si le fichier n'existe pas encore
        return 5173
    except:
        # En cas d'erreur, port par défaut = 5173
        return 5173
    
def write_flask_port_to_file(port):
    with open("flask-port.txt", "w") as f:
        f.write(str(port))
