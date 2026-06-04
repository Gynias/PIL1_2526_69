# Fiche de Mission : Membre 5
## Thème : Tableau de bord et Messagerie (Full-Stack)

Ton rôle est crucial : tu gères la page d'accueil de l'utilisateur (Dashboard) où il verra les correspondances trouvées par l'algorithme, ainsi que le système de messagerie interne.

### 🎨 Tes Maquettes (Dossier `maquettes/`)
- `dashboard_desktop` (Tableau de bord principal)
- `matching_page` (Page affichant les meilleurs mentors/mentorés)
- `conversations_list_desktop` (Liste des messages)
- `open_conversation_desktop` (Chat)
- `notifications`

### 🛠️ Tes Missions :
1. **Créer ta branche** : `git checkout -b feature/dashboard-messagerie`
2. **Côté Frontend (HTML)** : Intégrer tes maquettes dans le dossier `application_principale/templates/`.
3. **Côté Backend (Python)** : Dans `views.py`, écrire la vue d'accueil qui appellera la fonction `generer_correspondances` (l'algo du chef de projet). Créer aussi la logique pour envoyer et lire un `Message`.
4. **Soumission** : Faire un `git add`, `git commit` et `git push` pour envoyer ton travail.
