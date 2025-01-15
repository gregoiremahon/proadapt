<script>
import ComponentCard from "./ComponentCard.vue";

export default {
  components: { ComponentCard },
  data() {
    return {
      components: [
        {
          name: "Batterie LiPo 4000 mAh",
          description: "Fournit une autonomie de 8 heures d'entraînement continu.",
          specs: [
            { label: "Capacité", value: "4000 mAh" },
            { label: "Autonomie", value: "8 heures en usage continu, 24 heures en veille" }
          ],
          image: "../assets/components/battery.jpg", // Image pour la batterie
          link: "https://www.gotronic.fr/art-accu-lipo-3-7-vcc-4000-mah-l805080-31843.htm"
        },
        {
          name: "ESP32",
          description: "Module pour connexion Bluetooth et Wi-Fi, permettant la transmission en temps réel des données.",
          specs: [
            { label: "Connexion", value: "Bluetooth & Wi-Fi" },
            { label: "Dimensions", value: "48 x 26 x 11.5 mm" }
          ],
          image: "../assets/components/esp32.jpg", // Image pour l'ESP32
          link: "https://www.gotronic.fr/art-module-nodemcu-esp32-28407.htm"
        },
        {
          name: "Capteur GPS GOKU GM10 Nano V3",
          description: "Permet le suivi de la position et de la vitesse en extérieur.",
          specs: [
            { label: "Précision", value: "Haute précision" },
            { label: "Dimensions", value: "12 x 17 x 4.5 mm" }
          ],
          image: "../assets/components/gps.jpg", // Image pour le GPS
          link: "https://www.drone-fpv-racer.com/gps-goku-gm10-nano-v3-flywoo-10844.html"
        },
        {
          name: "Capteur de Flexion",
          description: "Mesure les angles de flexion pour analyser la dynamique du mouvement.",
          specs: [
            { label: "Longueur", value: "112 mm" },
            { label: "Placement", value: "Articulations de la prothèse" }
          ],
          image: "../assets/components/flexion-sensor.jpg", // Image pour le capteur de flexion
          link: "https://www.gotronic.fr/art-capteur-de-flexion-112-mm-fs2l095-30853.htm"
        },
        {
          name: "Module MPU-6050",
          description: "Capteur 6 DOF pour mesurer l'orientation et l'accélération.",
          specs: [
            { label: "Dimensions", value: "25 x 20 x 7 mm" },
            { label: "Fonctions", value: "Accéléromètre & Gyroscope" }
          ],
          image: "../assets/components/mpu6050.jpg", // Image pour le MPU-6050
          link: "https://www.gotronic.fr/art-module-6-dof-sen-mpu6050-31492.htm"
        },
        {
          name: "Connecteur Magnétique",
          description: "Recharge rapide et sécurisée du boîtier principal.",
          specs: [
            { label: "Type", value: "Magnétique" },
            { label: "Compatibilité", value: "Recharge de la batterie principale" }
          ],
          image: "../assets/components/magnetic-connector.jpg", // Image pour le connecteur magnétique
          link: "https://www.gotronic.fr/art-connecteur-magnetique-4-cts-ada5358-35225.htm"
        }
      ]
    };
  }
};
</script>

