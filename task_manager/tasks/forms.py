from django import forms
from .models import Task
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = CustomUser.objects.filter(is_active=True).order_by('username')
        self.fields['labels'].queryset = Label.objects.all()
        
        for field_name, field in self.fields.items():
            if field_name in ['status', 'executor', 'labels']:
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
            self.save_m2m()
        return instance


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        label='Исполнитель',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label='Метка',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    self_tasks = forms.BooleanField(
        required=False,
        label='Только свои задачи',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )