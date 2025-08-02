from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from task_manager.labels.models import Label

class LabelCRUDTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.label = Label.objects.create(name='Test Label')
        self.labels_url = reverse('labels')
        self.create_url = reverse('create_label')
        self.edit_url = lambda id: reverse('edit_label', kwargs={'label_id': id})
        self.delete_url = lambda id: reverse('delete_label', kwargs={'label_id': id})

    def test_label_list_view(self):
        """Тест отображения списка меток"""
        response = self.client.get(self.labels_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Label')
        self.assertTemplateUsed(response, 'label/index.html')

    def test_create_label_view_get(self):
        """Тест GET-запроса для создания метки"""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/create.html')
        self.assertContains(response, 'Имя')

    def test_create_label_view_post_success(self):
        """Тест успешного создания метки"""
        data = {'name': 'New Label'}
        response = self.client.post(self.create_url, data)
        self.assertRedirects(response, self.labels_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно создана')
        self.assertTrue(Label.objects.filter(name='New Label').exists())

    def test_label_create_view_post_invalid(self):
        """Тест создания метки с невалидными данными"""
        data = {'name': ''}
        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('This field is required.', response.context['form'].errors['name'][0])

    def test_label_edit_view_get(self):
        """Тест GET-запроса для редактирования метки"""
        response = self.client.get(self.edit_url(self.label.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/edit.html')
        self.assertContains(response, 'Test Label')

    def test_label_edit_view_post_success(self):
        """Тест успешного редактирования метки"""
        data = {'name': 'Updated Label'}
        response = self.client.post(self.edit_url(self.label.id), data)
        
        self.assertRedirects(response, self.labels_url)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_edit_view_post_invalid(self):
        """Тест редактирования метки с невалидными данными"""
        data = {'name': ''}
        response = self.client.post(self.edit_url(self.label.id), data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('This field is required.', response.context['form'].errors['name'][0])

    def test_label_delete_view_get(self):
        """Тест GET-запроса для удаления метки"""
        response = self.client.get(self.delete_url(self.label.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'label/label_confirm_delete.html')
        self.assertContains(response, 'Test Label')

    def test_label_delete_view_post_success(self):
        """Тест успешного удаления метки"""
        response = self.client.post(self.delete_url(self.label.id))
        self.assertRedirects(response, self.labels_url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно удалена')
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())


    def test_unauthenticated_access(self):
        """Тест доступа неавторизованного пользователя"""
        self.client.logout()
        
        urls = [
            self.labels_url,
            self.create_url,
            self.edit_url(self.label.id),
            self.delete_url(self.label.id),
        ]
        
        for url in urls:
            response = self.client.get(url)
            self.assertRedirects(response, reverse('login'))
            response = self.client.post(url)
            self.assertRedirects(response, reverse('login'))