from django import forms
from .models import Label

class LabelForm(forms.ModelForm):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': "Имя",
        }