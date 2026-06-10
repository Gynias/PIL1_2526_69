import os
import django
from django.test import Client
from django.urls import reverse
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_mentorlink.settings')
django.setup()

client = Client()
errors = []

def test_url(url_name, kwargs=None, expected_status=200):
    try:
        url = reverse(url_name, kwargs=kwargs)
    except Exception as e:
        print(f'Routing failed for {url_name}: {e}')
        errors.append(f'{url_name}: {e}')
        return
        
    print(f'Testing GET {url} ...', end=' ')
    response = client.get(url)
    if response.status_code != expected_status and response.status_code != 302:
        print(f'FAIL (Got {response.status_code})')
        errors.append(f'{url_name}: Expected {expected_status} or 302, got {response.status_code}')
        if response.status_code == 500:
            print(response.content.decode('utf-8')[:500])
    else:
        print(f'OK ({response.status_code})')
    return response

# 1. Unauthenticated routes
test_url('accueil')
test_url('inscription')
test_url('connexion')

# 2. Create user and login
from application_principale.models import Utilisateur, Competence, CompetenceUtilisateur
import time

rand_tel = str(int(time.time()))
user = Utilisateur.objects.create_user(email=f'test{rand_tel}@example.com', prenom='Test', nom='User', mot_de_passe='password123', role='les_deux', telephone=rand_tel)
comp = Competence.objects.create(nom=f'Test Comp {rand_tel}')
CompetenceUtilisateur.objects.create(utilisateur=user, competence=comp, type_competence='force')

print('Logging in...')
client.login(email=f'test{rand_tel}@example.com', password='password123')

# 3. Authenticated routes
test_url('tableau_de_bord')
test_url('onboarding')
test_url('mon_profil')
test_url('account_settings')
test_url('discover_page')
test_url('offer_request_feed')
test_url('liste_conversations')
test_url('lancer_matching')
test_url('modifier_profil')
test_url('security_settings')
test_url('profil_public', kwargs={'user_id': user.id})

if errors:
    print('\nERRORS FOUND:')
    for err in errors:
        print(err)
else:
    print('\nALL TESTS PASSED!')
