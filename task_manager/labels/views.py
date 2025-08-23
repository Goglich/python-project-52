from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView
from .forms import LabelForm
from .models import Label
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError


class LabelsView(ListView):
    model = Label
    template_name = 'label/index.html'
    context_object_name = 'labels'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
                )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Label.objects.annotate().values(
            'id', 
            'name', 
            'time_create',
        ).order_by('time_create')


class CreateLabelView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
                )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = LabelForm()
        return render(request, 'label/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Метка успешно создана')
            return redirect('labels')
        return render(request, 'label/create.html', {'form': form})
    

class EditLabelView(UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'label/edit.html'
    pk_url_kwarg = 'label_id'
    success_url = reverse_lazy('labels')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
                )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        label = super().get_object(queryset)
        return label
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return redirect(self.success_url)
        messages.success(request, 'Метка успешно изменена')
        return super().post(request, *args, **kwargs)
    

class DeleteLabelView(View):
    success_url = reverse_lazy('labels')
    template_name = 'label/label_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request, 
                'Вы не авторизованы! Пожалуйста, войдите в систему.'
                )
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        label_id = self.kwargs.get('label_id')
        return get_object_or_404(Label, pk=label_id)

    def get(self, request, *args, **kwargs):
        label_to_delete = self.get_object()
        return render(request, self.template_name, {'label': label_to_delete})

    def post(self, request, *args, **kwargs):
        label_to_delete = self.get_object()
        try:
            label_to_delete.delete()
            messages.success(request, 'Метка успешно удалена')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request, 
                'Невозможно удалить метку, потому что она используется'
                )
            return redirect('labels')
