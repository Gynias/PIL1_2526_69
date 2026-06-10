import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_mentorlink.settings')
django.setup()

from application_principale.models import Utilisateur, Competence, CompetenceUtilisateur, DemandeOuOffre, Conversation, Message, Matching, Notification

print('--- DEBUT DES TESTS AVANCES ---')

# 1. Clean up potential old test users
Utilisateur.objects.filter(email__contains='@test-advanced.com').delete()
Competence.objects.filter(nom__startswith='TEST_COMP_').delete()

# 2. Setup Data
print('Creation de 5 utilisateurs et competences...')
c1 = Competence.objects.create(nom='TEST_COMP_Python')
c2 = Competence.objects.create(nom='TEST_COMP_React')
c3 = Competence.objects.create(nom='TEST_COMP_Maths')

u1 = Utilisateur.objects.create_user(email='u1@test-advanced.com', prenom='Alice', nom='Mentor', mot_de_passe='pass', role='mentor', telephone='999000001')
u2 = Utilisateur.objects.create_user(email='u2@test-advanced.com', prenom='Bob', nom='Mentee', mot_de_passe='pass', role='mentore', telephone='999000002')
u3 = Utilisateur.objects.create_user(email='u3@test-advanced.com', prenom='Charlie', nom='Both', mot_de_passe='pass', role='les_deux', telephone='999000003')
u4 = Utilisateur.objects.create_user(email='u4@test-advanced.com', prenom='Diana', nom='Mentor', mot_de_passe='pass', role='mentor', telephone='999000004')
u5 = Utilisateur.objects.create_user(email='u5@test-advanced.com', prenom='Eve', nom='Mentee', mot_de_passe='pass', role='mentore', telephone='999000005')

# Assign skills (Forces and Lacunes)
CompetenceUtilisateur.objects.create(utilisateur=u1, competence=c1, type_competence='force')
CompetenceUtilisateur.objects.create(utilisateur=u2, competence=c1, type_competence='lacune')

CompetenceUtilisateur.objects.create(utilisateur=u4, competence=c2, type_competence='force')
CompetenceUtilisateur.objects.create(utilisateur=u4, competence=c3, type_competence='force')
CompetenceUtilisateur.objects.create(utilisateur=u5, competence=c2, type_competence='lacune')
CompetenceUtilisateur.objects.create(utilisateur=u3, competence=c3, type_competence='lacune')
CompetenceUtilisateur.objects.create(utilisateur=u3, competence=c1, type_competence='force')

print('Utilisateurs crees avec succes.')

# 3. Test Matching Logic
print('Test de la logique de matching pour u2...')
mentors_potentiels = Utilisateur.objects.filter(role__in=['mentor', 'les_deux']).exclude(id=u2.id)
lacunes_u2 = set(CompetenceUtilisateur.objects.filter(utilisateur=u2, type_competence='lacune').values_list('competence', flat=True))

scores = []
for mentor in mentors_potentiels:
    forces_mentor = set(CompetenceUtilisateur.objects.filter(utilisateur=mentor, type_competence='force').values_list('competence', flat=True))
    common_skills = lacunes_u2.intersection(forces_mentor)
    if common_skills:
        score = (len(common_skills) / max(len(lacunes_u2), 1)) * 100
        scores.append((mentor, score))

scores.sort(key=lambda x: x[1], reverse=True)
print(f'Matchings trouves pour Bob: {len(scores)}')
assert len(scores) >= 1
assert any(m[0] == u1 for m in scores)
print('Matching OK.')

# 4. Create and Save Matching
Matching.objects.create(mentor=u1, mentore=u2, score_global=scores[0][1], statut='en_attente')

# 5. Test Messaging (demarrer_conversation)
print('Test de la creation de conversation...')
conv = Conversation.objects.create(utilisateur1=u1, utilisateur2=u2)
msg = Message.objects.create(conversation=conv, expediteur=u1, contenu='Bonjour Bob, pret pour le mentorat Python ?')
print(f'Message envoye de {u1.prenom} a {u2.prenom}.')

# 6. Test Notifications
notif = Notification.objects.create(utilisateur=u2, titre='Nouveau message', message=f'{u1.prenom} vous a envoye un message.', lien=f'/messagerie/{conv.id}/')
print(f'Notification creee pour {u2.prenom}.')

unread = Notification.objects.filter(utilisateur=u2, lu=False).count()
assert unread == 1
print('Notification OK.')

# 7. Test Annonces
print('Test des annonces...')
annonce = DemandeOuOffre.objects.create(auteur=u3, competence=c3, type_publication='demande', description='SVP aidez moi en Maths', format_seance='les_deux')
print(f'Annonce publiee par {u3.prenom}.')
annonces_count = DemandeOuOffre.objects.filter(auteur=u3).count()
assert annonces_count == 1
print('Annonces OK.')

# 8. Cleanup
print('--- NETTOYAGE ---')
Utilisateur.objects.filter(email__contains='@test-advanced.com').delete()
Competence.objects.filter(nom__startswith='TEST_COMP_').delete()
print('Utilisateurs de test et donnees associees (messages, matchings, annonces) supprimes avec succes.')
print('--- TOUS LES TESTS SONT PASSES AVEC SUCCES ---')
