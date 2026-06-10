from django.urls import path
from . import views

urlpatterns = [
    path('parametres/profil/', views.account_settings, name='account_settings'),
    path('parametres/securite/', views.security_settings, name='security_settings'),
    path('profil/', views.mon_profil, name='mon_profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('profil/<int:user_id>/', views.profil_public, name='profil_public'),
    path('competence/ajouter/', ajouter_competence, name='ajouter_competence'),
    path('competence/supprimer/<int:competence_id>/', supprimer_competence, name='supprimer_competence'),
]
