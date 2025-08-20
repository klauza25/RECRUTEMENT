from django.db import models
from django.core.validators import FileExtensionValidator
import os


def cv_upload_path(instance, filename):
    """Organise les CV par poste et date : cvs/développeur-web/2025/04/10/nom-cv.pdf"""
    poste_titre = instance.poste.titre.lower().replace(' ', '-').replace('/', '-')
    annee = instance.date_candidature.year if instance.date_candidature else 'inconnu'
    mois = f"{instance.date_candidature.month:02d}" if instance.date_candidature else '00'
    jour = f"{instance.date_candidature.day:02d}" if instance.date_candidature else '00'
    extension = filename.split('.')[-1].lower()
    nouveau_nom = f"{instance.nom_complet.replace(' ', '-')}-cv.{extension}"
    return f"cvs/{poste_titre}/{annee}/{mois}/{jour}/{nouveau_nom}"


class Travail(models.Model):
    """
    Représente une offre d'emploi.
    """
    TYPES_CONTRAT = [
        ('CDI', 'CDI'),
        ('CDD', 'CDD'),
        ('STAGE', 'Stage'),
        ('FREELANCE', 'Freelance'),
    ]

    titre = models.CharField("Titre du poste", max_length=200)
    localisation = models.CharField("Localisation", max_length=100)
    type_contrat = models.CharField("Type de contrat", max_length=20, choices=TYPES_CONTRAT)
    categorie = models.CharField("Catégorie", max_length=100, blank=True, help_text="Ex : Informatique, Marketing, etc.")
    description = models.TextField("Description du poste")
    profil_recherche = models.TextField("Profil recherché")
    publie = models.BooleanField("Publié", default=True)
    date_creation = models.DateTimeField("Date de création", auto_now_add=True)
    date_modification = models.DateTimeField("Date de modification", auto_now=True)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Offre d'emploi"
        verbose_name_plural = "Offres d'emploi"
        ordering = ['-date_creation']


class Postuler(models.Model):
    """
    Représente une candidature à un poste.
    """
    poste = models.ForeignKey(
        Travail,
        on_delete=models.CASCADE,
        related_name='candidatures',
        verbose_name="Poste"
    )
    nom_complet = models.CharField("Nom complet", max_length=150)
    email = models.EmailField("Adresse email")
    telephone = models.CharField("Téléphone", max_length=20, blank=True, null=True)
    lettre_motivation = models.TextField("Lettre de motivation", blank=True, null=True)
    cv = models.FileField(
        "CV",
        upload_to=cv_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text="Seuls les fichiers PDF, DOC et DOCX sont autorisés."
    )
    date_candidature = models.DateTimeField("Date de candidature", auto_now_add=True)

    def __str__(self):
        return f"✅ {self.nom_complet} → {self.poste.titre}"

    def nom_fichier_cv(self):
        """Retourne le nom du fichier CV sans le chemin."""
        return os.path.basename(self.cv.name)

    class Meta:
        verbose_name = "Candidature"
        verbose_name_plural = "Candidatures"
        ordering = ['-date_candidature']