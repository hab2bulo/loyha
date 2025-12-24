# app/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProductViewSet, CategoryViewSet, ProfileViewSet, OrderViewSet

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("categories", CategoryViewSet, basename="category")
router.register("profiles", ProfileViewSet, basename="profile")
router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),  # app ichidagi barcha API endpointlar shu yerda
]