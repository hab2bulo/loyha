# views.py boshida
from .serializers import (
    CategorySerializer,
    ProductImageSerializer,
    ProfileSerializer,
    ProductSerializer,
    OrderSerializer,
    CollectionItemSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsHunarmand, IsCollector

# app/views.py (minimal stublar — makemigrations uchun yetarli)
from rest_framework import viewsets
from .models import Product, Category, Profile, Order
from .serializers import ProductSerializer, CategorySerializer, ProfileSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('product', 'buyer').all()
    serializer_class = OrderSerializer