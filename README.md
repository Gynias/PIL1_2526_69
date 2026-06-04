# IFRI_MentorLink

Application web de mentorat académique et professionnel pour les étudiants de l'IFRI.

Projet intégrateur 2025-2026 - Groupe 69  
Université d'Abomey-Calavi - Institut de Formation et de Recherche en Informatique

## Objectif

IFRI_MentorLink met en relation les étudiants qui souhaitent offrir ou recevoir du mentorat. L'application permet de créer un profil, publier des offres ou demandes de mentorat, lancer un algorithme de matching et échanger via une plateforme intuitive.

## Fonctionnalités Principales

- **Authentification & Sécurité** : Inscription, connexion, et protection des données.
- **Profil Utilisateur** : Gestion des compétences, lacunes, filière et niveau d'études.
- **Annonces & Recherche** : Publication et exploration des offres et demandes de mentorat.
- **Matching Intelligent** : Algorithme de correspondance basé sur les compétences et les disponibilités.
- **Dashboard & Communication** : Tableau de bord personnel et messagerie intégrée.

## Technologies Utilisées

- **Backend** : Python, Django
- **Frontend** : HTML5, CSS3, JavaScript
- **Base de données** : MySQL

## Architecture du Projet

Le projet suit une architecture monolithique centralisée pour faciliter le travail collaboratif des étudiants :

```text
PIL1_2526_69/
├── application_principale/ # Coeur de l'application (Vues, Modèles, URLs)
│   ├── templates/          # Interfaces HTML de tous les membres
│   └── static/             # Fichiers CSS, JS et images
├── projet_mentorlink/      # Configuration globale Django
├── Taches_Equipe/          # Directives et guides internes de développement
└── requirements.txt        # Dépendances du projet
```

## Installation & Démarrage

### 1. Clonage et Environnement
```bash
git clone https://github.com/Gynias/PIL1_2526_69.git
cd PIL1_2526_69
python -m venv venv
```
*(Activation Windows : `.\venv\Scripts\activate` | Mac/Linux : `source venv/bin/activate`)*

### 2. Dépendances
```bash
pip install -r requirements.txt
```

### 3. Base de données
Assurez-vous que votre serveur MySQL (XAMPP/WAMP) est actif et exécutez :
```sql
CREATE DATABASE mentorlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
L'application se connecte par défaut avec l'utilisateur `root` (sans mot de passe) sur `127.0.0.1`.

### 4. Lancement
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Accès : `http://127.0.0.1:8000/`

## Organisation de l'Équipe (Full-Stack)
- **Chef de Projet** : Architecture globale, base de données, algorithme de matching, DevOps.
- **Membre 2** : Module Authentification (Onboarding, Connexion).
- **Membre 3** : Module Profil & Compétences.
- **Membre 4** : Module Annonces & Recherche.
- **Membre 5** : Module Dashboard & Messagerie.

---
*Dépôt officiel du groupe : https://github.com/Gynias/PIL1_2526_69*
