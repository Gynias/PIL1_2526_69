from .models import Utilisateur, CompetenceUtilisateur, Disponibilite, Correspondance

def calculer_score_compatibilite(mentor, mentore):
    """
    Calcule le score de compatibilite entre un mentor et un mentore sur 100 points.
    Criteres :
    - 50 points : Compatibilite des competences (Points forts du mentor vs Lacunes du mentore)
    - 30 points : Compatibilite des horaires (Disponibilites communes)
    - 20 points : Proximite des filieres
    """
    score = 0
    
    # 1. Compatibilite des competences (Max 50 points)
    forces_mentor = set(CompetenceUtilisateur.objects.filter(utilisateur=mentor, type_competence='FORT').values_list('competence_id', flat=True))
    lacunes_mentore = set(CompetenceUtilisateur.objects.filter(utilisateur=mentore, type_competence='FAIBLE').values_list('competence_id', flat=True))
    
    competences_communes = forces_mentor.intersection(lacunes_mentore)
    
    if lacunes_mentore:
        ratio_competence = len(competences_communes) / len(lacunes_mentore)
        score += ratio_competence * 50
    else:
        score += 25

    # 2. Compatibilite des horaires (Max 30 points)
    dispos_mentor = Disponibilite.objects.filter(utilisateur=mentor)
    dispos_mentore = Disponibilite.objects.filter(utilisateur=mentore)
    
    horaires_compatibles = False
    for dm in dispos_mentor:
        for dme in dispos_mentore:
            if dm.jour_semaine == dme.jour_semaine:
                debut_max = max(dm.heure_debut, dme.heure_debut)
                fin_min = min(dm.heure_fin, dme.heure_fin)
                if debut_max < fin_min:
                    horaires_compatibles = True
                    break
        if horaires_compatibles:
            break
            
    if horaires_compatibles:
        score += 30

    # 3. Proximite des filieres (Max 20 points)
    if mentor.filiere and mentore.filiere:
        if mentor.filiere.lower().strip() == mentore.filiere.lower().strip():
            score += 20
    
    return round(score, 2)

def generer_correspondances(mentore):
    """
    Trouve les meilleurs mentors pour un mentore donne et cree les objets Correspondance en attente.
    """
    mentors_potentiels = Utilisateur.objects.exclude(id=mentore.id)
    
    resultats = []
    for mentor in mentors_potentiels:
        score = calculer_score_compatibilite(mentor, mentore)
        if score > 0:
            resultats.append({
                'mentor': mentor,
                'score': score
            })
            
    resultats = sorted(resultats, key=lambda x: x['score'], reverse=True)
    meilleurs_matchs = resultats[:5]
    
    for match in meilleurs_matchs:
        Correspondance.objects.get_or_create(
            mentor=match['mentor'],
            mentore=mentore,
            defaults={'score_compatibilite': match['score'], 'statut': 'ATTENTE'}
        )
        
    return meilleurs_matchs
