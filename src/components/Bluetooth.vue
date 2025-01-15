<script setup>
import { ref } from 'vue';

const connectionStatus = ref('Non connecté');
const isConnecting = ref(false);
const isSending17 = ref(false);
const isSending18 = ref(false);
let bleDevice = null;
let gattCharacteristic = null;

async function clearCsvFile() {
  try {
    const response = await fetch("http://127.0.0.1:5173/api/clear-csv", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    const result = await response.json();
    console.log(result.message);
    connectionStatus.value = result.message;  // Afficher le message
  } catch (error) {
    console.error("Erreur lors de la suppression du contenu du fichier :", error);
  }
}

// Fonction pour charger le CSV dans la base de données
async function loadCsvToDb() {
  try {
    const response = await fetch("http://127.0.0.1:5173/api/load-csv-to-db", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });

    const result = await response.json();
    console.log(result.message);
    connectionStatus.value = result.message;
  } catch (error) {
    console.error("Erreur lors du chargement du fichier CSV dans la base de données :", error);
  }
}

async function connectBluetooth() {
  isConnecting.value = true;
  try {
    bleDevice = await navigator.bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: ['19b10000-e8f2-537e-4f6c-d104768a1214'], // UUID du service
    });

    const server = await bleDevice.gatt.connect();
    const service = await server.getPrimaryService('19b10000-e8f2-537e-4f6c-d104768a1214'); // Service UUID
    gattCharacteristic = await service.getCharacteristic('87654321-4321-4321-4321-0987654321fe'); // Characteristic UUID

    // Supprimer tous les anciens écouteurs pour éviter les doublons
    gattCharacteristic.removeEventListener('characteristicvaluechanged', handleDataReceived);

    // Ajouter l'écouteur uniquement si ce n'est pas déjà fait
    if (!gattCharacteristic._isListening) {
      await gattCharacteristic.startNotifications(); // Activer les notifications
      gattCharacteristic.addEventListener('characteristicvaluechanged', handleDataReceived);
      gattCharacteristic._isListening = true;  // Marquer qu'on écoute déjà
    }

    connectionStatus.value = `Connecté à ${bleDevice.name}`;
    console.log('Connexion BLE réussie !');
  } catch (error) {
    connectionStatus.value = 'Échec de la connexion : ' + error.message;
    console.error('Erreur lors de la connexion BLE :', error);
  } finally {
    isConnecting.value = false;
  }
}


// Fonction pour gérer les données reçues de l'ESP32
function handleDataReceived(event) {
  const value = new TextDecoder().decode(event.target.value);
  if (value === "186" || value === 186) {
    console.log(value)
    console.log('Fin de la réception des paquets détectée.');

    // Charger les données dans la base de données
    loadCsvToDb(); // Appel automatique après réception complète des paquets
  }
  if (value.includes(";")) {
    // Nettoyer les caractères `\r` en remplaçant par un espace vide
    const cleanedValue = value.replace(/\r/g, "");
    const rows = cleanedValue.split("\n").filter(row => row.trim() !== "");

    if (rows.length < 1) {
      console.warn("Le CSV ne contient pas suffisamment de lignes de données.");
      return;
    }

    // Utiliser les en-têtes complets envoyés
    const headers = [
      "Timer", "Accel1X", "Accel1Y", "Accel1Z", "Gyro1X", "Gyro1Y", "Gyro1Z",
      "Accel2X", "Accel2Y", "Accel2Z", "Gyro2X", "Gyro2Y", "Gyro2Z",
      "Flexion", "Latitude", "Longitude", "Altitude", "Vitesse", "Orientation", "Satellites", "HDOP"
    ];

    const dataObjects = rows.map(row => {
      const values = row.split(";");
      return headers.reduce((obj, header, index) => {
        obj[header.trim()] = values[index]?.trim() || null;  // Si une valeur est manquante, la remplacer par null
        return obj;
      }, {});
    });

    sendToServer(dataObjects);
  } else {
    console.warn("Format inattendu : les données reçues ne contiennent pas de séparateur ';'.");
  }
}

