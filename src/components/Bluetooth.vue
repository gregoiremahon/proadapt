<script setup>
import { ref } from 'vue';

const connectionStatus = ref('Non connecté');
const isConnecting = ref(false);
const isTransferring = ref(false);
const device = ref(null); // Stocker le périphérique Bluetooth
const server = ref(null); // Stocker le serveur GATT
const serviceUUID = 'battery_service'; // Remplacez par le service utilisé par l'ESP32
const characteristicUUID = 'battery_level'; // Remplacez par la caractéristique utilisée par l'ESP32
const receivedData = ref([]); // Stocker les données reçues

async function connectBluetooth() {
  isConnecting.value = true;
  try {
    // Demander à l'utilisateur de se connecter au périphérique Bluetooth
    device.value = await navigator.bluetooth.requestDevice({
      acceptAllDevices: true,
      optionalServices: [serviceUUID],
    });

    // Se connecter au serveur GATT
    server.value = await device.value.gatt.connect();
    connectionStatus.value = `Connecté à ${device.value.name || 'un périphérique'}`;
  } catch (error) {
    connectionStatus.value = 'Échec de la connexion : ' + error.message;
  } finally {
    isConnecting.value = false;
  }
}

async function transferData() {
  if (!device.value || !server.value) {
    console.error('ESP32 non connecté');
    connectionStatus.value = 'ESP32 non connecté';
    return;
  }

  isTransferring.value = true;
  try {
    // Accéder au service et à la caractéristique pour lire les données
    const service = await server.value.getPrimaryService(serviceUUID);
    const characteristic = await service.getCharacteristic(characteristicUUID);

    // Lire les données brutes depuis la caractéristique
    const value = await characteristic.readValue();
    const decoder = new TextDecoder('utf-8');
    const data = decoder.decode(value);

    // Transformer les données en JSON (si l'ESP32 envoie des données au format JSON)
    const parsedData = JSON.parse(data);
    console.log('Données reçues depuis l\'ESP32 :', parsedData);
    receivedData.value = parsedData;

    // Envoyer les données au serveur Flask
    const response = await fetch('http://127.0.0.1:5173/api/receive-bluetooth-data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(parsedData),
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Données transférées avec succès :', result);
    } else {
      console.error('Erreur lors du transfert des données vers le serveur.');
    }
  } catch (error) {
    console.error('Erreur lors du transfert des données :', error);
  } finally {
    isTransferring.value = false;
  }
}
</script>

<template>
  <section class="bg-white dark:bg-gray-900 py-12 pt-28">
    <div class="max-w-screen-xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">
        Connexion Bluetooth et Transfert des Données
      </h1>
      <p class="text-lg text-gray-700 dark:text-gray-300 mb-6">{{ connectionStatus }}</p>
      <button
        @click="connectBluetooth"
        :disabled="isConnecting"
        class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-500 dark:hover:bg-blue-600 focus:outline-none dark:focus:ring-blue-800"
      >
        {{ isConnecting ? 'Connexion en cours...' : 'Se connecter à l’ESP32' }}
      </button>
      <button
        @click="transferData"
        :disabled="isTransferring || !device"
        class="text-white bg-green-600 hover:bg-green-700 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-green-500 dark:hover:bg-green-600 focus:outline-none dark:focus:ring-green-800 mt-4"
      >
        {{ isTransferring ? 'Transfert en cours...' : 'Transférer les données' }}
      </button>
    </div>
  </section>
</template>

<style scoped>
/* Ajoutez du style si nécessaire */
</style>
