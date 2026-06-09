from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur, CompetenceUtilisateur


@login_required
def mon_profil(request):
    utilisateur = request.user  # ✅ Plus de champ "user" inexistant
    competences = CompetenceUtilisateur.objects.filter(utilisateur=utilisateur)

    context = {
        'utilisateur': utilisateur,
        'competences': competences,
    }
    return render(request, 'my_profil/mon_profil.html', context)  # ✅ Bon dossier


@login_required
def modifier_profil(request):
    utilisateur = request.user  # ✅

    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')

        if nom:
            utilisateur.nom = nom
        if prenom:
            utilisateur.prenom = prenom
        if email:
            utilisateur.email = email

        utilisateur.save()
        messages.success(request, "Profil mis à jour avec succès !")
        return redirect('mon_profil')

    return render(request, 'my_profil/edit_profil.html', {'utilisateur': utilisateur})  # ✅ Bon dossier


@login_required
def profil_public(request, user_id):
    utilisateur = get_object_or_404(Utilisateur, pk=user_id)  # ✅ Ici pk est correct
    competences = CompetenceUtilisateur.objects.filter(utilisateur=utilisateur)

    context = {
        'utilisateur': utilisateur,
        'competences': competences,
    }
    return render(request, 'my_profil/my_profil.html', 'edit_profil/edit_profil.html' , 'public_profil/public_profil.html' context)  # ✅ Bon dossier
