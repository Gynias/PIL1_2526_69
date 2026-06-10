from django.core.management.base import BaseCommand
from application_principale.models import Competence

class Command(BaseCommand):
    help = 'Ajoute les compétences et matières par défaut pour IFRI MentorLink'

    def handle(self, *args, **kwargs):
        competences_par_defaut = [
            # Programmation et Développement
            "Python", "Java", "C++", "C", "JavaScript", "PHP", "Ruby", "Swift", "Go",
            "Développement Web (HTML/CSS)", "React.js", "Angular", "Vue.js", "Django", "Spring Boot",
            "Développement Mobile (Android)", "Développement Mobile (iOS)", "Flutter", "React Native",
            
            # Bases de données et Data
            "SQL (MySQL/PostgreSQL)", "NoSQL (MongoDB)", "Data Science", "Machine Learning",
            "Intelligence Artificielle", "Big Data", "Analyse de Données", "Statistiques Appliquées",
            
            # Réseaux et Cybersécurité
            "Administration Réseaux", "Cybersécurité", "Cryptographie", "Sécurité des Systèmes",
            "Cloud Computing (AWS/Azure)", "Docker/Kubernetes", "Administration Linux",
            
            # Mathématiques et Informatique Théorique
            "Algorithmique", "Structures de Données", "Mathématiques Discrètes", "Algèbre Linéaire",
            "Analyse Mathématique", "Recherche Opérationnelle", "Théorie des Graphes",
            
            # Autres compétences académiques IFRI
            "Architecture des Ordinateurs", "Systèmes d'Exploitation", "Génie Logiciel",
            "Gestion de Projet Informatique", "Anglais Technique", "Communication Professionnelle"
        ]

        count_added = 0
        for nom in competences_par_defaut:
            comp, created = Competence.objects.get_or_create(nom=nom)
            if created:
                count_added += 1

        self.stdout.write(self.style.SUCCESS(f'Succès ! {count_added} nouvelles compétences ont été ajoutées à la base de données.'))
