from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm


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
            'executor': self.user2.id
        }
        
        response = self.client.post(reverse('tasks_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        
        self.assertTrue(Task.objects.filter(name='New Task').exists())
        
    def test_task_detail_view(self):
        """Тест просмотра деталей задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse(
            'task', 
            kwargs={'task_id': self.task.id}
            ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/show_task.html')
        self.assertEqual(response.context['task'], self.task)
        
    def test_task_edit_view_get(self):
        """Тест GET запроса на редактирование задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.get(reverse(
            'edit_task', 
            kwargs={'task_id': self.task.id}
            ))
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
            'executor': self.user2.id
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
        
        response = self.client.get(reverse(
            'delete_task', 
            kwargs={'task_id': self.task.id}
            ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task/task_confirm_delete.html')
        self.assertEqual(response.context['task'], self.task)
        
    def test_task_delete_view_post(self):
        """Тест POST запроса на удаление задачи"""
        self.client.login(username='user1', password='password123')
        
        response = self.client.post(reverse(
            'delete_task', 
            kwargs={'task_id': self.task.id}
            ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        
    def test_task_delete_by_non_author(self):
        """Тест попытки удаления задачи не автором"""
        self.client.login(username='user2', password='password123')
        response = self.client.get(reverse(
            'delete_task', 
            kwargs={'task_id': self.task.id}
            ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        response = self.client.post(reverse(
            'delete_task', 
            kwargs={'task_id': self.task.id}
            ))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
        
    def test_task_form_save(self):
        """Тест сохранения формы задачи"""
        form_data = {
            'name': 'Form Task',
            'description': 'Form Description',
            'status': self.status.id,
            'executor': self.user2.id
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


class TaskFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(
            username='user1',
            password='testpass123',
            first_name='User1',
            last_name='Test'
        )
        cls.user2 = User.objects.create_user(
            username='user2',
            password='testpass123',
            first_name='User2',
            last_name='Test'
        )
        
        cls.status1 = Status.objects.create(name='Статус 1')
        cls.status2 = Status.objects.create(name='Статус 2')
        cls.label1 = Label.objects.create(name='Метка 1')
        cls.label2 = Label.objects.create(name='Метка 2')
        cls.task1 = Task.objects.create(
            name='Задача 1',
            description='Описание задачи 1',
            author=cls.user1,
            executor=cls.user2,
            status=cls.status1
        )
        cls.task1.labels.add(cls.label1)
        cls.task2 = Task.objects.create(
            name='Задача 2',
            description='Описание задачи 2',
            author=cls.user2,
            executor=None,
            status=cls.status2
        )
        cls.task2.labels.add(cls.label2)
        cls.task3 = Task.objects.create(
            name='Задача 3',
            description='Описание задачи 3',
            author=cls.user1,
            executor=cls.user1,
            status=cls.status1
        )
        cls.task3.labels.add(cls.label1, cls.label2)

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user1)

    def test_filter_by_status(self):
        response = self.client.get(
            reverse('tasks'), 
            {'status': self.status1.id}
            )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task3, tasks)
        response = self.client.get(
            reverse('tasks'), 
            {'status': self.status2.id}
            )
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertIn(self.task2, tasks)

    def test_filter_by_executor(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(len(response.context['tasks']), 3)
        response = self.client.get(
            reverse('tasks'), 
            {'executor': self.user2.id}
            )
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1, 
            f"Ожидалась 1 задача, получено {len(tasks)}.")
        self.assertIn(self.task1, tasks)
        self.assertNotIn(self.task2, tasks)
        self.assertNotIn(self.task3, tasks)
        response = self.client.get(
            reverse('tasks'), 
            {'executor': self.user1.id}
            )
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertIn(self.task3, tasks)
        response = self.client.get(reverse('tasks'), {'executor': ''})
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertIn(self.task2, tasks)

    def test_filter_self_tasks(self):
        response = self.client.get(reverse('tasks'), {'self_tasks': 'on'})
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task3, tasks)
        self.assertNotIn(self.task2, tasks)

    def test_combined_filters(self):
        response = self.client.get(reverse('tasks'), {
            'status': self.status1.id,
            'label': self.label1.id,
            'self_tasks': 'on'
        })
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task3, tasks)
        response = self.client.get(reverse('tasks'), {
            'status': self.status1.id,
            'label': self.label2.id
        })
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(len(tasks), 1)
        self.assertIn(self.task3, tasks)

    def test_filter_form_in_context(self):
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('filter_form', response.context)
        self.assertEqual(len(response.context['filter_form'].fields), 4)

    def test_reset_filters(self):
        response = self.client.get(reverse('tasks'), {
            'status': self.status1.id,
            'label': self.label1.id,
            'self_tasks': 'on'
        })
        self.assertEqual(len(response.context['tasks']), 2)
        
        response = self.client.get(reverse('tasks'))
        self.assertEqual(len(response.context['tasks']), 3)