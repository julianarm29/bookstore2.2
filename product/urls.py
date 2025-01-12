from django.urls import path, include
from django.http import HttpResponse
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from product import viewsets

router = routers.DefaultRouter()
router.register(r'product', viewsets.ProductViewSet, basename='product')
router.register(r'category', viewsets.CategoryViewSet, basename='category')

urlpatterns = [
    path('', lambda request: HttpResponse("API funcionando")),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]