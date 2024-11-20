<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

Chart.register(...registerables)

// Références pour les données des graphiques
const stepData = ref({
  labels: [],
  datasets: [
    {
      label: 'Accéléromètre - Jambe gauche (Z)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
    {
      label: 'Accéléromètre - Jambe droite (Z)',
      backgroundColor: 'rgba(192, 75, 75, 0.2)',
      borderColor: 'rgba(192, 75, 75, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
  ],
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

// Fonction pour charger les données depuis le serveur
const loadData = async () => {
  try {
    // Requête pour récupérer les données des capteurs
    const sensorResponse = await fetch('http://127.0.0.1:5000/api/sensor-data')
    const sensorData = await sensorResponse.json()

    if (sensorData.length > 0) {
      const labels = sensorData.map(item => item.Timer / 1000) // Convertir Timer en secondes
      const accelLeft = sensorData.map(item => item.Accel1Z) // Jambe gauche
      const accelRight = sensorData.map(item => item.Accel2Z) // Jambe droite

      stepData.value.labels = labels
      stepData.value.datasets[0].data = accelLeft
      stepData.value.datasets[1].data = accelRight
    }

    // Requête pour récupérer les données GPS (Altitude)
    const gpsResponse = await fetch('http://127.0.0.1:5000/api/gpx-data')
    const gpsDataResponse = await gpsResponse.json()

    if (gpsDataResponse.length > 0) {
      const labels = gpsDataResponse.map(item => item.Timer / 1000) // Temps en secondes
      const altitudes = gpsDataResponse.map(item => item.Altitude)

      gpsData.value.labels = labels
      gpsData.value.datasets[0].data = altitudes
    }

    // Requête pour récupérer le tracé GPS
    const gpsTraceResponse = await fetch('http://127.0.0.1:5000/api/gps-trace')
    gpsTrace.value = await gpsTraceResponse.json()

    // Ajouter le tracé sur la carte
    if (map.value && gpsTrace.value.length > 0) {
      const polyline = L.polyline(
        gpsTrace.value.map(point => [point.Latitude, point.Longitude]),
        { color: 'blue' }
      ).addTo(map.value)

      // Ajuster la vue de la carte pour englober tout le tracé
      map.value.fitBounds(polyline.getBounds())
    }
  } catch (error) {
    console.error('Erreur lors du chargement des données :', error)
  }
}

// Charger les données et initialiser la carte lorsque le composant est monté
onMounted(() => {
  loadData()

  // Initialiser la carte OpenStreetMap
  map.value = L.map('map').setView([48.8566, 2.3522], 13) // Coordonnées de départ (Paris)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map.value)
})
</script>

<template>
  <section class="bg-white dark:bg-gray-900 py-12 pt-28">
    <div class="max-w-screen-xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">
        Analyse des données de foulée et du parcours
      </h1>
      <p class="text-lg font-light text-gray-500 dark:text-gray-400 mb-16">
        Visualisez l'accélération des jambes, l'altitude et le tracé GPS pendant la course.
      </p>

      <!-- Graphique des foulées -->
      <div class="max-w-4xl mx-auto mb-12">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Accélération des jambes (Z)
        </h2>
        <div v-if="stepData.labels.length > 0" class="chart-container">
          <Line
            :data="stepData"
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
        <p v-else class="text-gray-500 dark:text-gray-400">
          Aucune donnée de foulée disponible.
        </p>
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
                y: { title: { display: true, text: 'Altitude (mètres)' } },
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
          Tracé GPS
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
