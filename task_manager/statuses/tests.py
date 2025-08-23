from django.test import TestCase, Client
from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class StatusCRUDIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def test_full_crud_cycle(self):
        # Create
        create_url = reverse('statuses') + 'create/'
        response = self.client.post(create_url, {'name': 'Test Status'})
        self.assertEqual(response.status_code, 302)
        status = Status.objects.first()
        self.assertEqual(status.name, "Test Status")

        # Read
        list_url = reverse('statuses')
        response = self.client.get(list_url)
        self.assertContains(response, "Test Status")

        # Update
        update_url = reverse('edit_status', kwargs={'status_id': status.id})
        response = self.client.post(update_url, {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, "Updated Status")

        # Delete
        delete_url = reverse('delete_status', kwargs={'status_id': status.id})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.count(), 0)