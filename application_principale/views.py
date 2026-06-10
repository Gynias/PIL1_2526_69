from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Max
from .models import DemandeOuOffre, Matching, Utilisateur, Competence, CompetenceUtilisateur, Disponibilite, Conversation, Message
import json

def accueil_view(request):
    if request.user.is_authenticated:
        return redirect('tableau_de_bord')
    return render(request, 'accueil.html')

def inscription_view(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        mot_de_passe = request.POST.get('mot_de_passe')
        role = request.POST.get('role', 'les_deux')
        
        # Mappons les valeurs du formulaire au modèle (Mentor/Mentee/Both -> mentor/mentore/les_deux)
        if role == 'Mentor':
            role = 'mentor'
        elif role == 'Mentee':
            role = 'mentore'
        else:
            role = 'les_deux'
            
        if not telephone:
            messages.error(request, "Le numéro de téléphone est obligatoire.")
            return render(request, 'register.html')
            
        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        elif Utilisateur.objects.filter(telephone=telephone).exists():
            messages.error(request, "Ce numéro de téléphone est déjà utilisé.")
        else:
            try:
                utilisateur = Utilisateur.objects.create_user(
                    email=email,
                    mot_de_passe=mot_de_passe,
                    nom=nom,
                    prenom=prenom,
                    telephone=telephone,
                    role=role
                )
                login(request, utilisateur)
                messages.success(request, "Inscription réussie !")
                return redirect('onboarding')
            except Exception as e:
                messages.error(request, "Une erreur s'est produite lors de la création du compte.")
            
    return render(request, 'register.html')

def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        user = authenticate(request, email=email, password=mot_de_passe)
        if user is not None:
            login(request, user)
            return redirect('tableau_de_bord')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    return render(request, 'login.html')

def deconnexion_view(request):
    logout(request)
    messages.info(request, "Vous êtes déconnecté.")
    return redirect('accueil')

@login_required
def create_offer_request(request):
    if request.method == 'POST':
        type_publication = request.POST.get('type_publication')
        competence_id = request.POST.get('competence')
        format_seance = request.POST.get('format_seance')
        jour = request.POST.get('jour')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')
        description = request.POST.get('description', '')

        if type_publication and competence_id:
            try:
                competence = Competence.objects.get(id=competence_id)
                DemandeOuOffre.objects.create(
                    auteur=request.user,
                    type_publication=type_publication,
                    competence=competence,
                    format_seance=format_seance,
                    jour=jour if jour else None,
                    heure_debut=heure_debut if heure_debut else None,
                    heure_fin=heure_fin if heure_fin else None,
                    description=description,
                    statut='ouvert'
                )
                messages.success(request, "Votre annonce a été publiée avec succès !")
                return redirect('offer_request_feed')
            except Competence.DoesNotExist:
                messages.error(request, "La compétence sélectionnée n'existe pas.")
        else:
            messages.error(request, "Veuillez remplir les champs obligatoires (Type et Compétence).")

    competences = Competence.objects.all().order_by('nom')
    jours = Disponibilite.JOURS
    
    return render(request, 'create_offer_request.html', {
        'competences': competences,
        'jours': jours,
    })

from django.core.paginator import Paginator

@login_required
def discover_page(request):
    mentors_list = Utilisateur.objects.filter(role__in=['mentor', 'les_deux'], is_active=True).prefetch_related('competences__competence', 'filiere').order_by('-id')
    
    q = request.GET.get('q', '')
    sujet = request.GET.get('sujet', '')
    niveau = request.GET.get('niveau', '')
    filiere = request.GET.get('filiere', '')
    
    if q:
        mentors_list = mentors_list.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))
    if niveau:
        mentors_list = mentors_list.filter(niveau=niveau)
    if filiere:
        mentors_list = mentors_list.filter(filiere__nom__iexact=filiere)
        
    # Check competence sujet
    if sujet:
        mentors_list = mentors_list.filter(competences__competence__nom__iexact=sujet).distinct()

    paginator = Paginator(mentors_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'discover_page.html', {'mentors': page_obj})

@login_required
def offer_request_detail(request, annonce_id):
    annonce = get_object_or_404(DemandeOuOffre, id=annonce_id)
    
    return render(request, 'offer_request_detail.html', {
        'annonce': annonce
    })

@login_required
def offer_request_feed(request):
    annonces = DemandeOuOffre.objects.filter(statut='ouvert').select_related('auteur', 'competence').order_by('-date_creation')
    
    return render(request, 'offer_request_feed.html', {
        'annonces': annonces
    })

