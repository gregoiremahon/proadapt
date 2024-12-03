import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'

// Lire le port Flask depuis le fichier flask-port.txt
function getFlaskPort() {
  try {
    const port = fs.readFileSync('flask-port.txt', 'utf-8').trim()
    return parseInt(port, 10) || 5000 // Par défaut, retourne 5000 si le port n'est pas lisible
  } catch (err) {
    console.warn('Impossible de lire le fichier flask-port.txt, utilisation du port par défaut : 5000')
    return 5000
  }
}

// Plugin pour écrire le port Vite dans dev-port.txt
function writeDevPortPlugin() {
  return {
    name: 'write-dev-port', // Nom du plugin
    configureServer(server) {
      server.httpServer.on('listening', () => {
        const port = server.httpServer.address().port
        console.log(`Vite est en cours d'exécution sur le port ${port}`)
        fs.writeFileSync('dev-port.txt', String(port)) // Écrit le port dans dev-port.txt
      })
    },
  }
}

export default defineConfig({
  plugins: [
    vue(),
    writeDevPortPlugin(), // Plugin personnalisé pour capturer le port
  ],
  resolve: {
    alias: {
      '@': './', // Alias pour simplifier les chemins relatifs
    },
  },
  server: {
    host: '127.0.0.1', // Assure que Vue.js est accessible localement
    port: 5173,        // Port par défaut pour Vue.js
    strictPort: false, // Permet de changer de port si 5173 est occupé
    proxy: {
      '/api': {
        target: `http://127.0.0.1:${getFlaskPort()}`, // Lit dynamiquement le port Flask
        changeOrigin: true,
      },
    },
  },
})
