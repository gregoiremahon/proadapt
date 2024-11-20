<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)

const teamMembers = [
  {
    name: "Jonathan QUEYROI",
    role: "Directeur Commercial",
    description: "Expert en gestion commerciale avec un œil stratégique sur l'optimisation de la performance de ProAdapt.",
    imageUrl: "/src/assets/Photo-profil/Jonathan.jpg"
  },
  {
    name: "Sylvain PLAZE",
    role: "Ingénieure en Mécanique",
    description: "Spécialiste en conception et développement de solutions mécaniques pour optimiser les performances des athlètes.",
    imageUrl: "/src/assets/Photo-profil/Sylvain.jpg"
  },
  {
    name: "Grégoire MAHON",
    role: "Ingénieur Électronique",
    description: "Responsable de l'intégration des capteurs et du développement de la connectivité du projet ProAdapt.",
    imageUrl: "/src/assets/Photo-profil/Gregoire.jpg"
  },
  {
    name: "Mohamed Zaidi",
    role: "Ingénieure Biomédicale",
    description: "Experte en analyse biomédicale, Sophie s'assure que les solutions ProAdapt respectent les normes de santé et sécurité.",
    imageUrl: "/src/assets/Photo-profil/Ashraf.jpg"
  },
  {
    name: "Chahine BOUKHENAISSI",
    role: "Ingénieur en Informatique",
    description: "Développeur principal de l'application ProAdapt, garantissant une expérience utilisateur fluide et performante.",
    imageUrl: "/src/assets/Photo-profil/Chahine.jpg"
  },
  {
    name: "Armand LELONG",
    role: "Designer UX/UI",
    description: "Lucie conçoit l'interface utilisateur pour que l'expérience de ProAdapt soit aussi agréable qu'efficace.",
    imageUrl: "/src/assets/Photo-profil/armand.jpg"
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
