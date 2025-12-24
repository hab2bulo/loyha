from django.shortcuts import render
from .models import User, Profile, Profile_m, Profile_h, Profile_c, Catygory, Product, ProductImage, Zakaz, Product_col, Product_col_images

def home(request):
    products = Product.objects.all()
    catygorys = Catygory.objects.all()
    Products = {
        'products': products,
        'categories': catygorys,
    }
    return render(request, 'home.html', Products)