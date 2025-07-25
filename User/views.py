from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterUserForm, LoginUserForm, UserEditForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, View, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

# Create your views here.
class IndexView(ListView):
    model = User
    template_name = 'user/index.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).values(
            'id', 
            'username', 
            'full_name', 
            'date_joined'
        ).order_by('date_joined')


class RegistrationView(CreateView):
    form_class = RegisterUserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        if form.cleaned_data['password'] != form.cleaned_data['password2']:
            form.add_error('password2', "Пароли не совпадают")
            return self.form_invalid(form)
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы залогинены')
        return response
    
    def get_success_url(self):
        return reverse_lazy('main_page')


class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        logout(request)
        return redirect('login')


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user/edit.html'
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('users')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if self.request.user.id != user.id:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя')
            return None
        return user
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)
    

class UserDeleteView(LoginRequiredMixin, View):
    success_url = reverse_lazy('users')
    template_name = 'user/user_confirm_delete.html'

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return get_object_or_404(User, pk=user_id)

    def get(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.id != user_to_delete.id:
            messages.error(request, 'У вас нет прав для удаления другого пользователя')
            return redirect(self.success_url)
        return render(request, self.template_name, {'user': user_to_delete})

    def post(self, request, *args, **kwargs):
        user_to_delete = self.get_object()
        if request.user.id != user_to_delete.id:
            messages.error(request, 'У вас нет прав для удаления другого пользователя')
            return redirect(self.success_url)
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'Пользователь {username} успешно удален')
        return redirect(self.success_url)