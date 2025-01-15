<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuth } from '../auth'; // Importer le gestionnaire d'authentification

const { login } = useAuth(); // Utiliser la fonction login pour mettre à jour l'état global

// Variables pour stocker les informations de connexion
const email = ref('');
const password = ref('');
const name = ref('');
const isNewUser = ref(false);
const message = ref('');
const router = useRouter(); // Utilisation du router pour redirection

// Fonction utilitaire pour envoyer une requête HTTP
async function sendRequest(endpoint, payload) {
  console.log('Préparation de la requête pour :', endpoint, payload);
  try {
    const response = await fetch(`/api/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      message.value = errorData.error || 'Erreur inconnue.';
      console.error('Erreur retournée par le serveur :', errorData);
      return;
    }

    const data = await response.json();
    console.log('Réponse reçue :', data);
    message.value = data.message;

    if (endpoint === 'login') {
      // Stocker l'ID utilisateur (email) dans localStorage
      if (data.userId) {
        localStorage.setItem('user_id', data.userId);
        console.log('ID utilisateur enregistré dans localStorage:', data.userId);
      }

      login(); // Mettre à jour l'état global comme connecté
      router.push('/'); // Redirection vers la page d'accueil
    }
  } catch (error) {
    console.error('Erreur lors de la requête :', error);
    message.value = 'Erreur du serveur';
  }
}

// Fonction pour gérer la connexion
function handleLogin() {
  sendRequest('login', { email: email.value, password: password.value });
}

// Fonction pour gérer l'inscription
function handleSignUp() {
  sendRequest('signup', {
    email: email.value,
    password: password.value,
    name: name.value,
  }).then(() => {
    if (message.value === 'Inscription réussie.') {
      setTimeout(() => {
        router.push('/login');
      }, 2000);
    }
  });
}
</script>


<template>
  <section class="bg-gray-100 dark:bg-gray-900 flex items-center justify-center min-h-screen">
    <div class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8 max-w-md w-full">
      <h1 class="text-3xl font-extrabold text-gray-900 dark:text-white text-center mb-6">
        {{ isNewUser ? "Inscription" : "Connexion" }}
      </h1>
      
      <form @submit.prevent="isNewUser ? handleSignUp() : handleLogin()">
        <!-- Champ Nom (visible uniquement lors de l'inscription) -->
        <div v-if="isNewUser" class="mb-4">
          <label for="name" class="block text-gray-700 dark:text-gray-400 mb-1">Nom</label>
          <input
            v-model="name"
            type="text"
            id="name"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-600 dark:bg-gray-700 dark:text-white"
            required
          />
        </div>

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

        <!-- Message -->
        <p v-if="message" class="text-sm text-center text-red-500 mb-4">{{ message }}</p>

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
