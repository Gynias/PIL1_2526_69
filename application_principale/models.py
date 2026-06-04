from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    filiere = models.CharField(max_length=100, null=True, blank=True)
    niveau_etudes = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Profil(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profil')
    photo = models.ImageField(upload_to='profils/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    centres_interet = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Profil de {self.utilisateur.username}"

class Competence(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nom

class CompetenceUtilisateur(models.Model):
    CHOIX_TYPE = (
        ('FORT', 'Point Fort (Peut enseigner)'),
        ('FAIBLE', 'Point Faible (A besoin d\'aide)'),
    )
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    type_competence = models.CharField(max_length=10, choices=CHOIX_TYPE)

    class Meta:
        unique_together = ('utilisateur', 'competence', 'type_competence')

    def __str__(self):
        return f"{self.utilisateur.username} - {self.competence.nom} ({self.type_competence})"

class Disponibilite(models.Model):
    CHOIX_JOURS = (
        ('LUN', 'Lundi'),
        ('MAR', 'Mardi'),
        ('MER', 'Mercredi'),
        ('JEU', 'Jeudi'),
        ('VEN', 'Vendredi'),
        ('SAM', 'Samedi'),
        ('DIM', 'Dimanche'),
    )
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='disponibilites')
    jour_semaine = models.CharField(max_length=3, choices=CHOIX_JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.utilisateur.username}: {self.get_jour_semaine_display()} {self.heure_debut}-{self.heure_fin}"

class Annonce(models.Model):
    CHOIX_TYPE = (
        ('OFFRE', 'Offre de mentorat'),
        ('DEMANDE', 'Demande de mentorat'),
    )
    CHOIX_FORMAT = (
        ('LIGNE', 'En ligne'),
        ('PRESENTIEL', 'Présentiel'),
        ('MIXTE', 'Mixte'),
    )
    CHOIX_STATUT = (
        ('OUVERT', 'Ouvert'),
        ('FERME', 'Fermé'),
    )
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='annonces')
    type_annonce = models.CharField(max_length=10, choices=CHOIX_TYPE)
    format_annonce = models.CharField(max_length=15, choices=CHOIX_FORMAT)
    statut = models.CharField(max_length=10, choices=CHOIX_STATUT, default='OUVERT')
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    competences_ciblees = models.ManyToManyField(Competence, related_name='annonces')

    def __str__(self):
        return f"{self.get_type_annonce_display()} par {self.auteur.username}"

class Message(models.Model):
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='messages_recus')
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"De {self.expediteur.username} à {self.destinataire.username}"

class Correspondance(models.Model):
    CHOIX_STATUT = (
        ('ATTENTE', 'En attente'),
        ('ACCEPTE', 'Accepté'),
        ('REFUSE', 'Refusé'),
    )
    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='correspondances_mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='correspondances_mentore')
    score_compatibilite = models.FloatField()
    statut = models.CharField(max_length=15, choices=CHOIX_STATUT, default='ATTENTE')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Correspondance: {self.mentor.username} & {self.mentore.username} ({self.score_compatibilite}%)"