@login_required
def search_results(request):
    mot_cle = request.GET.get('q', '')
    
    if mot_cle:
        resultats = DemandeOuOffre.objects.filter(
            Q(description__icontains=mot_cle) | Q(competence__nom__icontains=mot_cle),
            statut='ouvert'
        ).select_related('auteur', 'competence').order_by('-date_creation')
    else:
        resultats = DemandeOuOffre.objects.none()
        
    return render(request, 'search_results.html', {
        'annonces': resultats,
        'recherche': mot_cle
    })

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
                mentor, mentore = utilisateur, autre
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

    # Get conversations list for the sidebar
    toutes_conversations = Conversation.objects.filter(
        Q(utilisateur1=request.user) | Q(utilisateur2=request.user)
    ).prefetch_related('messages', 'utilisateur1', 'utilisateur2')
    conv_enrichies = []
    for conv in toutes_conversations:
        autre_conv = conv.utilisateur2 if conv.utilisateur1 == request.user else conv.utilisateur1
        dernier_msg = conv.messages.order_by('-date_envoi').first()
        non_lus = conv.messages.filter(lu=False).exclude(expediteur=request.user).count()
        conv_enrichies.append({
            'conversation': conv,
            'autre_utilisateur': autre_conv,
            'dernier_message': dernier_msg,
            'non_lus': non_lus,
        })
    conv_enrichies.sort(key=lambda c: c['dernier_message'].date_envoi if c['dernier_message'] else datetime.min, reverse=True)

    return render(request, 'open_conversation_desktop.html', {
        'conversation': conversation,
        'messages': msgs,
        'autre_utilisateur': autre,
        'conversations': conv_enrichies,
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
# MODULE : PARAMÈTRES ET PROFIL (Membre 3 - Evan)
# ==========================================

@login_required
def account_settings(request):
    if request.method == 'POST':
        request.user.prenom = request.POST.get('first_name', request.user.prenom)
        request.user.nom = request.POST.get('last_name', request.user.nom)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        # Update competences
        forces = request.POST.getlist('forces[]')
        lacunes = request.POST.getlist('lacunes[]')
        
        # Clean existing competences
        CompetenceUtilisateur.objects.filter(utilisateur=request.user).delete()
        
        # Add forces
        for force_id in forces:
            try:
                comp = Competence.objects.get(id=force_id)
                CompetenceUtilisateur.objects.create(utilisateur=request.user, competence=comp, type_competence='force')
            except Competence.DoesNotExist:
                pass

        # Add lacunes
        for lacune_id in lacunes:
            try:
                comp = Competence.objects.get(id=lacune_id)
                CompetenceUtilisateur.objects.create(utilisateur=request.user, competence=comp, type_competence='lacune')
            except Competence.DoesNotExist:
                pass
                
        messages.success(request, "Vos informations ont été mises à jour.")
        return redirect('account_settings')
    
    competences = Competence.objects.all().order_by('nom')
    user_forces = request.user.competences.filter(type_competence='force').values_list('competence_id', flat=True)
    user_lacunes = request.user.competences.filter(type_competence='lacune').values_list('competence_id', flat=True)

    return render(request, 'account_settings.html', {
        'utilisateur': request.user,
        'competences': competences,
        'user_forces': list(user_forces),
        'user_lacunes': list(user_lacunes),
    })

@login_required
def security_settings(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not request.user.check_password(current_password):
            messages.error(request, "L'ancien mot de passe est incorrect.")
        elif new_password != confirm_password:
            messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            # Important : reconnecter l'utilisateur après changement de mot de passe
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            messages.success(request, "Mot de passe modifié avec succès !")
            return redirect('security_settings')
            
    return render(request, 'security_settings.html', {
        'utilisateur': request.user
    })


# ==========================================
# MODULE : ONBOARDING (Membre 2 - Emmanuel)
# ==========================================

@login_required
def onboarding_post_inscription(request):
    if request.method == 'POST':
        forces = request.POST.getlist('forces[]')
        lacunes = request.POST.getlist('lacunes[]')

        # Clean existing competences to prevent duplicates on refresh
        CompetenceUtilisateur.objects.filter(utilisateur=request.user).delete()

        # Add forces
        for force_id in forces:
            try:
                comp = Competence.objects.get(id=force_id)
                CompetenceUtilisateur.objects.create(utilisateur=request.user, competence=comp, type_competence='force')
            except Competence.DoesNotExist:
                pass

        # Add lacunes
        for lacune_id in lacunes:
            try:
                comp = Competence.objects.get(id=lacune_id)
                CompetenceUtilisateur.objects.create(utilisateur=request.user, competence=comp, type_competence='lacune')
            except Competence.DoesNotExist:
                pass

        return redirect('tableau_de_bord')

    competences = Competence.objects.all().order_by('nom')
    return render(request, 'onboarding.html', {
        'utilisateur': request.user,
        'competences': competences
    })

