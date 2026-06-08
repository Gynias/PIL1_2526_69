# Fiche de Mission : Membre 1
## Thème : Module Accueil, Gamification & Erreurs (Full-Stack)

Ton rôle est d'accueillir les nouveaux étudiants, de gérer la page d'erreur du site, et surtout de créer un système de Gamification ludique (Points et Badges) pour récompenser les meilleurs mentors.

### 🎨 Tes Maquettes (Dossier `maquettes/`)
- `onboarding_desktop` (Page de bienvenue / Accueil)
- `404_page` (Page d'erreur 404)
- *Gamification* : Pas de maquette précise, à toi de l'intégrer au tableau de bord ou au profil !

### 🛠️ Tes Missions :
1. **Créer ta branche** : `git checkout -b feature/accueil-gamification`
2. **Côté Frontend (HTML)** : Intégrer les maquettes `onboarding` et `404` dans le dossier `application_principale/templates/`. Créer un petit bloc HTML pour afficher les points et badges d'un mentor.
3. **Côté Backend (Python)** : 
   - Dans `application_principale/models.py`, ajouter des champs au modèle étudiant pour stocker ses "points" ou "badges".
   - Dans `application_principale/views.py`, écrire la logique qui ajoute des points à un étudiant quand il aide quelqu'un.
   - Gérer la vue de la page d'erreur 404 personnalisée.
4. **Soumission** : Faire un `git add`, `git commit` et `git push` pour envoyer ton travail.

---
## ⛔ INTERDICTIONS ABSOLUES ⛔
1. **NE CRÉEZ AUCUNE NOUVELLE APPLICATION**. Tout votre code Python (vues, urls, modèles) doit aller EXCLUSIVEMENT dans le dossier `application_principale`.
2. **NE MODIFIEZ JAMAIS `settings.py`**.
3. **NE CODEZ QUE VOTRE MODULE**. Ne touchez pas aux pages ou fonctionnalités assignées aux autres membres. En cas de chevauchement, coordonnez-vous avec l'équipe !
---
