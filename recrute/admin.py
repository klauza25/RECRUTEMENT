# recruitment/admin.py

import os
from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils.safestring import mark_safe
from .models import Travail, Postuler

# --- 🔴 Ajoute ce bloc ici ---
# === Couleurs personnalisées pour l'admin (en harmonie avec ta home) ===
custom_css = """
<style>
    /* Couleur d'en-tête : bleu doux (comme dans ta home) */
    #header {
        background: green !important; /* Bleu vif mais élégant (blue-600) */
        background-image: none !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Texte blanc dans l'en-tête */
    #branding h1 a, #branding h2 a {
        color: white !important;
        font-weight: 800;
    }

    /* Liens dans les modules (liste des objets) */
    .module a {
        color: orange !important; /* Bleu cohérent avec ta home */
    }
    .module a:hover {
        background-color: #dbeafe !important; /* Bleu très clair au hover */
        border-radius: 4px;
    }

    /* Boutons d'action (comme "Enregistrer") */
    .submit-row input[type="submit"] {
        background: green !important; /* Bleu un peu plus clair pour le bouton */
        border: none !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    .submit-row input[type="submit"]:hover {
        background: #1d4ed8 !important; /* Bleu plus foncé au hover */
    }

    /* Bordures des champs et sélecteurs */
    .actions select, .actions input {
        border: 1px solid #2563eb !important;
        border-radius: 4px;
    }

    /* Pagination et autres boutons par défaut */
    .default {
        background: #3b82f6 !important;
        border: none !important;
    }
    .default:hover {
        background: #1d4ed8 !important;
    }

    /* Tableaux : entête */
    .model-postuler .results th, 
    .model-travail .results th {
        background-color: green !important;
        font-weight: 800;
    }

    /* Amélioration visuelle globale */
    body {
        background-color: gray !important; /* Fond clair, comme dans Tailwind */
    }
</style>
"""

admin.site.site_header = "RecrutPro - Espace Administrateur"
admin.site.site_title = "RecrutPro"
admin.site.index_title = mark_safe(f"Administration des candidatures {custom_css}")
# --- Fin du bloc ---



@admin.register(Travail)
class TravailAdmin(admin.ModelAdmin):
    list_display = ('titre', 'localisation', 'type_contrat', 'categorie', 'publie', 'date_creation')
    list_filter = ('publie', 'type_contrat', 'categorie', 'localisation', 'date_creation')
    search_fields = ('titre', 'description', 'profil_recherche')
    prepopulated_fields = {'categorie': ('titre',)}
    date_hierarchy = 'date_creation'
    ordering = ['-date_creation']
    fieldsets = (
        ("Informations du poste", {
            'fields': ('titre', 'localisation', 'type_contrat', 'categorie')
        }),
        ("Description", {
            'fields': ('description', 'profil_recherche')
        }),
        ("Publication", {
            'fields': ('publie',)
        }),
    )


def envoyer_email_retenu(modeladmin, request, queryset):
    """
    Action admin : Envoyer un email aux candidats sélectionnés pour les informer qu'ils sont retenus.
    """
    total_envoyes = 0
    total_erreurs = 0

    for candidature in queryset:
        try:
            sujet = f"Félicitations ! Vous êtes retenu(e) pour le poste : {candidature.poste.titre}"
            message = f"""
Bonjour {candidature.nom_complet},

Nous sommes heureux de vous informer que votre candidature pour le poste de **{candidature.poste.titre}** 
a été retenue ! 

Nous allons prendre contact avec vous dans les prochains jours pour la suite du processus.

Félicitations et à très bientôt,

L'équipe de recrutement
"""

            send_mail(
                subject=sujet,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL or 'recrutement@votreentreprise.com',
                recipient_list=[candidature.email],
                fail_silently=False,  # Pour attraper les erreurs
            )
            total_envoyes += 1

        except Exception as e:
            modeladmin.message_user(
                request,
                f"Échec de l'envoi à {candidature.email} : {str(e)}",
                level=messages.ERROR
            )
            total_erreurs += 1

    # Message de résumé
    if total_envoyes > 0:
        modeladmin.message_user(
            request,
            f"Emails envoyés avec succès à {total_envoyes} candidat(s).",
            level=messages.SUCCESS
        )
    if total_erreurs > 0:
        modeladmin.message_user(
            request,
            f"Échec de l'envoi à {total_erreurs} candidat(s).",
            level=messages.WARNING
        )


envoyer_email_retenu.short_description = "📧 Envoyer un email : Candidat retenu"


@admin.register(Postuler)
class PostulerAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'email', 'poste', 'date_candidature', 'nom_fichier_cv')
    list_filter = ('date_candidature', 'poste')
    search_fields = ('nom_complet', 'email', 'poste__titre')
    readonly_fields = ('date_candidature',)
    date_hierarchy = 'date_candidature'
    ordering = ['-date_candidature']
    actions = [envoyer_email_retenu]  # 👈 Action ajoutée ici

    def nom_fichier_cv(self, obj):
        return os.path.basename(obj.cv.name)
    nom_fichier_cv.short_description = "Nom du fichier CV"