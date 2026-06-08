from datetime import date, datetime
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max
from .models import DemandeOuOffre, Matching, Utilisateur, Competence, CompetenceUtilisateur, Disponibilite, Conversation, Message

# ==========================================
# MODULE : PARAMÈTRES DU COMPTE (MEMBRE 6)
# ==========================================

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


# ==========================================
# MODULE : TABLEAU DE BORD ET MENTORAT
# ==========================================

@login_required
def tableau_de_bord(request):
    mes_matchings = Matching.objects.filter(
        Q(mentor=request.user) | Q(mentore=request.user)
    ).select_related('mentor', 'mentore').order_by('-score_global')[:5]

    mes_publications = DemandeOuOffre.objects.filter(
        auteur=request.user, statut='ouvert'
    ).select_related('competence').order_by('-date_creation')[:5]

    contexte = {
        'matchings': mes_matchings,
        'publications': mes_publications,
        'utilisateur': request.user,
    }
    # Modifié pour pointer vers le dossier racine templates/
    return render(request, 'dashboard_desktop.html', contexte)


@login_required
def lancer_matching(request):
    utilisateur = request.user

    mes_forces = set(utilisateur.competences.filter(type_competence='force').values_list('competence_id', flat=True))
    mes_lacunes = set(utilisateur.competences.filter(type_competence='lacune').values_list('competence_id', flat=True))
    mes_dispos = list(utilisateur.disponibilites.all())

    autres_utilisateurs = Utilisateur.objects.filter(is_active=True).exclude(id=utilisateur.id)
    resultats = []

    def overlap_minutes(dispo_a, dispo_b):
        if dispo_a.jour != dispo_b.jour:
            return 0
        debut = max(dispo_a.heure_debut, dispo_b.heure_debut)
        fin = min(dispo_a.heure_fin, dispo_b.heure_fin)
        if debut >= fin:
            return 0
        delta = datetime.combine(date.today(), fin) - datetime.combine(date.today(), debut)
        return max(delta.total_seconds() / 60, 0)

    def total_minutes(dispos):
        total = 0
        for dispo in dispos:
            delta = datetime.combine(date.today(), dispo.heure_fin) - datetime.combine(date.today(), dispo.heure_debut)
            total += max(delta.total_seconds() / 60, 0)
        return max(total, 1)

    total_mes_minutes = total_minutes(mes_dispos)

    for autre in autres_utilisateurs:
        if utilisateur.role == 'mentor' and autre.role == 'mentor':
            continue
        if utilisateur.role == 'mentore' and autre.role == 'mentore':
            continue

        forces_autre = set(autre.competences.filter(type_competence='force').values_list('competence_id', flat=True))
        lacunes_autre = set(autre.competences.filter(type_competence='lacune').values_list('competence_id', flat=True))
        dispos_autre = list(autre.disponibilites.all())

        correspondances_mentor = len(mes_lacunes & forces_autre)
        correspondances_mentore = len(mes_forces & lacunes_autre)
        total_possible = max(len(mes_lacunes) + len(lacunes_autre), 1)
        score_comp = ((correspondances_mentor + correspondances_mentore) / total_possible) * 100

        common_minutes = sum(overlap_minutes(a, b) for a in mes_dispos for b in dispos_autre)
        total_autre_minutes = total_minutes(dispos_autre)
        score_horaires = (common_minutes / max(total_mes_minutes, total_autre_minutes, 1)) * 100

        if utilisateur.filiere_id and autre.filiere_id:
            score_filiere = 100 if utilisateur.filiere_id == autre.filiere_id else 40
        else:
            score_filiere = 0

        if utilisateur.niveau and autre.niveau:
            score_niveau = 100 if utilisateur.niveau == autre.niveau else 40
        else:
            score_niveau = 0

        score_global = (
            score_comp * 0.45 +
            score_horaires * 0.30 +
            score_filiere * 0.15 +
            score_niveau * 0.10
        )

        if score_global > 10:
            if utilisateur.role == 'mentor' and autre.role in ['mentore', 'les_deux']:
                mentor, mentore = utilisateur, autre
            elif utilisateur.role == 'mentore' and autre.role in ['mentor', 'les_deux']:
                mentor, mentore = autre, utilisateur
            elif utilisateur.role == 'les_deux' and autre.role == 'mentor':
                mentor, mentore = autre, utilisateur
            elif utilisateur.role == 'les_deux' and autre.role == 'mentore':
                mentor, mentore = utilisateur, ...
            else:
                if correspondances_mentor >= correspondances_mentore:
                    mentor, mentore = autre, utilisateur
                else:
                    mentor, mentore = utilisateur, autre

            matching, created = Matching.objects.update_or_create(
                mentor=mentor,
                mentore=mentore,
                defaults={
                    'score_global': round(score_global, 2),
                    'score_competences': round(score_comp, 2),
                    'score_horaires': round(score_horaires, 2),
                    'score_filiere': round(score_filiere, 2),
                }
            )
            resultats.append(matching)

    resultats.sort(key=lambda m: m.score_global, reverse=True)

    return render(request, 'matching_page.html', {
        'resultats': resultats[:20],
        'utilisateur': utilisateur,
    })


