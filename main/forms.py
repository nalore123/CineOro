from django import forms
from .models import Review

#definira obrasce koje korisnik popunjava
#unos recenzija, automatski stvara polje forme prema modelu review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['movie', 'rating', 'comment']#polja za unos
