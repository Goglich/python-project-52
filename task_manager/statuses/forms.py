from django import forms
from .models import Status


class StatusForm(forms.ModelForm):
    name = forms.CharField(
        label="Имя", 
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': "Имя",
        }