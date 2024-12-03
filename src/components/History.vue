<script setup>
import { ref, onMounted } from 'vue'

const userId = ref(localStorage.getItem('user_id'))
const courses = ref([])

const fetchCourses = async () => {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/courses?user_id=${userId.value}`)
    courses.value = await response.json()
  } catch (error) {
    console.error('Erreur lors de la récupération des courses:', error)
  }
}

onMounted(() => {
  fetchCourses()
})
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-3xl font-bold mb-8 text-center">Historique des Courses</h1>
    <ul>
      <li v-for="course in courses" :key="course.file_name" class="mb-4">
        <a :href="`/data/${course.file_name}`" target="_blank" class="text-blue-500 hover:underline">
          {{ course.file_name }}
        </a>
        <p class="text-gray-600">Uploaded at: {{ course.uploaded_at }}</p>
      </li>
    </ul>
  </div>
</template>
