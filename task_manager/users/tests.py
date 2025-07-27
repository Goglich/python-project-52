from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import pytest

User = get_user_model()

@pytest.mark.django_db
def test_load_users():
    User = get_user_model()
    
    User.objects.create(
        username='user1',
        first_name='Иван',
        last_name='Иванов',
        password=make_password('TestPass123'),
        is_active=True
    )
    
    User.objects.create(
        username='user2',
        first_name='Петр',
        last_name='Петров',
        password=make_password('TestPass123'),
        is_active=True
    )
    
    User.objects.create(
        username='user3',
        first_name='Сергей',
        last_name='Сергеев',
        password=make_password('TestPass123'),
        is_active=True
    )
    
    assert User.objects.count() == 3

class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        self.user = User.objects.create_user(
            username='existinguser',
            password='existingpass123',
            first_name='Existing',
            last_name='User'
        )
        self.login_url = reverse('login')
        self.users_list_url = reverse('users')
        self.create_user_url = '/users/create/'
        self.edit_user_url = reverse('edit_user', args=[self.user.id])
        self.delete_user_url = reverse('delete_user', args=[self.user.id])


    def test_user_registration_success(self):
        response = self.client.post(self.create_user_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data['password2'] = 'wrongpass'
        response = self.client.post(self.create_user_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())


    def test_user_edit_authenticated(self):
        self.client.login(username='existinguser', password='existingpass123')
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'updateduser',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(self.edit_user_url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_list_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_edit_unauthenticated(self):
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'updateduser',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(self.edit_user_url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.login_url))


    def test_user_edit_other_user(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        updated_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'username': 'updateduser',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(self.edit_user_url, data=updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_list_url)


    def test_user_delete_authenticated(self):
        self.client.login(username='existinguser', password='existingpass123')
        response = self.client.post(self.delete_user_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.users_list_url)
        self.assertFalse(User.objects.filter(username='existinguser').exists())

    def test_user_delete_unauthenticated(self):
        response = self.client.post(self.delete_user_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(self.login_url))

    def test_user_delete_other_user(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        initial_count = User.objects.count()
        response = self.client.post(self.delete_user_url)
        self.assertEqual(User.objects.count(), initial_count)
        self.assertTrue(User.objects.filter(username='existinguser').exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.users_list_url)