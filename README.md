# Projet Intégrateur 2025-2026 : IFRI_MentorLink
**Groupe 69**

## 1. Présentation du Projet
IFRI_MentorLink est une plateforme institutionnelle visant à faciliter le mentorat académique et professionnel au sein de l'Institut de Formation et de Recherche en Informatique (IFRI). Cette application web connecte les étudiants souhaitant partager leurs compétences (mentors) avec ceux ayant besoin d'accompagnement (mentorés), via un système de mise en relation intelligent basé sur la compatibilité des profils.

## 2. Architecture Technique
- **Backend** : Framework Django (Python)
- **Base de données** : MySQL
- **Architecture de Branches (Git Flow)** :
  - `principale` : Code de production stable (évalué).
  - `developpement` : Branche d'intégration continue.
  - `fonctionnalite/*` : Branches de développement isolées.

## 3. Configuration de l'Environnement de Développement

### Prérequis
- Python 3.10 ou supérieur
- Un serveur MySQL (ex: XAMPP, WAMP, ou service natif)
- Git

### Initialisation
1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/Gynias/PIL1_2526_69.git
   cd PIL1_2526_69
   ```

2. **Création et activation de l'environnement virtuel**
   ```bash
   python -m venv venv
   # Sous Windows :
   .\venv\Scripts\activate
   # Sous Linux/Mac :
   source venv/bin/activate
   ```

3. **Installation des dépendances**
   ```bash
   pip install django pymysql
   ```

4. **Configuration de la Base de Données**
   - Assurez-vous que le service MySQL est démarré.
   - Créez une base de données nommée exactement `mentorlink_db`.
   - L'application utilise les identifiants par défaut (`root` sans mot de passe sur `127.0.0.1:3306`). Modifiez `projet_mentorlink/settings.py` si votre configuration locale diffère.

5. **Migrations et Lancement du Serveur**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```
   L'application sera disponible à l'adresse : `http://127.0.0.1:8000/`

## 4. Organisation de l'Équipe
- **Chef de Projet** : Architecture globale, conception de la base de données et algorithme de correspondance (matching).
- **Développeurs Backend** : Gestion des utilisateurs, offres/demandes, et API internes.
- **Développeurs Frontend** : Intégration des maquettes HTML/CSS fournies et liaisons avec le backend Django.

---
*Ce projet est réalisé dans le cadre de l'Unité d'Enseignement "Projet Intégrateur L1" de l'IFRI.*
