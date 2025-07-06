from django import forms
from .models import Task
from status.models import Status
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'assignee']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['status'].queryset = Status.objects.all()
        self.fields['assignee'].queryset = User.objects.all()
        
        for field_name, field in self.fields.items():
            if field_name in ['status', 'assignee']:
                field.widget.attrs.update({'class': 'form-select'})
            elif not isinstance(field.widget, forms.CheckboxInput):
                if 'class' not in field.widget.attrs:
                    field.widget.attrs['class'] = 'form-control'
            
            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Введите название задачи'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Опишите задачу подробнее'
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user
        if commit:
            instance.save()
        return instance