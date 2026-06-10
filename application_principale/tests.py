from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime, date, time
from application_principale.models import Utilisateur, DemandeOuOffre, Competence, CompetenceUtilisateur, Disponibilite, Matching, Conversation, Message

class MentorLinkViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Création d'un utilisateur de test
        self.user = Utilisateur.objects.create_user(
            email='test@ifri.bj',
            mot_de_passe='testpassword123',
            prenom='Jean',
            nom='Dupont',
            telephone='12345678',
            role='les_deux'
        )

        # Création d'une compétence
        self.competence = Competence.objects.create(
            nom='Intelligence Artificielle',
            categorie='Informatique'
        )

        # Création d'une annonce de test
        self.annonce = DemandeOuOffre.objects.create(
            auteur=self.user,
            type_publication='demande',
            competence=self.competence,
            format_seance='en_ligne',
            statut='ouvert'
        )

    def test_public_views(self):
        """Teste les pages accessibles sans être connecté."""
        response = self.client.get(reverse('accueil'))
        self.assertEqual(response.status_code, 200)

    def test_create_offer_request_post(self):
        """Teste la création d'une annonce via POST."""
        self.client.force_login(self.user)
        competence = Competence.objects.create(nom="Django")
        
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
            'competence': competence.id,
            'format_seance': 'en_ligne',
            'jour': 'lundi',
            'heure_debut': '10:00',
            'heure_fin': '12:00',
            'description': 'Je propose mon aide en Django.'
        })
        
        # Redirection vers le flux après succès
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DemandeOuOffre.objects.count(), 2)
        annonce = DemandeOuOffre.objects.order_by('-id').first()
        self.assertEqual(annonce.type_publication, 'offre')
        self.assertEqual(annonce.description, 'Je propose mon aide en Django.')

    def test_create_offer_request_invalid(self):
        """Teste la soumission invalide."""
        self.client.force_login(self.user)
        
        # Manque competence
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
        })
        
        # Reste sur la page avec erreur
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DemandeOuOffre.objects.count(), 1)

    def test_lancer_matching(self):
        """Teste l'algorithme de matching."""
        self.client.force_login(self.user)
        
        user2 = Utilisateur.objects.create_user(
            email='test2@example.com',
            mot_de_passe='password123',
            prenom='Jane',
            nom='Smith',
            role='mentor'
        )
        
        comp1 = Competence.objects.create(nom="Python")
        
        # Le User 1 (mentore) cherche Python
        CompetenceUtilisateur.objects.create(utilisateur=self.user, competence=comp1, type_competence='lacune')
        Disponibilite.objects.create(utilisateur=self.user, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        # Le User 2 (mentor) propose Python
        CompetenceUtilisateur.objects.create(utilisateur=user2, competence=comp1, type_competence='force')
        Disponibilite.objects.create(utilisateur=user2, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        response = self.client.get(reverse('lancer_matching'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('resultats', response.context)
        
        resultats = response.context['resultats']
        # Il devrait y avoir un match !
        self.assertTrue(len(resultats) > 0)
        matching = resultats[0]
        matched_user = matching.mentore if matching.mentor == self.user else matching.mentor
        score = matching.score_global
        self.assertEqual(matched_user, user2)
        self.assertTrue(score > 0)

        
        response = self.client.get(reverse('inscription'))
        self.assertEqual(response.status_code, 200)

    def test_create_offer_request_post(self):
        """Teste la création d'une annonce via POST."""
        self.client.force_login(self.user)
        competence = Competence.objects.create(nom="Django")
        
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
            'competence': competence.id,
            'format_seance': 'en_ligne',
            'jour': 'lundi',
            'heure_debut': '10:00',
            'heure_fin': '12:00',
            'description': 'Je propose mon aide en Django.'
        })
        
        # Redirection vers le flux après succès
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DemandeOuOffre.objects.count(), 2)
        annonce = DemandeOuOffre.objects.order_by('-id').first()
        self.assertEqual(annonce.type_publication, 'offre')
        self.assertEqual(annonce.description, 'Je propose mon aide en Django.')

    def test_create_offer_request_invalid(self):
        """Teste la soumission invalide."""
        self.client.force_login(self.user)
        
        # Manque competence
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
        })
        
        # Reste sur la page avec erreur
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DemandeOuOffre.objects.count(), 1)

    def test_lancer_matching(self):
        """Teste l'algorithme de matching."""
        self.client.force_login(self.user)
        
        user2 = Utilisateur.objects.create_user(
            email='test2@example.com',
            mot_de_passe='password123',
            prenom='Jane',
            nom='Smith',
            role='mentor'
        )
        
        comp1 = Competence.objects.create(nom="Python")
        
        # Le User 1 (mentore) cherche Python
        CompetenceUtilisateur.objects.create(utilisateur=self.user, competence=comp1, type_competence='lacune')
        Disponibilite.objects.create(utilisateur=self.user, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        # Le User 2 (mentor) propose Python
        CompetenceUtilisateur.objects.create(utilisateur=user2, competence=comp1, type_competence='force')
        Disponibilite.objects.create(utilisateur=user2, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        response = self.client.get(reverse('lancer_matching'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('resultats', response.context)
        
        resultats = response.context['resultats']
        # Il devrait y avoir un match !
        self.assertTrue(len(resultats) > 0)
        matching = resultats[0]
        matched_user = matching.mentore if matching.mentor == self.user else matching.mentor
        score = matching.score_global
        self.assertEqual(matched_user, user2)
        self.assertTrue(score > 0)


        response = self.client.get(reverse('connexion'))
        self.assertEqual(response.status_code, 200)

    def test_create_offer_request_post(self):
        """Teste la création d'une annonce via POST."""
        self.client.force_login(self.user)
        competence = Competence.objects.create(nom="Django")
        
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
            'competence': competence.id,
            'format_seance': 'en_ligne',
            'jour': 'lundi',
            'heure_debut': '10:00',
            'heure_fin': '12:00',
            'description': 'Je propose mon aide en Django.'
        })
        
        # Redirection vers le flux après succès
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DemandeOuOffre.objects.count(), 2)
        annonce = DemandeOuOffre.objects.order_by('-id').first()
        self.assertEqual(annonce.type_publication, 'offre')
        self.assertEqual(annonce.description, 'Je propose mon aide en Django.')

    def test_create_offer_request_invalid(self):
        """Teste la soumission invalide."""
        self.client.force_login(self.user)
        
        # Manque competence
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
        })
        
        # Reste sur la page avec erreur
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DemandeOuOffre.objects.count(), 1)

    def test_lancer_matching(self):
        """Teste l'algorithme de matching."""
        self.client.force_login(self.user)
        
        user2 = Utilisateur.objects.create_user(
            email='test2@example.com',
            mot_de_passe='password123',
            prenom='Jane',
            nom='Smith',
            role='mentor'
        )
        
        comp1 = Competence.objects.create(nom="Python")
        
        # Le User 1 (mentore) cherche Python
        CompetenceUtilisateur.objects.create(utilisateur=self.user, competence=comp1, type_competence='lacune')
        Disponibilite.objects.create(utilisateur=self.user, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        # Le User 2 (mentor) propose Python
        CompetenceUtilisateur.objects.create(utilisateur=user2, competence=comp1, type_competence='force')
        Disponibilite.objects.create(utilisateur=user2, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        response = self.client.get(reverse('lancer_matching'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('resultats', response.context)
        
        resultats = response.context['resultats']
        # Il devrait y avoir un match !
        self.assertTrue(len(resultats) > 0)
        matching = resultats[0]
        matched_user = matching.mentore if matching.mentor == self.user else matching.mentor
        score = matching.score_global
        self.assertEqual(matched_user, user2)
        self.assertTrue(score > 0)


    def test_protected_views_unauthenticated(self):
        """Vérifie que les pages privées redirigent vers la connexion."""
        protected_urls = [
            'tableau_de_bord',
            'create_offer_request',
            'discover_page',
            'offer_request_feed',
            'account_settings',
            'security_settings',
            'liste_conversations'
        ]
        for url_name in protected_urls:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith(reverse('connexion')))

    def test_protected_views_authenticated(self):
        """Teste le rendu des pages principales avec un utilisateur connecté."""
        self.client.login(email='test@ifri.bj', password='testpassword123')
        
        urls_to_test = [
            'tableau_de_bord',
            'create_offer_request',
            'discover_page',
            'offer_request_feed',
            'account_settings',
            'security_settings',
            'liste_conversations'
        ]
        
        for url_name in urls_to_test:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200, f"Erreur sur l'URL {url_name}")

    def test_dynamic_views_authenticated(self):
        """Teste les pages nécessitant des IDs (Annonce)."""
        self.client.login(email='test@ifri.bj', password='testpassword123')
        
        response = self.client.get(reverse('offer_request_detail', args=[self.annonce.id]))
        self.assertEqual(response.status_code, 200)

    def test_create_offer_request_post(self):
        """Teste la création d'une annonce via POST."""
        self.client.force_login(self.user)
        competence = Competence.objects.create(nom="Django")
        
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
            'competence': competence.id,
            'format_seance': 'en_ligne',
            'jour': 'lundi',
            'heure_debut': '10:00',
            'heure_fin': '12:00',
            'description': 'Je propose mon aide en Django.'
        })
        
        # Redirection vers le flux après succès
        self.assertEqual(response.status_code, 302)
        self.assertEqual(DemandeOuOffre.objects.count(), 2)
        annonce = DemandeOuOffre.objects.order_by('-id').first()
        self.assertEqual(annonce.type_publication, 'offre')
        self.assertEqual(annonce.description, 'Je propose mon aide en Django.')

    def test_create_offer_request_invalid(self):
        """Teste la soumission invalide."""
        self.client.force_login(self.user)
        
        # Manque competence
        response = self.client.post(reverse('create_offer_request'), {
            'type_publication': 'offre',
        })
        
        # Reste sur la page avec erreur
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DemandeOuOffre.objects.count(), 1)

    def test_lancer_matching(self):
        """Teste l'algorithme de matching."""
        self.client.force_login(self.user)
        
        user2 = Utilisateur.objects.create_user(
            email='test2@example.com',
            mot_de_passe='password123',
            prenom='Jane',
            nom='Smith',
            role='mentor'
        )
        
        comp1 = Competence.objects.create(nom="Python")
        
        # Le User 1 (mentore) cherche Python
        CompetenceUtilisateur.objects.create(utilisateur=self.user, competence=comp1, type_competence='lacune')
        Disponibilite.objects.create(utilisateur=self.user, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        # Le User 2 (mentor) propose Python
        CompetenceUtilisateur.objects.create(utilisateur=user2, competence=comp1, type_competence='force')
        Disponibilite.objects.create(utilisateur=user2, jour='lundi', heure_debut='10:00', heure_fin='12:00')
        
        response = self.client.get(reverse('lancer_matching'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('resultats', response.context)
        
        resultats = response.context['resultats']
        # Il devrait y avoir un match !
        self.assertTrue(len(resultats) > 0)
        matching = resultats[0]
        matched_user = matching.mentore if matching.mentor == self.user else matching.mentor
        score = matching.score_global
        self.assertEqual(matched_user, user2)
        self.assertTrue(score > 0)



    def test_connexion_view(self):
        response = self.client.post(reverse('connexion'), {'email': 'test@ifri.bj', 'mot_de_passe': 'testpassword123'})
        self.assertEqual(response.status_code, 302) # Redirect to tableau_de_bord
        
    def test_connexion_view_invalid(self):
        response = self.client.post(reverse('connexion'), {'email': 'test@ifri.bj', 'mot_de_passe': 'wrong'})
        self.assertEqual(response.status_code, 200)

    def test_inscription_view(self):
        response = self.client.post(reverse('inscription'), {
            'prenom': 'Alice',
            'nom': 'Wonderland',
            'email': 'alice@ifri.bj',
            'telephone': '00000000',
            'mot_de_passe': 'password123',
            'confirmer_mot_de_passe': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Utilisateur.objects.filter(email='alice@ifri.bj').exists())

    def test_offer_request_detail(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('offer_request_detail', args=[self.annonce.id]))
        self.assertEqual(response.status_code, 200)
        
    def test_search_results(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('search_results'), {'q': 'Intelligence'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('annonces', response.context)

    def test_accepter_matching(self):
        self.client.force_login(self.user)
        matching = Matching.objects.create(mentor=self.user, mentore=self.user, score_global=90, statut='en_attente')
        response = self.client.post(reverse('accepter_matching', args=[matching.id]))
        self.assertEqual(response.status_code, 302)
        matching.refresh_from_db()
        self.assertEqual(matching.statut, 'accepte')

    def test_refuser_matching(self):
        self.client.force_login(self.user)
        matching = Matching.objects.create(mentor=self.user, mentore=self.user, score_global=90, statut='en_attente')
        response = self.client.post(reverse('refuser_matching', args=[matching.id]))
        self.assertEqual(response.status_code, 302)
        matching.refresh_from_db()
        self.assertEqual(matching.statut, 'refuse')

    def test_liste_conversations(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('liste_conversations'))
        self.assertEqual(response.status_code, 200)

    def test_demarrer_conversation(self):
        self.client.force_login(self.user)
        user2 = Utilisateur.objects.create_user(email='bob@example.com', mot_de_passe='pass')
        response = self.client.post(reverse('demarrer_conversation', args=[user2.id]))
        self.assertEqual(response.status_code, 302)

    def test_envoyer_message(self):
        self.client.force_login(self.user)
        user2 = Utilisateur.objects.create_user(email='bob2@example.com', mot_de_passe='pass')
        from application_principale.models import Conversation
        conv = Conversation.objects.create(utilisateur1=self.user, utilisateur2=user2)
        response = self.client.post(reverse('envoyer_message', args=[conv.id]), {'contenu': 'Hello Bob'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(conversation=conv).exists())

    def test_account_settings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('account_settings'))
        self.assertEqual(response.status_code, 200)

    def test_security_settings(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('security_settings'))
        self.assertEqual(response.status_code, 200)

    def test_onboarding_post_inscription(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('onboarding'))
        self.assertEqual(response.status_code, 200)
