<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

Chart.register(...registerables)

// Vérification et récupération de l'utilisateur connecté
const userId = localStorage.getItem("user_id");
if (!userId) {
  console.error("Aucun ID utilisateur trouvé. Veuillez vous connecter.");
}

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

// Références pour les graphiques
const speedData = ref({
  labels: [], // Temps (secondes)
  datasets: [
    {
      label: 'Vitesse (km/h)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
  ],
})

const paceData = ref({
  labels: [],
  datasets: [
    {
      label: 'Allure (min/km)',
      backgroundColor: 'rgba(192, 75, 75, 0.2)',
      borderColor: 'rgba(192, 75, 75, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
  ],
})

const asymmetryData = ref({
  labels: [],
  datasets: [
    {
      label: 'Asymétrie (%)',
      backgroundColor: 'rgba(255, 159, 64, 0.2)',
      borderColor: 'rgba(255, 159, 64, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
  ],
})

const cadenceData = ref({
  labels: [],
  datasets: [
    {
      label: 'Cadence (pas par minute)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 2,
      pointRadius: 2,
      data: [],
    },
  ],
})

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

// Fonction pour convertir des degrés en radians
function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}

// Fonction pour calculer la distance entre deux points GPS (formule de Haversine)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371e3; // Rayon de la Terre en mètres
  const φ1 = toRadians(lat1);
  const φ2 = toRadians(lat2);
  const Δφ = toRadians(lat2 - lat1);
  const Δλ = toRadians(lon2 - lon1);

  const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
            Math.cos(φ1) * Math.cos(φ2) *
            Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c; // Distance en mètres
}

// Fonction pour calculer la vitesse à partir des données GPS
function calculateSpeed(sensorData) {
  let speedArray = [];

  for (let i = 1; i < sensorData.length; i++) {
    const prevPoint = sensorData[i - 1];
    const currentPoint = sensorData[i];

    const distance = calculateDistance(
      prevPoint.Latitude, prevPoint.Longitude,
      currentPoint.Latitude, currentPoint.Longitude
    );

    const timeDiff = (currentPoint.Timer - prevPoint.Timer) / 1000; // Temps en secondes

    const speed = timeDiff > 0 ? (distance / timeDiff) : 0; // Vitesse en m/s
    speedArray.push((speed * 3.6).toFixed(2)); // Convertir en km/h
  }

  // Ajouter une vitesse nulle pour le premier point
  speedArray.unshift(0);
  return speedArray;
}


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

      const labels = sensorData.map((item) => (item.Timer / 1000).toFixed(2))

      paceData.value.labels = labels
      asymmetryData.value.labels = labels

      paceData.value.datasets[0].data = sensorData.map((item) => {
        const kmh = item.Vitesse ? item.Vitesse * 3.6 : 0
        return kmh > 0 ? (60 / kmh).toFixed(2) : 0 // min/km
      })

      asymmetryData.value.datasets[0].data = sensorData.map((item) => {
        const leftLeg = Math.abs(item.Accel1X || 0)
        const rightLeg = Math.abs(item.Accel2X || 0)
        return ((Math.abs(leftLeg - rightLeg) / ((leftLeg + rightLeg) / 2)) * 100).toFixed(2)
      })

      // Calcul de la cadence
      const zLeftLeg = sensorData.map((item) => item.Accel1Z || 0) // Axe Z pour la jambe gauche
      const zRightLeg = sensorData.map((item) => item.Accel2Z || 0) // Axe Z pour la jambe droite
      const peaks = detectPeaks(zLeftLeg, zRightLeg)

      cadenceData.value.labels = labels
      cadenceData.value.datasets[0].data = peaks.map((count) => count * 60) // Cadence en pas par minute
      console.log("Pics détectés :", detectPeaks(zLeftLeg, zRightLeg));
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

function detectPeaks(zLeftLeg, zRightLeg) {
  const threshold = 8000; // Ajusté pour une sensibilité correcte
  let peakCounts = [];
  let count = 0;

  // Parcours des données pour détecter les pics
  for (let i = 1; i < zLeftLeg.length - 1; i++) {
    if (
      (zLeftLeg[i] > threshold && zLeftLeg[i] > zLeftLeg[i - 1] && zLeftLeg[i] > zLeftLeg[i + 1]) || 
      (zRightLeg[i] > threshold && zRightLeg[i] > zRightLeg[i - 1] && zRightLeg[i] > zRightLeg[i + 1])
    ) {
      count++;
    }

    // Ajout de la cadence toutes les 5 secondes
    if (i % 100 === 0) {
      peakCounts.push(count);
      count = 0;
    }
  }

  return peakCounts;
}


// Fonction pour enregistrer la course
const saveCourse = async () => {
  const flaskPort = 5173;  // Changez ce port si besoin
  const baseURL = `http://127.0.0.1:${flaskPort}`;
  
  const courseData = {
    userId,  // Envoi de l'email comme identifiant
    file_name: `course_${new Date().toISOString().replace(/[:.-]/g, "_")}.csv`,
    uploaded_at: new Date().toISOString(),
  };

  console.log("Données envoyées :", courseData);  // Ajout du log pour vérifier les données

  try {
    const response = await fetch(`${baseURL}/api/save-course`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(courseData),
    });

    const result = await response.json();
    if (response.ok) {
      alert('Course enregistrée avec succès !');
    } else {
      console.error('Erreur lors de l’enregistrement de la course :', result.error);
    }
  } catch (error) {
    console.error('Erreur lors de l’enregistrement de la course :', error);
  }
};

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

      <!-- Graphique de la vitesse -->
      <div class="max-w-4xl mx-auto mb-12 chart-wrapper">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Vitesse (km/h)</h2>
        <Line
          :data="speedData"
          :options="{
            responsive: true,
            maintainAspectRatio: true, // Maintient un ratio fixe
            scales: {
              x: { title: { display: true, text: 'Temps (secondes)' } },
              y: { title: { display: true, text: 'Vitesse (km/h)' }, min: 0 },
            },
          }"
          class="chart-container"
        />
      </div>

      <!-- Graphique de l'allure -->
      <div class="max-w-4xl mx-auto mb-12 chart-wrapper">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Allure (min/km)</h2>
        <Line
          :data="paceData"
          :options="{
            responsive: true,
            maintainAspectRatio: true, // Maintient un ratio fixe
            scales: {
              x: { title: { display: true, text: 'Temps (secondes)' } },
              y: { title: { display: true, text: 'Allure (min/km)' }, min: 0 },
            },
          }"
          class="chart-container"
        />
      </div>

      <!-- Graphique de l'asymétrie -->
      <div class="max-w-4xl mx-auto mb-12 chart-wrapper">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Asymétrie (%)</h2>
        <Line
          :data="asymmetryData"
          :options="{
            responsive: true,
            maintainAspectRatio: true, // Maintient un ratio fixe
            scales: {
              x: { title: { display: true, text: 'Temps (secondes)' } },
              y: { title: { display: true, text: 'Asymétrie (%)' }, min: 0, max: 100 },
            },
          }"
          class="chart-container"
        />
      </div>

      <!-- Graphique de la cadence -->
      <div class="max-w-4xl mx-auto mb-12 chart-wrapper">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Cadence (pas par minute)</h2>
        <Line
          :data="cadenceData"
          :options="{
            responsive: true,
            maintainAspectRatio: true,
            scales: {
              x: { title: { display: true, text: 'Temps (secondes)' } },
              y: { title: { display: true, text: 'Cadence (pas/min)' }, min: 0, max: 200 },
            },
          }"
          class="chart-container"
        />
      </div>

      <button
        @click="loadData"
        class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 mt-8"
      >
        Recharger les données
      </button>

      <!-- Bouton pour enregistrer la course -->
      <button
        @click="saveCourse"
        class="text-white bg-green-600 hover:bg-green-700 focus:ring-4 focus:ring-green-300 font-medium rounded-lg text-sm px-4 py-2 mt-8"
      >
        Enregistrer la course
      </button>
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
