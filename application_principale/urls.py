from django.urls import path
from . import views

urlpatterns = [
    path('profil/', views.mon_profil, name='mon_profil'),
    path('profil/modifier/', views.modifier_profil, name='modifier_profil'),
    path('profil/<int:user_id>/', views.profil_public, name='profil_public'),
]
