from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur, CompetenceUtilisateur
from .forms import ProfilUtilisateurForm, CompetenceUtilisateurForm

@login_required
def afficher_profil(request, user_id=None):

    if user_id:
        utilisateur = get_object_or_404(Utilisateur, pk=user_id)
    else:
        utilisateur = get_object_or_404(Utilisateur, user=request.user)

    competences = CompetenceUtilisateur.objects.filter(utilisateur=utilisateur)

    context = {
        'utilisateur': utilisateur,
        'competences': competences,
    }
    return render(request, 'application_principale/profil.html', context)


@login_required
def modifier_profil(request):
    utilisateur = get_object_or_404(Utilisateur, user=request.user)

    if request.method == 'POST':
        form = ProfilUtilisateurForm(request.POST, request.FILES, instance=utilisateur)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('afficher_profil')
    else:
        form = ProfilUtilisateurForm(instance=utilisateur)

    return render(request, 'application_principale/modifier_profil.html', {'form': form})

@login_required
def ajouter_competence(request):

    utilisateur = get_object_or_404(Utilisateur, user=request.user)

    if request.method == 'POST':
        form = CompetenceUtilisateurForm(request.POST)
        if form.is_valid():
            competence = form.save(commit=False)
            competence.utilisateur = utilisateur
            competence.save()
            messages.success(request, "Compétence ajoutée !")
            return redirect('afficher_profil')
    else:
        form = CompetenceUtilisateurForm()

    return render(request, 'application_principale/ajouter_competence.html', {'form': form})

def supprimer_competence(request, competence_id):
    
    competence = get_object_or_404(
        CompetenceUtilisateur, pk=competence_id, utilisateur__user=request.user
    )
    competence.delete()
    messages.success(request, "Compétence supprimée.")
    return redirect('afficher_profil')
