// import { createApp } from 'vue'
// import './style.css'
// import App from './App.vue'

// createApp(App).mount('#app')

import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

const app = createApp(App);

// Ajouter un état global pour la connexion
window.isAuthenticated = false;

app.use(router);
app.mount('#app');