from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'}),
        required=True
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Фамилия'}),
        required=True
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя пользователя'}),
        required=True
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Пароль'}),
        required=True
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Подтверждение пароля'}),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")

        return cleaned_data
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует")
        return username

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя пользователя'})
    )
    password = forms.CharField(
        label="Пароль", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Пароль'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Имя пользователя"
        self.fields['password'].label = "Пароль"


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя'})
    )
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ПарФамилияоль'})
    )
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Имя пользователя'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Пароль'}),
        required=True
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Подтверждение пароля'}),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return cleaned_data

    #def save(self, commit=True):
    #    user = super().save(commit=False)
    #    password1 = self.cleaned_data.get('password1')
    #    if password1:
    #        user.set_password(password1)
    #    if commit:
    #        user.save()
    #    return user