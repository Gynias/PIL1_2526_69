from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required
def account_settings(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, "Votre profil a été mis à jour avec succès.")
        return redirect('account_settings')
    
    return render(request, 'account_settings.html')

@login_required
def security_settings(request):
    if request.method == 'POST':
        user = request.user
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            messages.error(request, "Le mot de passe actuel est incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
        elif len(new_password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user) # Garde l'utilisateur connecté
            messages.success(request, "Votre mot de passe a été modifié avec succès.")
            return redirect('security_settings')

    return render(request, 'security_settings.html')
