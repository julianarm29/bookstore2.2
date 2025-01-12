from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from order.factories import UserFactory, OrderFactory
from product.factories import ProductFactory, CategoryFactory
from rest_framework.authtoken.models import Token
import json
from order.models import Order  # Adicionando a importação do modelo Order

class TestOrderViewSet(APITestCase):

    client = APIClient()

    def setUp(self):
        # Criando o usuário e o token de autenticação
        self.user = UserFactory()
        token = Token.objects.create(user=self.user)
        
        # Criando a categoria e o produto relacionados ao pedido
        self.category = CategoryFactory(title='tecnologia')
        self.product = ProductFactory(title='mouse', price=100, category=[self.category])
        
        # Criando o pedido (Order)
        self.order = OrderFactory(product=[self.product])

    def test_order(self):
        # Recuperando o token e configurando a autenticação
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Acessando a lista de pedidos
        response = self.client.get(
            reverse('order-list')  # Corrigido: Não há necessidade de passar 'version' aqui
        )

        # Verificando se o status é OK e validando os dados do pedido
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_data = json.loads(response.content)
        self.assertEqual(order_data['results'][0]['product'][0]['title'], self.product.title)

    def test_create_order(self):
        # Recuperando o token e configurando a autenticação
        token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        # Criando um novo usuário e produto para o pedido
        user = UserFactory()
        product = ProductFactory()

        # Dados para criar o pedido
        data = json.dumps({
            'products_id': [product.id],
            'user': user.id
        })

        # Enviando uma requisição POST para criar o pedido
        response = self.client.post(
            reverse('order-list'),  # Corrigido: Não há necessidade de passar 'version' aqui
            data=data,
            content_type='application/json'
        )

        # Verificando se o pedido foi criado com sucesso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Validando que o pedido foi salvo no banco de dados
        created_order = Order.objects.get(user=user)
        self.assertEqual(created_order.user, user)
        self.assertEqual(created_order.product.first(), product)
