<script setup>
import { ref, onMounted } from 'vue';

// Simuler l'ID utilisateur
const userId = ref(localStorage.getItem('user_id') || 'test_user');

// Simuler des données de test brutes
const courses = ref([]);
const error = ref(''); // Gérer les erreurs lors de la récupération des données

const fetchCourses = async () => {
  try {
    // Données de test brutes
    courses.value = [
      {
        file_name: 'course1.csv',
        uploaded_at: '2024-12-01T10:00:00Z',
      },
      {
        file_name: 'course2.csv',
        uploaded_at: '2024-12-02T12:30:00Z',
      },
      {
        file_name: 'course3.csv',
        uploaded_at: '2024-12-03T15:45:00Z',
      },
    ];
  } catch (err) {
    console.error('Erreur lors de la récupération des courses:', err);
    error.value = 'Impossible de récupérer les données. Veuillez réessayer plus tard.';
  }
};

onMounted(() => {
  fetchCourses();
});
</script>

<template>
  <div class="container mx-auto bg-white dark:bg-gray-900 py-12 pt-28">
    <h1 class="text-center text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">
      Historique des Courses
    </h1>

    <!-- Message d'erreur -->
    <div v-if="error" class="text-center text-red-500 bg-red-100 p-4 rounded-md">
      {{ error }}
    </div>

    <!-- Liste des courses -->
    <div v-else-if="courses.length > 0">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="course in courses"
          :key="course.file_name"
          class="bg-white shadow-lg rounded-lg p-6 dark:bg-gray-800 dark:text-white"
        >
          <h2 class="text-lg font-semibold mb-2 truncate text-purple-700 dark:text-purple-400">
            {{ course.file_name }}
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Ajouté le : {{ new Date(course.uploaded_at).toLocaleDateString() }}
          </p>
          <a
            :href="`/data/${course.file_name}`"
            target="_blank"
            class="inline-block bg-purple-600 text-white text-sm font-medium py-2 px-4 rounded-lg hover:bg-purple-700 dark:hover:bg-purple-500"
          >
            Télécharger
          </a>
        </div>
      </div>
    </div>

    <!-- Message si aucune course disponible -->
    <div v-else class="text-center text-gray-600 dark:text-gray-400 mt-10">
      Aucune course disponible. Veuillez synchroniser vos données pour afficher votre historique.
    </div>
  </div>
</template>
