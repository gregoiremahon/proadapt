<script setup>
import { ref } from 'vue'

// Variables pour stocker les informations de connexion
const email = ref('')
const password = ref('')
const isNewUser = ref(false)

// Fonction pour gérer la connexion
function handleLogin() {
  console.log('Connexion avec', email.value, password.value)
  // Ajouter la logique de connexion ici
}

// Fonction pour gérer l'inscription
function handleSignUp() {
  console.log('Inscription avec', email.value, password.value)
  // Ajouter la logique d'inscription ici
}
</script>

<template>
  <section class="bg-gray-100 dark:bg-gray-900 flex items-center justify-center min-h-screen">
    <div class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8 max-w-md w-full">
      <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white text-center mb-6">
        {{ isNewUser ? "Inscription" : "Connexion" }}
      </h1>
      
      <form @submit.prevent="isNewUser ? handleSignUp() : handleLogin()">
        <!-- Champ Email -->
        <div class="mb-4">
          <label for="email" class="block text-gray-700 dark:text-gray-400 mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 dark:bg-gray-700 dark:text-white"
            required
          />
        </div>

        <!-- Champ Mot de Passe -->
        <div class="mb-4">
          <label for="password" class="block text-gray-700 dark:text-gray-400 mb-1">Mot de passe</label>
          <input
            v-model="password"
            type="password"
            id="password"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 dark:bg-gray-700 dark:text-white"
            required
          />
        </div>

        <!-- Bouton de Connexion ou d'Inscription -->
        <button
          type="submit"
          class="w-full bg-purple-700 hover:bg-purple-800 text-white font-bold py-2 px-4 rounded-lg focus:outline-none focus:ring-4 focus:ring-purple-300 dark:focus:ring-purple-800"
        >
          {{ isNewUser ? "S'inscrire" : "Se connecter" }}
        </button>
      </form>

      <!-- Lien pour changer de mode -->
      <div class="mt-6 text-center">
        <p class="text-gray-600 dark:text-gray-400">
          {{ isNewUser ? "Déjà un compte ?" : "Pas encore de compte ?" }}
          <a
            href="#"
            @click.prevent="isNewUser = !isNewUser"
            class="text-purple-700 hover:underline dark:text-purple-500"
          >
            {{ isNewUser ? "Connectez-vous" : "Inscrivez-vous" }}
          </a>
        </p>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Styles supplémentaires pour la page de connexion */
</style>
