import json

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task


class TasksAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.task_data = {'title': 'New Task', 'description': 'Task description', 'completed': False}
        self.task = Task.objects.create(**self.task_data)

    def test_create_task(self):
        response = self.client.post(reverse('task-list'), data=json.dumps({'title': 'New Task'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(Task.objects.get(id=response.data['id']).title, "New Task")

    def test_create_empty_title(self):
        response = self.client.post(reverse('task-list'),
                                    data=json.dumps({'title': '', 'description': 'test description'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'][0], 'This field may not be blank.')

    def test_create_without_title(self):
        response = self.client.post(reverse('task-list'),
                                    data=json.dumps({'description': 'test description', 'completed': True}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'][0], 'This field is required.')

    def test_get_tasks(self):
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        response = self.client.put(reverse('task-detail', args=[self.task.id]),
                                   data=json.dumps({'title': 'Updated Task'}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(reverse('task-detail', args=[self.task.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
