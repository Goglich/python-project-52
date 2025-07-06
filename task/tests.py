from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from status.models import Status
from task.models import Task
from task.forms import TaskForm

class TaskCRUDTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', 
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2', 
            password='password123'
        )
        
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            author=self.user1,
            status=self.status
        )
        
        self.client = Client()
        
    def test_task_list_view(self):
        """Тест отображения списка задач"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/index.html')
        self.assertContains(response, 'Test Task')
        
    def test_task_create_view_get(self):
        """Тест GET запроса на создание задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('tasks_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/create.html')
        self.assertIsInstance(response.context['form'], TaskForm)
        
    def test_task_create_view_post(self):
        """Тест POST запроса на создание задачи"""
        self.client.login(username='user1', password='password123')
        
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'assignee': self.user2.id
        }
        
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        
    def test_task_detail_view(self):
        """Тест просмотра деталей задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/show_task.html')
        self.assertEqual(response.context['task'], self.task)
        
    def test_task_edit_view_get(self):
        """Тест GET запроса на редактирование задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('edit_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/edit.html')
        self.assertIsInstance(response.context['form'], TaskForm)
        
    def test_task_edit_view_post(self):
        """Тест POST запроса на редактирование задачи"""
        self.client.login(username='user1', password='password123')
        
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'assignee': self.user2.id
        }
        
        response = self.client.post(
            reverse('edit_task', kwargs={'task_id': self.task.id}),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')
        
    def test_task_delete_view_get(self):
        """Тест GET запроса на удаление задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_confirm_delete.html')
        self.assertEqual(response.context['task'], self.task)
        
    def test_task_delete_view_post(self):
        """Тест POST запроса на удаление задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.post(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        
    def test_task_delete_by_non_author(self):
        """Тест попытки удаления задачи не автором"""
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        response = self.client.post(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
        
    def test_task_form_save(self):
        """Тест сохранения формы задачи"""
        form_data = {
            'name': 'Form Task',
            'description': 'Form Description',
            'status': self.status.id,
            'assignee': self.user2.id
        }
        
        form = TaskForm(data=form_data, user=self.user1)
        self.assertTrue(form.is_valid())
        
        task = form.save()
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.name, 'Form Task')
        
def test_unauthenticated_access(self):
    """Тест доступа неавторизованных пользователей"""
    urls = [
        reverse('tasks'),
        reverse('tasks_create'),
        reverse('task', kwargs={'task_id': self.task.id}),
        reverse('edit_task', kwargs={'task_id': self.task.id}),
        reverse('delete_task', kwargs={'task_id': self.task.id}),
    ]
    
    for url in urls:
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        self.assertTrue(response.url.startswith(reverse('login')))
        
        if url != reverse('tasks_create'):
            self.assertIn('next=', response.url)