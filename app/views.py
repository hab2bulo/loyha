from django.shortcuts import render
from .models import  Profile, Product, Category, Order, CollectionItem
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')