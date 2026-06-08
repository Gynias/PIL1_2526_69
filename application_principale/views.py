from django.shortcuts import render
class Utilisateur:

    def __init__(self, id_utilisateur, nom, email, competences=None):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.email = email
        self.competences = competences if competences is not None else []

    def afficher_profil(self):
        print("\n" + "=" * 30)
        print(f"PROFIL DE L'UTILISATEUR (ID: {self.id_utilisateur})")
        print("=" * 30)
        print(f"Nom : {self.nom}")
        print(f"Email : {self.email}")
        print("-" * 30)
        if self.competences:
            print("Compétences :")
            for comp in self.competences:
                print(f"  - {comp}")
        else:
            print("Aucune compétence enregistrée.")
        print("=" * 30 + "\n")

    def modifier_profil(self, nouveau_nom=None, nouvel_email=None):
            self.nom = nouveau_nom
            print(f"[Succès] Le nom a été mis à jour : {self.nom}")
        if nouvel_email:
            self.email = nouvel_email
            print(f"[Succès] L'adresse email a été mise à jour : {self.email}")

    def enregistrer_competence(self, nouvelle_competence) :
        comp_nettoyee = nouvelle_competence.strip()

        if comp_nettoyee and comp_nettoyee not in self.competences:
            self.competences.append(comp_nettoyee)
            print(
                f"[Succès] Compétence '{comp_nettoyee}' ajoutée avec succès."
            )
        elif comp_nettoyee in self.competences:
            print(f"[Info] La compétence '{comp_nettoyee}' existe déjà.")
        else:
            print("[Erreur] La compétence ne peut pas être vide.")
