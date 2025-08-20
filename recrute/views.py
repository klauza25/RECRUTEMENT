# recruitment/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Travail, Postuler
from .forms import PostulerForm


def home(request):
    """
    Affiche la page d'accueil avec les 6 dernières offres publiées.
    """
    offres = Travail.objects.filter(publie=True)[:6]  # Limite à 6 offres
    return render(request, 'recruitment/home.html', {'offres': offres})


def about(request):
    """
    Affiche la page "À propos" de l'entreprise.
    """
    return render(request, 'recruitment/about.html')


def job_list(request):
    """
    Affiche la liste des offres d'emploi avec filtres optionnels :
    - par localisation
    - par type de contrat
    """
    offres = Travail.objects.filter(publie=True)

    # Récupération des filtres depuis l'URL (GET)
    localisation = request.GET.get('localisation')
    type_contrat = request.GET.get('type_contrat')

    # Application des filtres si présents
    if localisation:
        offres = offres.filter(localisation__icontains=localisation)
    if type_contrat:
        offres = offres.filter(type_contrat=type_contrat)

    return render(request, 'recruitment/job_list.html', {'offres': offres})


def job_detail(request, pk):
    """
    Affiche le détail d'une offre d'emploi.
    """
    
    poste = get_object_or_404(Travail, pk=pk, publie=True)
    return render(request, 'recruitment/job_detail.html', {'poste': poste})

# recrute/views.py

def apply_job(request, pk):
    poste = get_object_or_404(Travail, pk=pk, publie=True)

    if request.method == 'POST':
        form = PostulerForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.poste = poste
            candidature.save()
            messages.success(request, "Votre candidature a été envoyée avec succès !")
            return redirect('thank_you')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PostulerForm()

    return render(request, 'recruitment/apply.html', {
        'form': form,
        'poste': poste
    })


def thank_you(request):
    """
    Page de remerciement après soumission de la candidature.
    """
    return render(request, 'recruitment/thank_you.html')


def privacy(request):
    """
    Affiche la politique de confidentialité (RGPD).
    """
    return render(request, 'recruitment/privacy.html')