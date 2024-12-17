// auth.js
import { ref } from 'vue';

const isAuthenticated = ref(false); // État réactif global pour la connexion

function login() {
  isAuthenticated.value = true; // Marque l'utilisateur comme connecté
}

function logout() {
  isAuthenticated.value = false; // Marque l'utilisateur comme déconnecté
}

export function useAuth() {
  return {
    isAuthenticated,
    login,
    logout,
  };
}
