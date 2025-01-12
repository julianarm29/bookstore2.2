from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from product.factories import CategoryFactory
import json

class CategoryViewSetTest(APITestCase):

    client = APIClient()

    def setUp(self):
        self.category = CategoryFactory(title='tecnologia')

    def test_create_category(self):
        data = {
            "title": "Novo título"
        }

        # Alterado: Usando a URL sem o 'version' nos kwargs
        response = self.client.post(
            reverse('category-list'),  # Sem o kwargs={'version': 'v1'}
            data=data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_category(self):
        response = self.client.get(
            reverse('category-list')  # Sem o kwargs={'version': 'v1'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
