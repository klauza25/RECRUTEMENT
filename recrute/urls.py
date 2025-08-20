from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('postes/', views.job_list, name='job_list'),
    path('postes/<int:pk>/', views.job_detail, name='job_detail'),
    path('postes/<int:pk>/postuler/', views.apply_job, name='apply_job'),  # ← <int:pk> ici
    path('merci/', views.thank_you, name='thank_you'),
    path('confidentialite/', views.privacy, name='privacy'),
]