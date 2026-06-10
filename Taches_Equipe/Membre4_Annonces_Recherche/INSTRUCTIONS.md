# Rapport de Réalisation : Membre 4
## Thème : Module Annonces et Recherche (Découvrir)

### Statut : Validé ✅

### Travaux accomplis :
1. **Création d'Annonces** : J'ai développé la logique de `create_offer_request.html` pour que les utilisateurs puissent publier une offre liée à une compétence spécifique de la base de données.
2. **Page Découvrir Dynamique** : J'ai transformé la page de recherche statique en un vrai moteur dynamique.
   - Les formulaires de filtres envoient désormais des requêtes `GET`.
   - La vue `discover_page` filtre en SQL les résultats en fonction de la matière, du type et du texte saisi.
3. **Pagination** : J'ai implémenté le module Paginator de Django (avec `order_by('-id')`) pour gérer l'affichage page par page sans surcharger le serveur.
