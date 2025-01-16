// vite.config.js
import { defineConfig } from "file:///Users/jonathan/Library/Mobile%20Documents/com~apple~CloudDocs/projet-long-4/PRGM/ProAdapt/src/proadapt/src/node_modules/vite/dist/node/index.js";
import vue from "file:///Users/jonathan/Library/Mobile%20Documents/com~apple~CloudDocs/projet-long-4/PRGM/ProAdapt/src/proadapt/src/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import fs from "fs";
function getFlaskPort() {
  try {
    const port = fs.readFileSync("flask-port.txt", "utf-8").trim();
    return parseInt(port, 10) || 5e3;
  } catch (err) {
    console.warn("Impossible de lire le fichier flask-port.txt, utilisation du port par d\xE9faut : 5000");
    return 5e3;
  }
}
function writeDevPortPlugin() {
  return {
    name: "write-dev-port",
    // Nom du plugin
    configureServer(server) {
      server.httpServer.on("listening", () => {
        const port = server.httpServer.address().port;
        console.log(`Vite est en cours d'ex\xE9cution sur le port ${port}`);
        fs.writeFileSync("dev-port.txt", String(port));
      });
    }
  };
}
var vite_config_default = defineConfig({
  plugins: [
    vue(),
    writeDevPortPlugin()
    // Plugin personnalisé pour capturer le port
  ],
  resolve: {
    alias: {
      "@": "./"
      // Alias pour simplifier les chemins relatifs
    }
  },
  server: {
    host: "127.0.0.1",
    // Assure que Vue.js est accessible localement
    port: 5173,
    // Port par défaut pour Vue.js
    strictPort: false,
    // Permet de changer de port si 5173 est occupé
    proxy: {
      "/api": {
        target: `http://127.0.0.1:${getFlaskPort()}`,
        // Lit dynamiquement le port Flask
        changeOrigin: true
      }
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcuanMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVXNlcnMvam9uYXRoYW4vTGlicmFyeS9Nb2JpbGUgRG9jdW1lbnRzL2NvbX5hcHBsZX5DbG91ZERvY3MvcHJvamV0LWxvbmctNC9QUkdNL1Byb0FkYXB0L3NyYy9wcm9hZGFwdC9zcmNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZmlsZW5hbWUgPSBcIi9Vc2Vycy9qb25hdGhhbi9MaWJyYXJ5L01vYmlsZSBEb2N1bWVudHMvY29tfmFwcGxlfkNsb3VkRG9jcy9wcm9qZXQtbG9uZy00L1BSR00vUHJvQWRhcHQvc3JjL3Byb2FkYXB0L3NyYy92aXRlLmNvbmZpZy5qc1wiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9pbXBvcnRfbWV0YV91cmwgPSBcImZpbGU6Ly8vVXNlcnMvam9uYXRoYW4vTGlicmFyeS9Nb2JpbGUlMjBEb2N1bWVudHMvY29tfmFwcGxlfkNsb3VkRG9jcy9wcm9qZXQtbG9uZy00L1BSR00vUHJvQWRhcHQvc3JjL3Byb2FkYXB0L3NyYy92aXRlLmNvbmZpZy5qc1wiO2ltcG9ydCB7IGRlZmluZUNvbmZpZyB9IGZyb20gJ3ZpdGUnXG5pbXBvcnQgdnVlIGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZSdcbmltcG9ydCBmcyBmcm9tICdmcydcblxuLy8gTGlyZSBsZSBwb3J0IEZsYXNrIGRlcHVpcyBsZSBmaWNoaWVyIGZsYXNrLXBvcnQudHh0XG5mdW5jdGlvbiBnZXRGbGFza1BvcnQoKSB7XG4gIHRyeSB7XG4gICAgY29uc3QgcG9ydCA9IGZzLnJlYWRGaWxlU3luYygnZmxhc2stcG9ydC50eHQnLCAndXRmLTgnKS50cmltKClcbiAgICByZXR1cm4gcGFyc2VJbnQocG9ydCwgMTApIHx8IDUwMDAgLy8gUGFyIGRcdTAwRTlmYXV0LCByZXRvdXJuZSA1MDAwIHNpIGxlIHBvcnQgbidlc3QgcGFzIGxpc2libGVcbiAgfSBjYXRjaCAoZXJyKSB7XG4gICAgY29uc29sZS53YXJuKCdJbXBvc3NpYmxlIGRlIGxpcmUgbGUgZmljaGllciBmbGFzay1wb3J0LnR4dCwgdXRpbGlzYXRpb24gZHUgcG9ydCBwYXIgZFx1MDBFOWZhdXQgOiA1MDAwJylcbiAgICByZXR1cm4gNTAwMFxuICB9XG59XG5cbi8vIFBsdWdpbiBwb3VyIFx1MDBFOWNyaXJlIGxlIHBvcnQgVml0ZSBkYW5zIGRldi1wb3J0LnR4dFxuZnVuY3Rpb24gd3JpdGVEZXZQb3J0UGx1Z2luKCkge1xuICByZXR1cm4ge1xuICAgIG5hbWU6ICd3cml0ZS1kZXYtcG9ydCcsIC8vIE5vbSBkdSBwbHVnaW5cbiAgICBjb25maWd1cmVTZXJ2ZXIoc2VydmVyKSB7XG4gICAgICBzZXJ2ZXIuaHR0cFNlcnZlci5vbignbGlzdGVuaW5nJywgKCkgPT4ge1xuICAgICAgICBjb25zdCBwb3J0ID0gc2VydmVyLmh0dHBTZXJ2ZXIuYWRkcmVzcygpLnBvcnRcbiAgICAgICAgY29uc29sZS5sb2coYFZpdGUgZXN0IGVuIGNvdXJzIGQnZXhcdTAwRTljdXRpb24gc3VyIGxlIHBvcnQgJHtwb3J0fWApXG4gICAgICAgIGZzLndyaXRlRmlsZVN5bmMoJ2Rldi1wb3J0LnR4dCcsIFN0cmluZyhwb3J0KSkgLy8gXHUwMEM5Y3JpdCBsZSBwb3J0IGRhbnMgZGV2LXBvcnQudHh0XG4gICAgICB9KVxuICAgIH0sXG4gIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgZGVmaW5lQ29uZmlnKHtcbiAgcGx1Z2luczogW1xuICAgIHZ1ZSgpLFxuICAgIHdyaXRlRGV2UG9ydFBsdWdpbigpLCAvLyBQbHVnaW4gcGVyc29ubmFsaXNcdTAwRTkgcG91ciBjYXB0dXJlciBsZSBwb3J0XG4gIF0sXG4gIHJlc29sdmU6IHtcbiAgICBhbGlhczoge1xuICAgICAgJ0AnOiAnLi8nLCAvLyBBbGlhcyBwb3VyIHNpbXBsaWZpZXIgbGVzIGNoZW1pbnMgcmVsYXRpZnNcbiAgICB9LFxuICB9LFxuICBzZXJ2ZXI6IHtcbiAgICBob3N0OiAnMTI3LjAuMC4xJywgLy8gQXNzdXJlIHF1ZSBWdWUuanMgZXN0IGFjY2Vzc2libGUgbG9jYWxlbWVudFxuICAgIHBvcnQ6IDUxNzMsICAgICAgICAvLyBQb3J0IHBhciBkXHUwMEU5ZmF1dCBwb3VyIFZ1ZS5qc1xuICAgIHN0cmljdFBvcnQ6IGZhbHNlLCAvLyBQZXJtZXQgZGUgY2hhbmdlciBkZSBwb3J0IHNpIDUxNzMgZXN0IG9jY3VwXHUwMEU5XG4gICAgcHJveHk6IHtcbiAgICAgICcvYXBpJzoge1xuICAgICAgICB0YXJnZXQ6IGBodHRwOi8vMTI3LjAuMC4xOiR7Z2V0Rmxhc2tQb3J0KCl9YCwgLy8gTGl0IGR5bmFtaXF1ZW1lbnQgbGUgcG9ydCBGbGFza1xuICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICB9LFxuICAgIH0sXG4gIH0sXG59KVxuIl0sCiAgIm1hcHBpbmdzIjogIjtBQUErZSxTQUFTLG9CQUFvQjtBQUM1Z0IsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sUUFBUTtBQUdmLFNBQVMsZUFBZTtBQUN0QixNQUFJO0FBQ0YsVUFBTSxPQUFPLEdBQUcsYUFBYSxrQkFBa0IsT0FBTyxFQUFFLEtBQUs7QUFDN0QsV0FBTyxTQUFTLE1BQU0sRUFBRSxLQUFLO0FBQUEsRUFDL0IsU0FBUyxLQUFLO0FBQ1osWUFBUSxLQUFLLHdGQUFxRjtBQUNsRyxXQUFPO0FBQUEsRUFDVDtBQUNGO0FBR0EsU0FBUyxxQkFBcUI7QUFDNUIsU0FBTztBQUFBLElBQ0wsTUFBTTtBQUFBO0FBQUEsSUFDTixnQkFBZ0IsUUFBUTtBQUN0QixhQUFPLFdBQVcsR0FBRyxhQUFhLE1BQU07QUFDdEMsY0FBTSxPQUFPLE9BQU8sV0FBVyxRQUFRLEVBQUU7QUFDekMsZ0JBQVEsSUFBSSxnREFBNkMsSUFBSSxFQUFFO0FBQy9ELFdBQUcsY0FBYyxnQkFBZ0IsT0FBTyxJQUFJLENBQUM7QUFBQSxNQUMvQyxDQUFDO0FBQUEsSUFDSDtBQUFBLEVBQ0Y7QUFDRjtBQUVBLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVM7QUFBQSxJQUNQLElBQUk7QUFBQSxJQUNKLG1CQUFtQjtBQUFBO0FBQUEsRUFDckI7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLE9BQU87QUFBQSxNQUNMLEtBQUs7QUFBQTtBQUFBLElBQ1A7QUFBQSxFQUNGO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUE7QUFBQSxJQUNOLE1BQU07QUFBQTtBQUFBLElBQ04sWUFBWTtBQUFBO0FBQUEsSUFDWixPQUFPO0FBQUEsTUFDTCxRQUFRO0FBQUEsUUFDTixRQUFRLG9CQUFvQixhQUFhLENBQUM7QUFBQTtBQUFBLFFBQzFDLGNBQWM7QUFBQSxNQUNoQjtBQUFBLElBQ0Y7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
