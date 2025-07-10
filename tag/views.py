from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView
from .forms import TagForm
from .models import Tag
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError

# Create your views here.
class TagsView(ListView):
    model = Tag
    template_name = 'tag/index.html'
    context_object_name = 'tags'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Tag.objects.annotate().values(
            'id', 
            'name', 
            'time_create',
        ).order_by('time_create')


class CreateTagView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TagForm()
        return render(request, 'tag/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Метка успешно создана')
            return redirect('tags')
        return render(request, 'tag/create.html', {'form': form})
    

class EditTagView(UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tag/edit.html'
    pk_url_kwarg = 'tag_id'
    success_url = reverse_lazy('tags')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        tag = super().get_object(queryset)
        return tag
    
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
    

class DeleteTagView(View):
    success_url = reverse_lazy('tags')
    template_name = 'tag/tag_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        tag_id = self.kwargs.get('tag_id')
        return get_object_or_404(Tag, pk=tag_id)

    def get(self, request, *args, **kwargs):
        tag_to_delete = self.get_object()
        return render(request, self.template_name, {'tag': tag_to_delete})

    def post(self, request, *args, **kwargs):
        tag_to_delete = self.get_object()
        tag_name = tag_to_delete.name
        try:
            tag_to_delete.delete()
            messages.success(request, f'Метка {tag_name} успешно удалена')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(request, 'Нельзя удалить метку, так как она связана с задачами.')
            return redirect('tags')