@login_required
def accepter_matching(request, match_id):
    matching = get_object_or_404(Matching, id=match_id, statut='en_attente')
    if request.user not in [matching.mentor, matching.mentore]:
        messages.error(request, "Vous n'êtes pas autorisé à effectuer cette action.")
        return redirect('tableau_de_bord')

    matching.statut = 'accepte'
    matching.save()
    Conversation.get_ou_creer(matching.mentor, matching.mentore, matching)
    messages.success(request, "Matching accepté ! Vous pouvez maintenant discuter.")
    return redirect('tableau_de_bord')


@login_required
def refuser_matching(request, match_id):
    matching = get_object_or_404(Matching, id=match_id)
    if request.user not in [matching.mentor, matching.mentore]:
        messages.error(request, "Action non autorisée.")
        return redirect('tableau_de_bord')

    matching.statut = 'refuse'
    matching.save()
    messages.info(request, "Matching refusé.")
    return redirect('tableau_de_bord')


# ==========================================
# MODULE : MESSAGERIE
# ==========================================

@login_required
def liste_conversations(request):
    conversations = Conversation.objects.filter(
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user)
    ).annotate(
        dernier_message=Max('messages__date_envoi')
    ).order_by('-dernier_message')

    conv_enrichies = []
    for conv in conversations:
        autre = conv.utilisateur2 if conv.utilisateur1 == request.user else conv.utilisateur1
        dernier_msg = conv.messages.order_by('-date_envoi').first()
        non_lus = conv.messages.filter(lu=False).exclude(expediteur=request.user).count()
        conv_enrichies.append({
            'conversation': conv,
            'autre_utilisateur': autre,
            'dernier_message': dernier_msg,
            'non_lus': non_lus,
        })

    return render(request, 'conversations_list_desktop.html', {
        'conversations': conv_enrichies
    })


@login_required
def detail_conversation(request, conv_id):
    conversation = get_object_or_404(
        Conversation,
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user),
        id=conv_id
    )

    conversation.messages.filter(lu=False).exclude(expediteur=request.user).update(lu=True)
    autre = conversation.utilisateur2 if conversation.utilisateur1 == request.user else conversation.utilisateur1
    msgs = conversation.messages.select_related('expediteur').order_by('date_envoi')

    return render(request, 'open_conversation_desktop.html', {
        'conversation': conversation,
        'messages': msgs,
        'autre_utilisateur': autre,
    })


@login_required
def demarrer_conversation(request, user_id):
    autre = get_object_or_404(Utilisateur, id=user_id, is_active=True)
    if autre == request.user:
        messages.error(request, "Vous ne pouvez pas vous envoyer un message à vous-même.")
        return redirect('tableau_de_bord')

    conv = Conversation.get_ou_creer(request.user, autre)
    return redirect('detail_conversation', conv_id=conv.id)


@login_required
@require_POST
def envoyer_message(request, conv_id):
    conversation = get_object_or_404(
        Conversation,
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user),
        id=conv_id
    )

    contenu = request.POST.get('contenu', '').strip()
    if not contenu:
        return JsonResponse({'erreur': 'Message vide'}, status=400)

    message = Message.objects.create(
        conversation=conversation,
        expediteur=request.user,
        contenu=contenu
    )

    return JsonResponse({
        'id': message.id,
        'contenu': message.contenu,
        'expediteur': request.user.nom_complet(),
        'date_envoi': message.date_envoi.strftime('%H:%M'),
        'est_moi': True,
    })


@login_required
def nouveaux_messages(request, conv_id):
    dernier_id = int(request.GET.get('dernier_id', 0))
    conversation = get_object_or_404(
        Conversation,
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user),
        id=conv_id
    )

    nouveaux = conversation.messages.filter(
        id__gt=dernier_id
    ).exclude(expediteur=request.user).select_related('expediteur')

    nouveaux.update(lu=True)

    data = [{
        'id': msg.id,
        'contenu': msg.contenu,
        'expediteur': msg.expediteur.nom_complet(),
        'date_envoi': msg.date_envoi.strftime('%H:%M'),
        'est_moi': False,
    } for msg in nouveaux]

    return JsonResponse({'messages': data})


# ==========================================
# MODULE : AUTHENTIFICATION (MEMBRE 2)
# ==========================================

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
            user_email = user_obj.email
        except Utilisateur.DoesNotExist:
            user_email = None
            
        user = None
        if user_email:
            user = authenticate(request, email=user_email, password=password)
            
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
                email=email,
                mot_de_passe=password,
                prenom=first_name,
                nom=last_name,
                telephone=phone
            )
            
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
