from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Utilisateur, CompetenceUtilisateur
from .forms import UserProfileForm, CompetenceForm 

@login_required
def afficher_et_modifier_profil(request):
    
    profil = get_object_or_404(Utilisateur, id=request.user.id)
    
    competence, created = CompetenceUtilisateur.objects.get_or_create(utilisateur=profil)

    if request.method == 'POST':
        form_profil = UserProfileForm(request.POST, instance=profil)
        form_competence = CompetenceForm(request.POST, instance=competence)
        
        if form_profil.is_valid() and form_competence.is_valid():
            form_profil.save()
            form_competence.save()
            
            return redirect('afficher_profil') 
    else:
        form_profil = UserProfileForm(instance=profil)
        form_competence = CompetenceForm(instance=competence)

    context = {
        'profil': profil,
        'form_profil': form_profil,
        'form_competence': form_competence,
    }
    
    return render(request, 'application_principale/templates/profil.html', context)
