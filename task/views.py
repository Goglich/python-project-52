from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View, UpdateView
from .forms import TaskForm, TaskFilterForm
from .models import Task
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.

class TaskView(ListView):
    model = Task
    template_name = 'task/index.html'
    context_object_name = 'tasks'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Task.objects.select_related('status', 'author', 'executor').order_by('time_create')
        status = self.request.GET.get('status')
        executor = self.request.GET.get('executor')
        label = self.request.GET.get('label')
        self_tasks = self.request.GET.get('self_tasks')
        if status:
            queryset = queryset.filter(status_id=int(status))
        if executor is not None:
            if executor == '':
                queryset = queryset.filter(executor__isnull=True)
            else:
                queryset = queryset.filter(executor_id=int(executor))
        if label:
            queryset = queryset.filter(labels__id=label).distinct()
        if self_tasks:
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context


class CreateTaskView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = TaskForm(user=request.user)
        return render(request, 'task/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Задача успешно создана')
            return redirect('tasks')
        return render(request, 'task/create.html', {'form': form})


class ShowTaskView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_object(self):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(Task, pk=task_id)

    def get(self, request, *args, **kwargs):
        task_to_show = self.get_object()
        return render(request, 'task/show_task.html', {'task': task_to_show})


class EditTaskView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/edit.html'
    pk_url_kwarg = 'task_id'
    success_url = reverse_lazy('tasks')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(self.request, f'Задача успешно изменена')
        return super().form_valid(form)


class DeleteTaskView(View):
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, войдите в систему.')
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        return get_object_or_404(Task, pk=task_id)

    def get(self, request, *args, **kwargs):
        task_to_delete = self.get_object()
        if request.user.id != task_to_delete.author.id:
            messages.error(request, 'Нельзя удалять задачи другого автора')
            return redirect(self.success_url)
        return render(request, self.template_name, {'task': task_to_delete})

    def post(self, request, *args, **kwargs):
        task_to_delete = self.get_object()
        if request.user.id != task_to_delete.author.id:
            messages.error(request, 'Нельзя удалять задачи другого автора')
            return redirect(self.success_url)
        task = task_to_delete.name
        task_to_delete.delete()
        messages.success(request, f'Задача {task} успешно удалена')
        return redirect(self.success_url)