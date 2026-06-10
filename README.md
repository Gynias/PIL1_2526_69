# IFRI_MentorLink - Projet Intégrateur (Statut : TERMINÉ ✅)

Application web de mentorat académique et professionnel pour les étudiants de l'IFRI.

Projet intégrateur 2025-2026 - Groupe 69  
Université d'Abomey-Calavi - Institut de Formation et de Recherche en Informatique

## Statut du Projet

Le projet a été mené à son terme avec succès. L'ensemble des fonctionnalités requises par le cahier des charges ont été implémentées, testées et validées (20 tests automatisés réussis à 100%). L'interface a été entièrement pensée avec un "Design System Pro Max" (Glassmorphism, animations fluides, Tailwind-like CSS) pour une expérience utilisateur premium.

## Fonctionnalités Réalisées

- **Authentification & Onboarding Dynamique** : Inscription sécurisée, et tunnel d'onboarding permettant à l'utilisateur de sélectionner ses points forts et ses lacunes depuis la base de données.
- **Profil Utilisateur & Paramètres** : Gestion complète du profil. Les étudiants peuvent modifier leurs compétences (forces/lacunes) a posteriori depuis les paramètres interactifs du compte.
- **Annonces & Recherche Paginée** : Page "Découvrir" dynamique avec filtres de recherche (matière, type, recherche libre) et pagination gérée par Django. L'interface s'adapte dynamiquement si aucune donnée n'est trouvée.
- **Matching Intelligent & Dashboard** : Algorithme de correspondance croisant les forces des uns avec les lacunes des autres. Fil d'actualité interactif (Offres / Demandes) géré en Javascript côté client.
- **Architecture de Base de Données Sécurisée** : Modèles relationnels (Utilisateurs, Compétences, Demandes/Offres) optimisés.

## Technologies Utilisées

- **Backend** : Python 3, Django 5
- **Frontend** : HTML5, CSS natif (Style Tailwind/Pro Max), Vanilla JavaScript
- **Base de données** : MySQL (MariaDB via XAMPP)

## Installation & Démarrage

### 1. Clonage et Environnement
```bash
git clone https://github.com/Gynias/PIL1_2526_69.git
cd PIL1_2526_69
python -m venv venv
# Windows : .\venv\Scripts\activate
```

### 2. Dépendances
```bash
pip install -r requirements.txt
```

### 3. Base de données
```sql
CREATE DATABASE mentorlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. Lancement
```bash
python manage.py makemigrations
python manage.py migrate
# Pour injecter la liste officielle des compétences :
python manage.py shell -c "from application_principale.models import Competence; Competence.objects.bulk_create([Competence(nom=n, categorie='Tech') for n in ['Python', 'Java', 'SQL', 'C++']])"
python manage.py runserver
```
Accès : `http://127.0.0.1:8000/`

## Contributions de l'Équipe

- **Chef de Projet** : Mise en place de la BDD, algorithme de matching, seeding des compétences.
- **Membre 2** : Module d'authentification et Onboarding interactif.
- **Membre 3** : Module de Profil & Modèles de Compétences.
- **Membre 4** : Module Annonces, pagination et filtres dynamiques (Page Découvrir).
- **Membre 5** : Tableau de bord dynamique et fil d'actualité JS.
- **Membre 6** : Paramètres du compte et modification a posteriori des compétences.

---
*Dépôt officiel du groupe : https://github.com/Gynias/PIL1_2526_69*
