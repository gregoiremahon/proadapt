<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)

const teamMembers = [
  {
    "name": "Jonathan QUEYROI",
    "role": "Ingénieur en Informatique",
    "description": "Responsable de la conception des interfaces utilisateur et de l'expérience globale, Jonathan garantit une application intuitive et esthétique tout en optimisant les fonctionnalités pour les utilisateurs.",
    "imageUrl": "../assets/Photo-Profil/Jonathan.jpg"
  },
  {
    "name": "Sylvain PLAZE",
    "role": "Chef de projet et Ingénieur en Electronique",
    "description": "Expert en programmation bas niveau et en électronique industrielle, Sylvain dirige le projet avec une vision claire et assure le bon fonctionnement des composants électroniques.",
    "imageUrl": "../assets/Photo-Profil/Sylvain.jpg"
  },
  {
    "name": "Grégoire MAHON",
    "role": "Ingénieur en Informatique",
    "description": "Responsable de l'intégration logicielle et matérielle, Grégoire se concentre sur la connectivité des capteurs et le développement des algorithmes d'analyse de données.",
    "imageUrl": "../assets/Photo-Profil/Gregoire.jpg"
  },
  {
    "name": "Mohamed Zaidi",
    "role": "Ingénieur en Conception 3D",
    "description": "Mohamed conçoit les modèles 3D du kit, en veillant à leur ergonomie et leur durabilité pour répondre aux besoins des utilisateurs finaux.",
    "imageUrl": "../assets/Photo-Profil/Ashraf.jpg"
  },
  {
    "name": "Chahine BOUKHENAISSI",
    "role": "Ingénieur en Electronique",
    "description": "Spécialiste des systèmes embarqués, Chahine est en charge de la conception et de l'optimisation des circuits électroniques de ProAdapt.",
    "imageUrl": "../assets/Photo-Profil/Chahine.jpg"
  },
  {
    "name": "Armand LELONG",
    "role": "Gestionnaire Commercial",
    "description": "Armand supervise les relations avec les partenaires et assure la viabilité financière du projet grâce à une stratégie commerciale efficace.",
    "imageUrl": "../assets/Photo-Profil/Armand.jpg"
  }
];

</script>

<template>
  <section class="bg-white dark:bg-gray-900 py-12 pt-28">
    <div class="max-w-screen-xl mx-auto text-center">
      <h1 class="text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">
        À propos de notre équipe
      </h1>
      <p class="text-lg font-light text-gray-500 dark:text-gray-400 mb-16">
        Nous sommes une équipe d'étudiants en dernière année à l'école d'ingénieurs de Polytech Sorbonne, passionnés par le sport, et plus particulièrement la course à pied. Le projet ProAdapt est né de notre volonté d'aider des coureurs de haut niveau amputés d'une jambe. Nous avons constaté qu'il existait peu de solutions pour les soutenir dans l'optimisation de leurs foulées. ProAdapt a été conçu pour leur permettre d'améliorer leur performance en recréant une foulée aussi proche que possible de celle d'une jambe naturelle.
      </p>
      
      <div class="grid gap-10 lg:grid-cols-3 md:grid-cols-2">
        <div v-for="member in teamMembers" :key="member.name" class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
          <img :src="member.imageUrl" :alt="member.name" class="member-image rounded-full mx-auto mb-4">
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white">{{ member.name }}</h2>
          <h3 class="text-lg text-purple-600 dark:text-purple-500 mb-4">{{ member.role }}</h3>
          <p class="text-gray-500 dark:text-gray-400">{{ member.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Pour garantir que les images ne soient pas déformées */
.member-image {
  width: 96px;
  height: 96px;
  object-fit: cover;  /* Cette propriété permet de recadrer l'image tout en conservant les proportions */
  border-radius: 50%;  /* Pour assurer que l'image reste ronde */
}
</style>
