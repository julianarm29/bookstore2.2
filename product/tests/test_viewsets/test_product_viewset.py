from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from order.factories import UserFactory, OrderFactory
from product.factories import ProductFactory, CategoryFactory
from rest_framework.authtoken.models import Token
import json
from order.models import Order

class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        self.category = CategoryFactory(title='tecnologia')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Alterado: Usando a URL sem o 'version' nos kwargs
        response = self.client.get(
            reverse('order-list')  # Sem o kwargs={'version': 'v1'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_data = json.loads(response.content)
        self.assertEqual(order_data['results'][0]['product'][0]['title'], self.product.title)

    def test_create_order(self):
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        user = UserFactory()
        product = ProductFactory()

        data = json.dumps({
            'products_id': [product.id],
            'user': user.id
        })

        # Alterado: Usando a URL sem o 'version' nos kwargs
        response = self.client.post(
            reverse('order-list'),  # Sem o kwargs={'version': 'v1'}
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_order = Order.objects.get(user=user)
        self.assertEqual(created_order.user, user)
        self.assertEqual(created_order.product.first(), product)