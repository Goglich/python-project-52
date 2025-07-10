from django import forms
from .models import Tag

class TagForm(forms.ModelForm):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': "Имя",
        }