<template>
    <div class="container mx-auto bg-white dark:bg-gray-900 py-12 pt-28">
      <h1 class="text-center text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">Caractéristiques Techniques de ProAdapt</h1>

        <div class="introduction mb-8">
            <p>
                ProAdapt est un système innovant conçu pour aider les athlètes amputés à améliorer leurs performances de course 
                et à prévenir les blessures. Ce kit de capteurs permet une analyse en temps réel de la dynamique de course, 
                de la pression exercée, et d'autres paramètres critiques grâce à une combinaison de technologies avancées. 
                Le système est modulable et adaptable à toutes les prothèses de jambe, avec une autonomie et une durabilité 
                optimisées pour des sessions d'entraînement intensives.
            </p>
        </div>

    <!-- Key Features Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 text-center mb-10">
      <div class="feature-card">
        <img src="../assets/icons/icon-battery.svg" alt="Battery Icon" class="mx-auto mb-2" />
        <h2 class="text-xl font-semibold">Autonomie de 8 heures</h2>
        <p class="text-gray-600">Jusqu'à 8 heures d'entraînement en continu</p>
      </div>
      <div class="feature-card">
        <img src="../assets/icons/icon-precision.svg" alt="Precision Icon" class="mx-auto mb-2" />
        <h2 class="text-xl font-semibold">Précision GPS</h2>
        <p class="text-gray-600">Positionnement de haute précision en extérieur</p>
      </div>
      <div class="feature-card">
        <img src="../assets/icons/icon-connectivity.svg" alt="Connectivity Icon" class="mx-auto mb-2" />
        <h2 class="text-xl font-semibold">Bluetooth & Wi-Fi</h2>
        <p class="text-gray-600">Connectivité facile pour une analyse en temps réel</p>
      </div>
      <div class="feature-card">
        <img src="../assets/icons/icon-durability.svg" alt="Durability Icon" class="mx-auto mb-2" />
        <h2 class="text-xl font-semibold">Design Résistant</h2>
        <p class="text-gray-600">Boîtier étanche et robuste certifié IP67</p>
      </div>
    </div>

    <!-- Component Details Section -->
    <h2 class="text-2xl font-semibold mt-10 mb-4 text-center">Composants Principaux</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <ComponentCard
        v-for="component in components"
        :key="component.name"
        :component="component"
      />
    </div>

    <!-- Additional Information -->
    <div class="additional-info mt-10">
      <h2 class="text-2xl font-semibold mb-4">Autonomie et Durabilité</h2>
      <p class="text-gray-600 mb-6">
        ProAdapt est optimisé pour offrir une autonomie de 8 heures en usage continu, idéal pour des sessions d'entraînement prolongées. 
        Son boîtier robuste, certifié IP67, assure une protection contre la poussière et l'eau, garantissant une utilisation sécurisée dans des environnements sportifs variés.
      </p>

      <h2 class="text-2xl font-semibold mb-4">Ergonomie et Conception</h2>
      <p class="text-gray-600 mb-6">
        Conçu pour s'adapter parfaitement aux prothèses, le boîtier principal est compact et léger (250g), ce qui facilite son transport et sa fixation sur l'athlète. 
        Le boîtier dispose d'un bouton multifonction intuitif, permettant de contrôler facilement l'enregistrement des données et la connexion Bluetooth.
      </p>

      <h2 class="text-2xl font-semibold mb-4">Fonctions Avancées de Mesure</h2>
      <p class="text-gray-600 mb-6">
        ProAdapt est équipé de capteurs de flexion pour analyser les angles de mouvement, d'un module MPU-6050 pour mesurer l'accélération et l'orientation, 
        ainsi que d'un capteur GPS haute précision. Ces données sont transmises en temps réel à une application dédiée via Bluetooth, offrant aux athlètes et aux professionnels de santé un feedback immédiat et exploitable.
      </p>

      <h2 class="text-2xl font-semibold mb-4">Système de Recharge et Connectivité</h2>
      <p class="text-gray-600">
        Le boîtier intègre une connexion magnétique pour une recharge rapide et facile, avec une autonomie en veille allant jusqu'à 24 heures. 
        De plus, le système de connectivité via Bluetooth et Wi-Fi permet une flexibilité d'utilisation selon les conditions et les besoins.
      </p>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
}
.feature-card {
  background-color: #f9fafb;
  border-radius: 0.5rem;
  padding: 1.5rem;
}
.feature-card h2 {
  color: #6b46c1; /* Purple shade */
}
.feature-card img {
  width: 40px;
  height: 40px;
}
.additional-info {
  font-size: 1.125rem;
  line-height: 1.75rem;
  color: #4a5568; /* Dark gray */
}
</style>
