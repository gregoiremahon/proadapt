<template>
    <div class="container mx-auto bg-white dark:bg-gray-900 py-12 pt-28">
      <h1 class="text-center text-4xl font-extrabold leading-none tracking-tight text-gray-900 dark:text-white mb-8">Guide d'Utilisation de ProAdapt</h1>
  
      <!-- Section: Setup Instructions -->
      <section class="mb-10">
        <h2 class="text-2xl font-semibold mb-4 text-purple-700">Configuration Initiale</h2>
        <p class="text-gray-700 mb-6">
          Suivez ces étapes pour configurer ProAdapt avant votre premier entraînement.
        </p>
        <ul class="list-disc pl-6 text-gray-600 space-y-2">
          <li>
            <strong>Charge :</strong> Utilisez le connecteur magnétique pour charger la batterie du boîtier principal. Placez le boîtier dans son emplacement pour un chargement sans friction.
          </li>
          <li>
            <strong>Connexion :</strong> Assurez-vous que les capteurs sont bien placés sur la prothèse. Activez le Bluetooth pour permettre la synchronisation avec l'application.
          </li>
        </ul>
      </section>
  
      <!-- Section: Using the Application -->
      <section class="mb-10">
        <h2 class="text-2xl font-semibold mb-4 text-purple-700">Utilisation de l'Application</h2>
        <p class="text-gray-700 mb-6">
          L'application ProAdapt offre des fonctionnalités avancées pour les athlètes et les médecins.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- For Athletes -->
          <div class="bg-gray-50 rounded-lg p-4 shadow">
            <h3 class="text-xl font-semibold mb-2 text-purple-700">Pour les Athlètes</h3>
            <ul class="list-disc pl-6 text-gray-600 space-y-2">
              <li>
                <strong>Visualisation des Données :</strong> Affichez vos performances sous forme de graphiques et d'indicateurs.
              </li>
              <li>
                <strong>Partage :</strong> Partagez vos données avec vos proches ou la communauté en respectant les options de confidentialité.
              </li>
              <li>
                <strong>Conseils Personnalisés :</strong> Recevez des recommandations pour améliorer vos performances et prévenir les blessures.
              </li>
            </ul>
          </div>
          
          <!-- For Medical Professionals -->
          <div class="bg-gray-50 rounded-lg p-4 shadow">
            <h3 class="text-xl font-semibold mb-2 text-purple-700">Pour les Médecins</h3>
            <ul class="list-disc pl-6 text-gray-600 space-y-2">
              <li>
                <strong>Accès aux Données :</strong> Visualisez les données de vos patients et suivez leurs progrès.
              </li>
              <li>
                <strong>Annotation :</strong> Ajoutez des annotations sur les tendances et les problèmes observés.
              </li>
              <li>
                <strong>Propositions d'Amélioration :</strong> Suggérez des ajustements pour la prothèse ou la technique de course.
              </li>
            </ul>
          </div>
        </div>
      </section>
  
      <!-- Section: Maintenance and Care -->
      <section class="mb-10">
        <h2 class="text-2xl font-semibold mb-4 text-purple-700">Entretien et Maintenance</h2>
        <p class="text-gray-700 mb-6">
          Suivez ces recommandations pour garantir la longévité et la fiabilité de votre kit ProAdapt.
        </p>
        <ul class="list-disc pl-6 text-gray-600 space-y-2">
          <li>
            <strong>Nettoyage :</strong> Nettoyez les capteurs et le boîtier avec un chiffon doux après chaque utilisation.
          </li>
          <li>
            <strong>Stockage :</strong> Rangez le kit dans son étui de protection pour éviter les dommages dus aux chocs ou à la poussière.
          </li>
          <li>
            <strong>Vérification :</strong> Inspectez régulièrement les capteurs pour s'assurer qu'ils sont correctement fixés.
          </li>
        </ul>
      </section>
  
      <!-- Additional Information -->
      <section class="additional-info mt-10">
        <h2 class="text-2xl font-semibold mb-4 text-purple-700">Informations Complémentaires</h2>
        <p class="text-gray-700">
          Pour plus de détails, veuillez consulter le manuel utilisateur complet ou contactez notre support technique.
        </p>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    name: "UserGuide"
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
  }
  h2 {
    color: #6b46c1; /* Matching purple for headings */
  }
  p, ul {
    font-size: 1.125rem; /* Text size for readability */
  }
  ul {
    line-height: 1.6;
  }
  </style>
  