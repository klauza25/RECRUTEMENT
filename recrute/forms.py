# recruitment/forms.py

from django import forms
from django.core.validators import FileExtensionValidator
from .models import Postuler

# recrute/forms.py
from django import forms
from django.core.validators import FileExtensionValidator
from .models import Postuler

class PostulerForm(forms.ModelForm):
    class Meta:
        model = Postuler
        fields = ['nom_complet', 'email', 'telephone', 'lettre_motivation', 'cv']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-200'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-200'}),
            'telephone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-200'}),
            'lettre_motivation': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring focus:ring-blue-200', 'rows': 4}),
            'cv': forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cv'].validators.append(
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx'],
                message="Seuls les fichiers PDF, DOC et DOCX sont autorisés."
            )
        )

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv and cv.size > 10 * 1024 * 1024:  # 10 Mo
            raise forms.ValidationError("Le fichier est trop volumineux. Taille max : 10 Mo.")
        return cv

