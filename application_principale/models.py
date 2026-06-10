from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class Filiere(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'fields_of_study'
        verbose_name = 'Filière'
        verbose_name_plural = 'Filières'

    def __str__(self):
        return self.nom


class Competence(models.Model):
    nom = models.CharField(max_length=150, unique=True)
    categorie = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'skills'
        verbose_name = 'Compétence'

    def __str__(self):
        return self.nom


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, mot_de_passe=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(mot_de_passe)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mot_de_passe=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, mot_de_passe, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('mentor', 'Mentor'),
        ('mentore', 'Mentoré'),
        ('les_deux', 'Les deux'),
    ]
    NIVEAUX = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, unique=True)
    photo_profil = models.ImageField(upload_to='photos_profil/', blank=True, null=True)
    bio = models.TextField(blank=True)
    filiere = models.ForeignKey(Filiere, on_delete=models.SET_NULL, null=True, blank=True)
    niveau = models.CharField(max_length=10, choices=NIVEAUX, blank=True)
    role = models.CharField(max_length=10, choices=ROLES, default='les_deux')
    est_actif = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    token_reinitialisation = models.CharField(max_length=255, blank=True, null=True)
    token_expire_le = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UtilisateurManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom', 'telephone']

    class Meta:
        db_table = 'users'
        verbose_name = 'Utilisateur'

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class CompetenceUtilisateur(models.Model):
    TYPES = [
        ('force', 'Point fort'),
        ('lacune', 'Lacune'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    type_competence = models.CharField(max_length=10, choices=TYPES)
    niveau = models.PositiveSmallIntegerField(default=3)

    class Meta:
        db_table = 'user_skills'
        unique_together = ('utilisateur', 'competence', 'type_competence')
        verbose_name = 'Compétence utilisateur'

    def __str__(self):
        return f"{self.utilisateur} - {self.competence} ({self.type_competence})"


class Disponibilite(models.Model):
    JOURS = [
        ('Monday', 'Lundi'),
        ('Tuesday', 'Mardi'),
        ('Wednesday', 'Mercredi'),
        ('Thursday', 'Jeudi'),
        ('Friday', 'Vendredi'),
        ('Saturday', 'Samedi'),
        ('Sunday', 'Dimanche'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='disponibilites')
    jour = models.CharField(max_length=10, choices=JOURS)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    class Meta:
        db_table = 'user_availabilities'
        verbose_name = 'Disponibilité'

    def __str__(self):
        return f"{self.utilisateur} - {self.jour} {self.heure_debut}-{self.heure_fin}"


class DemandeOuOffre(models.Model):
    TYPES = [
        ('offre', 'Offre de mentorat'),
        ('demande', 'Demande de mentorat'),
    ]
    FORMATS = [
        ('presentiel', 'Présentiel'),
        ('en_ligne', 'En ligne'),
        ('les_deux', 'Les deux'),
    ]
    STATUTS = [
        ('ouvert', 'Ouvert'),
        ('matche', 'Matché'),
        ('ferme', 'Fermé'),
    ]

    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='publications')
    type_publication = models.CharField(max_length=10, choices=TYPES)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)
    format_seance = models.CharField(max_length=15, choices=FORMATS, default='les_deux')
    jour = models.CharField(max_length=10, choices=Disponibilite.JOURS, blank=True, null=True)
    heure_debut = models.TimeField(blank=True, null=True)
    heure_fin = models.TimeField(blank=True, null=True)
    description = models.TextField(blank=True)
    statut = models.CharField(max_length=10, choices=STATUTS, default='ouvert')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mentoring_requests'
        verbose_name = 'Offre/Demande'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.type_publication} - {self.competence} par {self.auteur}"


class Matching(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]

    mentor = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchings_mentor')
    mentore = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='matchings_mentore')
    score_global = models.DecimalField(max_digits=5, decimal_places=2)
    score_competences = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_horaires = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    score_filiere = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    statut = models.CharField(max_length=15, choices=STATUTS, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'match_suggestions'
        unique_together = ('mentor', 'mentore')
        verbose_name = 'Matching'
        ordering = ['-score_global']

    def __str__(self):
        return f"Match {self.mentor} à {self.mentore} ({self.score_global}%)"

    def competences_communes(self):
        mentor_forces = set(self.mentor.competences.filter(type_competence='force').values_list('competence__nom', flat=True))
        mentore_lacunes = set(self.mentore.competences.filter(type_competence='lacune').values_list('competence__nom', flat=True))
        return sorted(mentor_forces & mentore_lacunes)

    def disponibilites_communes(self):
        result = []
        for dispo_mentor in self.mentor.disponibilites.all():
            for dispo_mentore in self.mentore.disponibilites.all():
                if dispo_mentor.jour != dispo_mentore.jour:
                    continue
                debut = max(dispo_mentor.heure_debut, dispo_mentore.heure_debut)
                fin = min(dispo_mentor.heure_fin, dispo_mentore.heure_fin)
                if debut < fin:
                    result.append(f"{dispo_mentor.get_jour_display()} {debut.strftime('%H:%M')} - {fin.strftime('%H:%M')}")
        return result


class Conversation(models.Model):
    utilisateur1 = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_en1')
    utilisateur2 = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='conversations_en2')
    matching = models.ForeignKey(Matching, on_delete=models.SET_NULL, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'
        verbose_name = 'Conversation'
        unique_together = ('utilisateur1', 'utilisateur2')

    def __str__(self):
        return f"Conv. {self.utilisateur1} et {self.utilisateur2}"

    @staticmethod
    def get_ou_creer(user_a, user_b, matching=None):
        if user_a.id > user_b.id:
            user_a, user_b = user_b, user_a
        conv, cree = Conversation.objects.get_or_create(
            utilisateur1=user_a,
            utilisateur2=user_b,
            defaults={'matching': matching}
        )
        return conv


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    expediteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Message'
        ordering = ['date_envoi']

    def __str__(self):
        return f"{self.expediteur} : {self.contenu[:40]}"


class Notification(models.Model):
    TYPES_NOTIF = (
        ('message', 'Nouveau message'),
        ('alerte', 'Alerte système'),
    )
    
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    type_notif = models.CharField(max_length=20, choices=TYPES_NOTIF, default='message')
    titre = models.CharField(max_length=255)
    message = models.TextField()
    lien = models.CharField(max_length=255, blank=True, null=True)
    lu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        ordering = ['-date_creation']

    def __str__(self):
        return f"Notif: {self.titre} pour {self.utilisateur.email}"
