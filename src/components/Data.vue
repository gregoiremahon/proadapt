<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

Chart.register(...registerables)

// Références pour les données des graphiques
const accelerometerData = ref({
  labels: [],
  leftLeg: {
    x: [],
    y: [],
    z: [],
  },
  rightLeg: {
    x: [],
    y: [],
    z: [],
  },
})

const gpsData = ref({
  labels: [],
  datasets: [
    {
      label: 'Altitude',
      backgroundColor: 'rgba(75, 75, 192, 0.2)',
      borderColor: 'rgba(75, 75, 192, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
  ],
})

// Carte et tracé GPS
const map = ref(null)
const gpsTrace = ref([])

// Fonction utilitaire pour lire le port depuis un fichier
const getFlaskPort = async (defaultPort = 5000) => {
  try {
    const response = await fetch('/flask-port.txt')
    if (response.ok) {
      const portText = await response.text()
      return parseInt(portText.trim(), 10)
    }
    console.warn('Fichier flask-port.txt introuvable ou illisible, utilisation du port par défaut.')
  } catch (error) {
    console.error('Erreur lors de la lecture du port Flask :', error)
  }
  return defaultPort
}

// Fonction utilitaire pour effectuer une requête et gérer les erreurs
const fetchData = async (url, defaultValue = []) => {
  try {
    const response = await fetch(url)
    if (response.ok) {
      return await response.json()
    }
    console.warn(`Requête échouée pour l'URL : ${url}`)
  } catch (error) {
    console.error(`Erreur lors de la requête vers ${url} :`, error)
  }
  return defaultValue
}

// Fonction utilitaire pour calculer l'altitude à partir des données GPS
const calculateAltitude = async (gpsTrace) => {
  const flaskPort = await getFlaskPort();
  const baseURL = `http://127.0.0.1:${flaskPort}`;
  try {
    const response = await fetch(`${baseURL}/api/calculate-altitude`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gps_points: gpsTrace }),
    });

    if (response.ok) {
      return await response.json();
    } else {
      console.warn('Failed to calculate altitudes.');
      return [];
    }
  } catch (error) {
    console.error('Erreur lors de la requête d’altitude :', error);
    return [];
  }
};

// Fonction principale pour charger les données
const loadData = async () => {
  try {
    const flaskPort = await getFlaskPort();
    const baseURL = `http://127.0.0.1:${flaskPort}`;

    // Charger les données des capteurs
    const sensorData = await fetchData(`${baseURL}/api/sensor-data`);
    if (sensorData.length > 0) {
      accelerometerData.value.labels = sensorData.map((item) => item.Timer / 1000);
      // Jambe gauche (accelerometre 1)
      accelerometerData.value.leftLeg.x = sensorData.map((item) => item.Accel1X || 0); 
      accelerometerData.value.leftLeg.y = sensorData.map((item) => item.Accel1Y || 0);
      accelerometerData.value.leftLeg.z = sensorData.map((item) => item.Accel1Z || 0);
      // Jambe droite (accelerometre 2)
      accelerometerData.value.rightLeg.x = sensorData.map((item) => item.Accel2X || 0);
      accelerometerData.value.rightLeg.y = sensorData.map((item) => item.Accel2Y || 0);
      accelerometerData.value.rightLeg.z = sensorData.map((item) => item.Accel2Z || 0);
    }

    // Charger les données GPS (tracé + altitude)
    const gpsTraceResponse = await fetchData(`${baseURL}/api/gps-trace`);
    const validTraceData = gpsTraceResponse.filter(
      (point) => point.Latitude && point.Longitude
    );

    if (validTraceData.length > 0) {
      // Calcul de l'altitude à partir des données GPS
      const calculatedAltitudes = await calculateAltitude(validTraceData);
      gpsData.value.labels = calculatedAltitudes
        .filter((item) => item.Altitude > 0)
        .map((item) => item.Timer / 1000);
      gpsData.value.datasets[0].data = calculatedAltitudes
        .filter((item) => item.Altitude > 0)
        .map((item) => item.Altitude);

      // Ajouter le tracé GPS à la carte
      if (map.value && validTraceData.length > 0) {
        const polyline = L.polyline(
          validTraceData.map((point) => [point.Latitude, point.Longitude]),
          { color: 'orange' }
        ).addTo(map.value);

        map.value.fitBounds(polyline.getBounds());
      }
    } else {
      console.warn('Aucune donnée GPS valide trouvée.');
    }
  } catch (error) {
    console.error('Erreur lors du chargement des données :', error);
  }
};


// Charger les données et initialiser la carte lorsque le composant est monté
onMounted(() => {
  loadData()

  // Initialiser la carte OpenStreetMap
  map.value = L.map('map').setView([48.8566, 2.3522], 13) // Coordonnées de départ (Paris)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      'Ceci est une carte :)',
  }).addTo(map.value)
})

</script>

<template>
  <section class="bg-white dark:bg-gray-900 py-12 pt-28">
    <div class="max-w-screen-xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">
        Analyse des données de foulée et du parcours
      </h1>

      <!-- Graphiques des accéléromètres -->
      <div v-for="axis in ['x', 'y', 'z']" :key="axis" class="mb-12">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Accélération - Axe {{ axis.toUpperCase() }}
        </h2>
        <div class="max-w-4xl mx-auto chart-container">
          <Line
            :data="{
              labels: accelerometerData.labels,
              datasets: [
                {
                  label: `Jambe gauche (${axis.toUpperCase()})`,
                  backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  borderColor: 'rgba(75, 192, 192, 1)',
                  data: accelerometerData.leftLeg[axis],
                },
                {
                  label: `Jambe droite (${axis.toUpperCase()})`,
                  backgroundColor: 'rgba(192, 75, 75, 0.2)',
                  borderColor: 'rgba(192, 75, 75, 1)',
                  data: accelerometerData.rightLeg[axis],
                },
              ],
            }"
            :options="{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: { title: { display: true, text: 'Temps (secondes)' } },
                y: { title: { display: true, text: 'Accélération (g)' } },
              },
              plugins: { legend: { position: 'top' } },
            }"
          />
        </div>
      </div>

      <!-- Graphique de l'altitude -->
      <div class="max-w-4xl mx-auto mb-12">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Altitude pendant la course
        </h2>
        <div v-if="gpsData.labels.length > 0" class="chart-container">
          <Line
            :data="gpsData"
            :options="{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: { title: { display: true, text: 'Temps (secondes)' } },
                y: {
                  title: { display: true, text: 'Altitude (mètres)' },
                  min: 0,
                  max: Math.max(...gpsData.datasets[0].data) + 5, // Dynamique -> Altitude max + 5m
                },
              },
              plugins: { legend: { position: 'top' } },
            }"
          />
        </div>
        <p v-else class="text-gray-500 dark:text-gray-400">
          Aucune donnée GPS disponible.
        </p>
      </div>

      <!-- Carte OpenStreetMap -->
      <div class="max-w-4xl mx-auto mb-12">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Tracé GPS de la course
        </h2>
        <div id="map" class="map-container"></div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;  
  width: 100%;
}

.map-container {
  height: 500px;
  width: 100%;
  border: 2px solid #ccc;
  border-radius: 8px;
}
</style>
