from apps.users.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class NoteAPITest(TestCase):

    factory = APIRequestFactory()
    api_client = APIClient()

    @classmethod
    def setUpTestData(cls):
        super(NoteAPITest, cls).setUpTestData()
        try:
            user = User.objects.get(username='testuser')
        except User.DoesNotExist:
            user = User.objects.create_user(
                'testuser', email='testuser@test.com', password='testing')
            user.save()

        token = Token.objects.create(user=user)
        token.save()

    def setUp(self):
        token = Token.objects.get(user__username='testuser')
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_list(self):
        base_url = reverse('mywebmarks-back:external_apis:note-list')
        response = self.api_client.get(base_url)
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        base_url = reverse('mywebmarks-back:external_apis:note-list')
        json = {'id': '', 'title': 'new item'}

        response = self.api_client.post(base_url, json)

        print(response.content)

        self.assertEqual(response.status_code, 201)
