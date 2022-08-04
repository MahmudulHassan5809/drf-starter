from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.client = APIClient()
        user = User.objects.create_user(
            email='admin@gmail.com',
            password="admin",
            username="admin",
            phone_number='phone_number',
            is_superuser=True,
            is_staff=True
        )
        user.save()
        cls.user = user
        cls.client.force_authenticate(user=user)

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
