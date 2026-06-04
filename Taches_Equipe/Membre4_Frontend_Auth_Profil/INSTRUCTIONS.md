# Fiche de Mission : Membre 4 (Frontend)
## Thème : Intégration Visuelle (Login, Inscription, Profil)

Bienvenue ! Ton rôle est d'intégrer les maquettes visuelles dans le moteur Django.
Le chef de projet a mis à ta disposition les fichiers HTML/CSS originaux dans le sous-dossier `maquettes/` juste à côté de ce fichier.

### Tes missions :
1. **Créer ta branche de travail** : `git checkout -b feature/integration-login` (à partir de `developpement`).
2. **Dossier Templates** : Crée un dossier `templates/` dans `application_principale/`.
3. **Intégration** : Prends les fichiers HTML du dossier `maquettes/` (`login_desktop`, `sign_up_desktop`, `my_profile`, etc.) et transforme-les en templates Django (avec les balises `{% extends 'base.html' %}`, `{% block content %}`, etc.).
4. **Formulaires** : Assure-toi que les balises `<form>` de tes pages HTML pointent vers les bonnes vues Backend (qui seront créées par le Membre 2) et incluent bien `{% csrf_token %}`.
5. **Soumission (Pull Request)** : Pousse ton code et fais une demande de fusion vers `developpement`.
