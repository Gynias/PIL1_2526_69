# IFRI MentorLink

Bienvenue sur **IFRI MentorLink**, la plateforme dédiée à la mise en relation entre étudiants (Mentors et Mentorés) de l'IFRI pour favoriser l'entraide, le partage de connaissances et l'excellence académique.

---

## 🎯 Aperçu du Projet

Le projet a pour but de créer un espace centralisé où les étudiants peuvent :
- **S'inscrire** en tant que Mentor, Mentoré, ou les deux.
- **Déclarer leurs compétences** (Points forts) et leurs besoins (Lacunes).
- **Découvrir des profils compatibles** grâce à un algorithme de "Matching" qui calcule un score de compatibilité.
- **Publier et consulter des annonces** (offres d'aide ou demandes d'accompagnement).
- **Discuter en temps réel** via un système de messagerie interne fluide.

---

## 🏗️ Architecture du Projet

L'application repose sur une architecture robuste et standardisée :

- **Backend** : Python avec le framework **Django** (Architecture MVT - Model View Template).
- **Base de Données** : **SQLite** (par défaut, idéale pour le développement et les tests locaux).
- **Frontend** : HTML5, CSS3 (utilisant des classes utilitaires inspirées de Tailwind pour un design moderne "Glassmorphism") et **JavaScript Vanilla** (pour les interactions en temps réel et le rafraîchissement des messages).
- **Communication Temps Réel** : Système de *Long Polling* (requêtes asynchrones JavaScript régulières) pour actualiser les conversations sans recharger la page.

### Structure des dossiers principaux
```text
IFRI_MentorLink/
│
├── application_principale/      # Application Django principale (Logique métier)
│   ├── models.py                # Modèles de base de données (Utilisateurs, Messages, Annonces...)
│   ├── views.py                 # Logique applicative et gestion des requêtes
│   ├── urls.py                  # Routage des URLs
│   └── templates/               # Fichiers HTML / Interface utilisateur
│
├── pil_project/                 # Configuration globale du projet Django (settings.py, urls.py globaux)
├── manage.py                    # Script utilitaire Django
└── requirements.txt             # (Optionnel) Liste des dépendances Python
```

---

## 🚀 Guide d'Installation et de Démarrage Rapide

Ce guide est conçu pour vous permettre de lancer le projet **sans aucune erreur** du premier coup. L'application est configurée pour fonctionner "Out of the box".

### 1. Prérequis
- Avoir **Python 3.10+** d'installé. (Assurez-vous que la commande `python` ou `python3` est accessible dans votre terminal).
- Utiliser un terminal (PowerShell sous Windows ou Terminal sous Linux/Mac).

### 2. Télécharger et préparer le projet
Ouvrez votre terminal et placez-vous dans le dossier du projet :
```bash
cd IFRI_MentorLink  # Ou le nom du dossier où vous avez extrait le projet
```

### 3. Créer et activer l'environnement virtuel (Obligatoire)
L'environnement virtuel garantit que les bibliothèques n'entrent pas en conflit avec votre système.
**Sous Windows (PowerShell) :**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**Sous MacOS / Linux :**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances
Nous avons préparé un fichier `requirements.txt` avec toutes les bibliothèques requises (Django, Pillow pour les images, etc.).
```bash
pip install -r requirements.txt
```

### 5. Préparer la Base de Données (SQLite)
Nous utilisons SQLite pour faciliter les tests (pas de serveur externe requis). Créez la base de données locale avec :
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. (Optionnel) Créer un administrateur
Pour accéder au panneau d'administration (`/admin/`), créez un super-utilisateur :
```bash
python manage.py createsuperuser
```
*(Suivez les instructions à l'écran pour l'email et le mot de passe)*

### 7. Lancer le serveur local
```bash
python manage.py runserver
```
Le projet est maintenant 100% fonctionnel et accessible sur : **http://127.0.0.1:8000/**

---

## 🧪 Guide de Test (Comment essayer l'application ?)

Pour tester toutes les fonctionnalités, l'idéal est de **simuler deux utilisateurs différents**. Vous pouvez le faire en ouvrant deux navigateurs différents (par exemple Chrome et Firefox) ou en utilisant une fenêtre de navigation privée.

### Étape 1 : Inscription et Onboarding
1. Allez sur `http://127.0.0.1:8000/register/`.
2. Créez un compte pour le **Testeur A** (choisissez le rôle "Mentor").
3. Lors de l'étape d'onboarding, sélectionnez ses **Points forts** (matières qu'il maîtrise) et ses disponibilités.
4. Dans un autre navigateur, créez un compte pour le **Testeur B** (choisissez le rôle "Mentoré").
5. Dans l'onboarding, sélectionnez ses **Lacunes** (matières où il a besoin d'aide).

### Étape 2 : Le Matching
1. Connectez-vous avec le **Testeur B**.
2. Allez sur la page de **Matching** via le menu principal.
3. Le système devrait vous proposer le profil du **Testeur A** avec un pourcentage de compatibilité élevé (puisque les points forts de A correspondent aux lacunes de B).

### Étape 3 : La Messagerie
1. Depuis la page de Matching ou le Profil public, cliquez sur **"Contacter"**.
2. Une conversation s'ouvre. Envoyez un message (ex: *"Bonjour, j'ai besoin d'aide en programmation !"*).
3. Basculez sur le navigateur du **Testeur A**, allez dans l'onglet **Messagerie**. Vous verrez le message apparaître.
4. Répondez avec A. Le message apparaîtra **instantanément** chez B sans avoir besoin de rafraîchir la page !

### Étape 4 : Les Annonces (Fil d'actualité)
1. Allez dans l'onglet **Créer une Annonce** (bouton "+" ou menu "Annonces").
2. Créez une offre (ex: "Je donne des cours de Python le mardi").
3. Allez dans l'onglet **Explorer (Feed)** pour voir votre annonce s'afficher dans le fil public. Tout le monde peut la consulter et vous contacter depuis cette page.

---

## ⚙️ Technologies et Choix Techniques

- **Tailwind CSS (via CDN ou classes équivalentes)** : Pour un design rapide, responsive et moderne (effets Glassmorphism, variables CSS pour le mode clair/sombre).
- **Google Material Symbols** : Utilisé pour les icônes vectorielles nettes et personnalisables.
- **Flexbox & CSS Grid** : Pour des mises en page (Layouts) fluides, que ce soit sur mobile ou sur écran large.
- **Sécurité Django** : Protection native contre les failles CSRF (Cross-Site Request Forgery), XSS, et injection SQL. Mots de passe hashés par défaut.

---
*Projet développé pour l'IFRI. Pour toute question technique, n'hésitez pas à consulter le code source.*
