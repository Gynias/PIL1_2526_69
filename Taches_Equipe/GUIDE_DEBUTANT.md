# 🎓 Guide de Démarrage pour les Débutants du Groupe 69

Pas de panique ! Ce projet est structuré pour que tout soit le plus simple possible. Suivez ces étapes une par une, sans vous presser.

---

## Étape 1 : Récupérer le code sur votre ordinateur
1. Ouvrez votre terminal (ou Git Bash).
2. Tapez exactement cette commande pour télécharger le projet depuis GitHub :
   ```bash
   git clone https://github.com/Gynias/PIL1_2526_69.git
   ```
3. Entrez dans le dossier du projet :
   ```bash
   cd PIL1_2526_69
   ```

## Étape 2 : Préparer l'environnement Python
Pour ne pas mélanger ce projet avec d'autres choses sur votre ordinateur, on crée une "bulle" (environnement virtuel) :
1. Créez la bulle : 
   ```bash
   python -m venv venv
   ```
2. Activez la bulle (à faire **à chaque fois** que vous ouvrez votre terminal pour travailler) :
   - Sur Windows : `.\venv\Scripts\activate`
   - Sur Mac/Linux : `source venv/bin/activate`
3. Installez les outils du projet :
   ```bash
   pip install django pymysql
   ```

## Étape 3 : Travailler sur SA propre branche
**Règle d'or : On ne travaille jamais sur `principale` ni sur `developpement` !**
1. Regardez votre fiche de mission dans le dossier `Taches_Equipe` pour connaître le nom de votre branche.
2. Créez et allez sur votre branche (exemple pour le membre 2) :
   ```bash
   git checkout -b feature/authentification
   ```
   *(Remplacez `feature/authentification` par le nom écrit dans votre fiche).*

## Étape 4 : Comment coder ?
- **Pour le Backend (Membres 2 et 3)** : Vous allez écrire du code Python dans le fichier `application_principale/views.py`. Regardez des tutoriels sur "Django views" pour vous aider.
- **Pour le Frontend (Membres 4 et 5)** : Vous allez créer un dossier `templates` dans `application_principale`. Vous allez copier les fichiers `code.html` de vos maquettes dans ce dossier, et vous allez remplacer les faux textes par des balises Django (ex: `{{ utilisateur.nom }}`).

## Étape 5 : Sauvegarder et envoyer son travail
Quand vous avez fini de coder pour la journée :
1. Ajoutez vos modifications :
   ```bash
   git add .
   ```
2. Enregistrez-les avec un petit message expliquant ce que vous avez fait :
   ```bash
   git commit -m "J'ai fini la page de connexion"
   ```
3. Envoyez tout sur Internet (GitHub) :
   ```bash
   git push origin <nom-de-votre-branche>
   ```
   *(Exemple : `git push origin feature/authentification`)*

---
**En cas de doute ou de blocage, demandez au Chef de Projet ! C'est lui qui gère la base de données et l'algorithme.**
