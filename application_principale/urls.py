from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.accueil_view, name='accueil'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('deconnexion/', views.deconnexion_view, name='deconnexion'),
    path('annonces/creer/', views.create_offer_request, name='create_offer_request'),
    path('annonces/decouvrir/', views.discover_page, name='discover_page'),
    path('annonces/detail/<int:annonce_id>/', views.offer_request_detail, name='offer_request_detail'),
    path('annonces/fil/', views.offer_request_feed, name='offer_request_feed'),
    path('annonces/recherche/', views.search_results, name='search_results'),
    path('parametres/profil/', views.account_settings, name='account_settings'),
    path('parametres/securite/', views.security_settings, name='security_settings'),

    # MODULE : ONBOARDING (Membre 2)
    path('onboarding/', views.onboarding_post_inscription, name='onboarding'),

    # MODULE : TABLEAU DE BORD ET MENTORAT (Membre 1)
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('matching/', views.lancer_matching, name='lancer_matching'),
    path('matching/accepter/<int:match_id>/', views.accepter_matching, name='accepter_matching'),
    path('matching/refuser/<int:match_id>/', views.refuser_matching, name='refuser_matching'),

    # MODULE : MESSAGERIE (Membre 1)
    path('messagerie/', views.liste_conversations, name='liste_conversations'),
    path('messagerie/<int:conv_id>/', views.detail_conversation, name='detail_conversation'),
    path('messagerie/demarrer/<int:user_id>/', views.demarrer_conversation, name='demarrer_conversation'),
    path('messagerie/<int:conv_id>/envoyer/', views.envoyer_message, name='envoyer_message'),
    path('messagerie/<int:conv_id>/nouveaux/', views.nouveaux_messages, name='nouveaux_messages'),
]
