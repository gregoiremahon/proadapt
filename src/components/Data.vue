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
      average: 0,
    },
  ],
})

const calculateAverage = (data) => {
  if (data.length === 0) return 0;
  const sum = data.reduce((total, value) => total + value, 0);
  return (sum / data.length).toFixed(2); // Arrondi à 2 décimales
};

// Fonction pour calculer l'asymétrie
const calculateAsymmetry = (data) => {
  return data.map((item, index) => {
    const leftZ = Math.abs(item.Accel1Z || 0);
    const rightZ = Math.abs(item.Accel2Z || 0);
    if (leftZ + rightZ === 0){
      console.log("Division par zéro évitée");
      return 0; // Éviter la division par zéro
    }
    return (Math.abs(leftZ - rightZ) / (leftZ + rightZ)) * 100; // Asymétrie en %
  });
};

// Fonction pour calculer la cadence
const calculateCadence = (data) => {
  let peaks = 0;
  let lastTime = 0;

  const threshold = 5000; // Seuil pour détecter un impact (ajuster selon les données)
  const cadenceData = data.map((item, index) => {
    const zAccel = item.Accel1Z || 0; // Accélération verticale
    const time = item.Timer / 1000; // Temps en secondes
    if (Math.abs(zAccel) > threshold && time - lastTime > 0.2) {
      peaks += 1;
      lastTime = time;
    }
    return (peaks * 60) / (time || 1); // Cadence en pas par minute
  });

  return cadenceData;
};

// Calculer les données d'asymétrie et de cadence lors du chargement
const processAdditionalMetrics = (sensorData) => {
  const asymmetry = calculateAsymmetry(sensorData);
  const cadence = calculateCadence(sensorData);
  // Echantillonnage pour les graphiques d'asymétrie et de cadence (toutes les 5 secondes)
  const labels = sensorData.map((item) => (item.Timer / 1000).toFixed(2));

  // Appliquer l'échantillonnage
  const { sampledData, sampledLabels } = sampleAsymmetryData(asymmetry, labels, 5);
  
  asymmetryData.value = {
    labels: sampledLabels, // Labels échantillonnés
    datasets: [
      {
        label: 'Asymétrie (%)',
        data: sampledData, // Données échantillonnées
        backgroundColor: 'rgba(255, 159, 64, 1)', // Points pleins
        borderWidth: 0, // Pas de lignes
        pointRadius: 2, // Taille des points
        showLine: false, // Pas de connexion entre points
      },
    ],
  };
  
  cadenceData.value = {
    labels: sensorData.map((item) => (item.Timer / 1000).toFixed(2)),
    datasets: [
      {
        label: 'Cadence (pas par minute)',
        data: cadence,
        backgroundColor: 'rgba(255, 159, 64, 1)', // Points pleins
        borderWidth: 0, // Pas de lignes
        pointRadius: 2, // Taille des points
        showLine: false, // Pas de connexion entre points
      },
    ],
  };

  // Calculer et mettre à jour la moyenne de la cadence
  cadenceData.value.average = calculateAverage(cadence);
  console.log("Cadence moyenne calculée :", cadenceData.value.average);
};

// Fonction pour traiter les données d'accéléromètre
const processAccelerometerMetrics = (sensorData) => {
  const labels = sensorData.map((item) => (item.Timer / 1000).toFixed(2));

  // Échantillonnage pour chaque axe des jambes gauche et droite
  ['x', 'y', 'z'].forEach((axis) => {
    const leftData = sensorData.map((item) => item[`Accel1${axis.toUpperCase()}`] || 0);
    const rightData = sensorData.map((item) => item[`Accel2${axis.toUpperCase()}`] || 0);

    const leftSample = sampleAccelerometerData(leftData, labels, 5);
    const rightSample = sampleAccelerometerData(rightData, labels, 5);

    accelerometerData.value.leftLeg[axis] = leftSample.sampledData;
    accelerometerData.value.rightLeg[axis] = rightSample.sampledData;
    accelerometerData.value.labels = leftSample.sampledLabels; // Même labels pour les deux
  });
};


// Fonction pour échantillonner les données d'accéléromètre (moyenne sur un intervalle donné en secondes)
const sampleAccelerometerData = (data, labels, interval = 5) => {
  const sampledData = [];
  const sampledLabels = [];
  let tempSum = 0;
  let count = 0;

  labels.forEach((label, index) => {
    tempSum += data[index];
    count++;

    if (count >= interval || index === labels.length - 1) {
      sampledData.push(tempSum / count); // Moyenne des données
      sampledLabels.push(label); // Utiliser le label de fin de l'intervalle
      tempSum = 0;
      count = 0;
    }
  });

  return { sampledData, sampledLabels };
};

// Fonction pour échantillonner les données d'asymétrie (moyenne sur un intervalle donné en secondes)
const sampleAsymmetryData = (asymmetry, labels, interval = 5) => {
  const sampledData = [];
  const sampledLabels = [];
  let tempSum = 0;
  let count = 0;

  labels.forEach((label, index) => {
    tempSum += asymmetry[index];
    count++;

    if (count >= interval || index === labels.length - 1) {
      sampledData.push(tempSum / count); // Moyenne des asymétries
      sampledLabels.push(label); // Utiliser le label de fin de l'intervalle
      tempSum = 0;
      count = 0;
    }
  });

  return { sampledData, sampledLabels };
};

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
      processAccelerometerMetrics(sensorData); // Appliquer l'échantillonnage
      processAdditionalMetrics(sensorData); // Asymétrie et cadence
    }

    // Charger les données GPS
    const gpsTraceResponse = await fetchData(`${baseURL}/api/gps-trace`);
    const validTraceData = gpsTraceResponse.filter(
      (point) => point.Latitude && point.Longitude
    );

    if (validTraceData.length > 0) {
      const calculatedAltitudes = await calculateAltitude(validTraceData);
      gpsData.value.labels = calculatedAltitudes.map((item) => (item.Timer / 1000).toFixed(2));
      gpsData.value.datasets[0].data = calculatedAltitudes.map((item) => item.Altitude);
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
                  backgroundColor: 'rgba(75, 192, 192, 1)', // Couleur des points
                  borderWidth: 0, // Pas de bordure (pas de lignes)
                  pointRadius: 2, // Taille des points
                  showLine: false, // Pas de connexion entre points
                  data: accelerometerData.leftLeg[axis],
                },
                {
                  label: `Jambe droite (${axis.toUpperCase()})`,
                  backgroundColor: 'rgba(192, 75, 75, 1)', // Couleur des points
                  borderWidth: 0,
                  pointRadius: 2,
                  showLine: false,
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
              y: { 
                title: { display: true, text: 'Asymétrie (%)' },
                suggestedMin: 0, // Min à 0
                suggestedMax: 100, // Calcul du max dynamique (max ou 100) Math.max(...asymmetryData.value.datasets[0].data, 100)
              },
            },
          }"
          class="chart-container"
        />
      </div>

      <!-- Graphique de la cadence -->
      <div class="max-w-4xl mx-auto mb-12 chart-wrapper">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">Cadence (pas par minute) : (Moyenne : {{ cadenceData.average || '--' }} PPM)</h2>
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
