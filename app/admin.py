from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Profile_m, Profile_h, Profile_c, Catygory, Product, ProductImage, Zakaz, Product_col, Product_col_images

admin.site.register(Profile)
admin.site.register(Profile_m)
admin.site.register(Profile_h)
admin.site.register(Profile_c)
admin.site.register(Catygory)
admin.site.register(Product)
admin.site.unregister(User)
admin.site.register(ProductImage)
admin.site.register(Zakaz)
admin.site.register(Product_col)
admin.site.register(Product_col_images)