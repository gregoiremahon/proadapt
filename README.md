# ProAdapt: Kit de Capteurs pour Athlètes Amputés

## Introduction

**ProAdapt** est une solution innovante visant à aider les athlètes amputés à optimiser leurs performances sportives grâce à une analyse approfondie de leurs données biomécaniques et environnementales. Ce projet, développé par une équipe d’ingénieurs de Polytech Sorbonne en collaboration avec AthleteCare, s’inscrit dans une démarche inclusive et technologique.

## Fonctionnalités

- **Suivi biomécanique** : Accélération des jambes via des capteurs positionnés sur chaque prothèse.
- **Analyse environnementale** : Tracé GPS et suivi de l’altitude pour une compréhension globale des efforts.
- **Visualisation intuitive** : Application web affichant des graphiques dynamiques et une carte interactive.
- **Accessibilité** : Interface conviviale, pensée pour répondre aux besoins spécifiques des athlètes amputés.

## Architecture

Le projet repose sur deux principaux composants :

1. **Backend Flask** : Un serveur Python pour gérer les API, la base de données SQLite, et le traitement des fichiers de données.
2. **Frontend Vue.js** : Une interface utilisateur moderne pour visualiser les données sous forme de graphiques et cartes interactives.

### Organisation des Fichiers

```plaintext
.
├── database_manager.py      # Gestion de la base de données SQLite
├── server.py                # Serveur Flask pour les API
├── main.py                  # Point d'entrée principal pour lancer le projet
├── tools.py                 # Outils utilitaires (gestion des ports, etc.)
├── data/                    # Fichiers CSV pour initialiser la base
├── flask-port.txt           # Port utilisé par Flask
├── vue/                     # Application Vue.js
│   ├── src/                 # Code source Vue.js
│   ├── public/              # Fichiers publics (index.html, favicon, etc.)
│   └── vite.config.js       # Configuration Vite
└── README.md                # Documentation du projet
```
## Documentation de l'API

### Endpoints

### 1. `/api/sensor-data`

- **Méthode** : `GET`
- **Description** : Récupère les données des capteurs biomécaniques (accéléromètres).
- **Réponse** (au format json):
  - `Timer` : Horodatage en millisecondes.
  - `Accel1X`, `Accel1Y`, `Accel1Z` : Accélérations mesurées pour la jambe gauche.
  - `Accel2X`, `Accel2Y`, `Accel2Z` : Accélérations mesurées pour la jambe droite.


### 2. /api/gpx-data
- **Méthode** : `GET`
- **Description** : Récupère les données GPS, incluant les coordonnées et l'altitude.
- **Réponse** (json):
  - `Timer` : Horodatage en millisecondes.
  - `Latitude`, `Longitude` : Coordonnées GPS.
  - `Altitude` : Altitude en mètres. (via GPS)
  - `Satellites`, `HDOP` : Informations sur la précision GPS.

### 3. /api/gps-trace
- **Méthode** : `GET`
- **Description** : Récupère uniquement le tracé GPS.
- **Réponse** (json):
  - `Latitude`, `Longitude` : Coordonnées GPS du parcours.


### Utilisation
Toutes les requêtes API doivent être effectuées vers l'URL de base suivante :
```
http://127.0.0.1:<PORT_FLASK>/api
```
Il est possible de récupérer les données des capteurs avec `curl`:
- Récupérer les données des capteurs :
`curl http://127.0.0.1:5000/api/sensor-data`
- Récupérer les données GPS :
`curl http://127.0.0.1:5000/api/gpx-data`
- Récupérer uniquement le tracé GPS :
`curl http://127.0.0.1:5000/api/gps-trace`


## Prérequis 
- Python 3.6 ou plus récent
- Node.js 16 ou plus récent
- npm (Node Package Manager)

## Installation
1. Clonez le dépot :
    ``` 
    git clone <https://github.com/gregoiremahon/proadapt.git>
    cd ProAdapt
    ```
2. Installez les dépendances backend :
    ```
    pip install -r requirements.txt
    ```
3. Installez les dépendances frontend :
    ```
    cd vue
    npm install
    cd ..
    ```

## Utilisation
1. Démarrez l'application via ```main.py```
- Le script initialise la base de données, démarre le serveur Flask, et exécute le serveur de développement Vue.js.
- -> Les ports Flask et Vue.js sont automatiquement gérés.
2. Accédez à l’application (en local) : Ouvrez votre navigateur à l’adresse affichée dans la console (par défaut : http://127.0.0.1:5173). Le port peut être différent en fonction des disponibilités sur votre machine.

## Points Clés Techniques
- Ports Dynamiques : Les ports de Flask et Vue.js sont automatiquement déterminés et partagés via des fichiers de configuration (flask-port.txt et dev-port.txt).
- Base de Données : SQLite est utilisé pour stocker les données des capteurs et les tracés GPS, formatées sous forme de CSV par notre appareil.
- Visualisation : Les graphiques sont générés avec Chart.js et les cartes interactives avec Leaflet.

## Auteurs
Équipe ProAdapt : Étudiants en ingénierie à Polytech Sorbonne : 
- Grégoire MAHON
- Armand LELONG
- Jonathan QUEYROI
- Sylvain PLAZE
- Chahine Boukhenaissi

