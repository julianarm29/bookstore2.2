from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.schemas import get_schema_view
from django.http import HttpResponse

# Função simples de boas-vindas
def welcome(request):
    return HttpResponse("<h1>Welcome to the Bookstore API</h1>")

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('', welcome),  # Rota raiz, leva para a página de boas-vindas
    path('v1/orders/', include('order.urls')),  # Prefixo 'v1/' para pedidos
    path('v1/products/', include('product.urls')),  # Prefixo 'v1/' para produtos
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('docs/', get_schema_view(title='Bookstore API'))
]
