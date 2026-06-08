from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from .models import Utilisateur, Profil

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


# --- MODULE AUTHENTIFICATION (MEMBRE 2) ---

def connexion_view(request):
    if request.user.is_authenticated:
        return redirect('account_settings')
        
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')
        
        if not identifier or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'login.html')
            
        # Authentifier par email ou par téléphone
        try:
            if '@' in identifier:
                user_obj = Utilisateur.objects.get(email=identifier)
            else:
                user_obj = Utilisateur.objects.get(telephone=identifier)
            username = user_obj.username
        except Utilisateur.DoesNotExist:
            username = None
            
        user = None
        if username:
            user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie.")
            return redirect('account_settings')
        else:
            messages.error(request, "Email/Téléphone ou mot de passe incorrect.")
            
    return render(request, 'login.html')


def inscription_view(request):
    if request.user.is_authenticated:
        return redirect('account_settings')
        
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Validation
        if not first_name or not last_name or not email or not password:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, 'sign_up.html')
            
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return render(request, 'sign_up.html')
            
        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée.")
            return render(request, 'sign_up.html')
            
        if phone and Utilisateur.objects.filter(telephone=phone).exists():
            messages.error(request, "Ce numéro de téléphone est déjà utilisé.")
            return render(request, 'sign_up.html')
            
        try:
            # Création de l'utilisateur
            user = Utilisateur.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                telephone=phone
            )
            # Création du profil associé
            Profil.objects.create(utilisateur=user)
            
            # Connexion automatique
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès.")
            return redirect('account_settings')
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de l'inscription : {str(e)}")
            
    return render(request, 'sign_up.html')


def deconnexion_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect('login')