async function sendToServer(data) {
  // Vérification avant l'envoi
  if (!Array.isArray(data) || data.length === 0) {
    console.error("Aucune donnée à envoyer au serveur.");
    connectionStatus.value = "Aucune donnée à envoyer.";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5173/api/receive-bluetooth-data", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data }), // Envoyer un objet { "data": [...] }
    });

    if (response.ok) {
      console.log("Données envoyées au serveur avec succès !");
      connectionStatus.value = "Données envoyées au serveur et enregistrées.";
    } else {
      const errorData = await response.json();
      console.error("Erreur lors de l'envoi des données au serveur : ", errorData.error);
    }
  } catch (error) {
    console.error("Erreur lors de l'envoi des données : ", error);
  }
  
}

// Fonction pour envoyer le code "18" pour recevoir les données accumulées
async function sendCode18() {
  if (!gattCharacteristic) {
    console.error('Aucune caractéristique BLE disponible.');
    connectionStatus.value = 'Veuillez vous connecter avant d’envoyer le code 18.';
    return;
  }

  isSending18.value = true;
  clearCsvFile()
  try {
    const textEncoder = new TextEncoder(); // Crée un encodeur pour convertir en bytes
    const buffer = textEncoder.encode("18"); // Convertit la chaîne "18" en binaire
    await gattCharacteristic.writeValue(buffer); // Écrire la chaîne encodée en binaire
    console.log('Code "18" envoyé à l’ESP32');
  } catch (error) {
    console.error('Erreur lors de l’envoi du code 18 :', error);
    connectionStatus.value = 'Erreur lors de l’envoi du code 18.';
  } finally {
    isSending18.value = false;
  }
  console.log('JVIUREHBIUERHIVUE')
}

// Fonction pour déconnecter l'ESP32
async function disconnectBluetooth() {
  if (bleDevice && bleDevice.gatt.connected) {
    bleDevice.gatt.disconnect();
    connectionStatus.value = 'Déconnecté';
    console.log('ESP32 déconnecté.');
  } else {
    console.warn('Aucun appareil connecté.');
  }
}

// Fonction pour charger un fichier CSV sélectionné par l'utilisateur
async function handleFileUpload(event) {
  const file = event.target.files[0];
  if (!file) {
    console.warn("Aucun fichier sélectionné.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("http://127.0.0.1:5173/api/upload-csv", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    console.log(result.message);
    connectionStatus.value = result.message;  // Affiche un message à l'utilisateur
  } catch (error) {
    console.error("Erreur lors du chargement du fichier CSV :", error);
    connectionStatus.value = "Erreur lors du chargement du fichier CSV.";
  }
}

</script>

<template>
  <section class="bg-white dark:bg-gray-900 py-12 pt-28">
    <div class="max-w-screen-xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">
        Connexion Bluetooth
      </h1>
      <p class="text-lg text-gray-700 dark:text-gray-300 mb-6">{{ connectionStatus }}</p>

      <!-- Bouton pour se connecter -->
      <button
        @click="connectBluetooth"
        :disabled="isConnecting"
        class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-500 dark:hover:bg-blue-600 focus:outline-none dark:focus:ring-blue-800"
      >
        {{ isConnecting ? 'Connexion en cours...' : 'Se connecter à l’ESP32' }}
      </button>

      <!-- Bouton pour envoyer le code 18 -->
      <button
        @click="sendCode18"
        :disabled="!bleDevice || isSending18"
        class="text-white bg-yellow-600 hover:bg-yellow-700 focus:ring-4 focus:ring-yellow-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-yellow-500 dark:hover:bg-yellow-600 focus:outline-none dark:focus:ring-yellow-800 mt-4"
      >
        {{ isSending18 ? 'Envoi en cours...' : 'Synchroniser l appareil' }}
      </button>

      <!-- Bouton pour déconnecter -->
      <button
        @click="disconnectBluetooth"
        class="text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-red-500 dark:hover:bg-red-600 focus:outline-none dark:focus:ring-red-800 mt-4"
      >
        Déconnecter l’ESP32
      </button>
      <!-- Bouton pour charger un fichier CSV -->
      <div class="mt-6">
        <label
          for="file-input"
          class="cursor-pointer bg-green-600 text-white font-medium rounded-lg text-sm px-4 py-2 hover:bg-green-700 focus:outline-none focus:ring-4 focus:ring-green-300"
        >
          Charger un fichier CSV
        </label>
        <input
          id="file-input"
          type="file"
          accept=".csv"
          @change="handleFileUpload"
          class="hidden"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
button {
  margin: 10px;
}
</style>
