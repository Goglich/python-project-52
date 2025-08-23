from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView
from .forms import StatusForm
from .models import Status
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError

# Create your views here.
class StatusView(ListView):
    model = Status
    template_name = 'status/index.html'
    context_object_name = 'statuses'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Status.objects.annotate().values(
            'id', 
            'name', 
            'time_create',
        ).order_by('time_create')


class CreateStatusView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'status/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Статус успешно создан')
            return redirect('statuses')
        return render(request, 'status/create.html', {'form': form})
    

class EditStatusView(UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'status/edit.html'
    pk_url_kwarg = 'status_id'
    success_url = reverse_lazy('statuses')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        status = super().get_object(queryset)
        return status
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        messages.success(request, f'Статус успешно изменен')
        return super().post(request, *args, **kwargs)
    

class StatusDeleteView(View):
    success_url = reverse_lazy('statuses')
    template_name = 'status/status_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        status_id = self.kwargs.get('status_id')
        return get_object_or_404(Status, pk=status_id)

    def get(self, request, *args, **kwargs):
        status_to_delete = self.get_object()
        return render(request, self.template_name, {'status': status_to_delete})

    def post(self, request, *args, **kwargs):
        status_to_delete = self.get_object()
        status_name = status_to_delete.name
        try:
            status_to_delete.delete()
            messages.success(request, f'Статус успешно удален')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить статус, потому что он используется')
            return redirect('statuses')