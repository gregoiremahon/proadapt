<template>
    <div class="border p-4 rounded-lg shadow-lg bg-white">
      <img :src="component.image" alt="Image du composant" class="mb-4 rounded-lg w-full h-48 object-cover">
      <h2 class="text-xl font-semibold mb-2 text-gray-800">{{ component.name }}</h2>
      <p class="text-gray-600 mb-4">{{ component.description }}</p>
      <ul class="mb-4">
        <li v-for="spec in component.specs" :key="spec.label" class="text-gray-700">
          <strong>{{ spec.label }}:</strong> {{ spec.value }}
        </li>
      </ul>
      <a :href="component.link" target="_blank" class="text-blue-500 hover:underline">
        En savoir plus
      </a>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      component: {
        type: Object,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
  .border {
    border-color: #e5e7eb;
  }
  </style>