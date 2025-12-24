from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # 'related_name' qo'shildi, chunki 'Profile_m' bilan to'qnashuv bor edi (default nomi 'profile' edi)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.TextField(blank=True, null=True)
    choices = [
        ('hunarmand', 'Hunarmand'),
        ('Mijoz', 'Mijoz'),
        ('collector', 'Collector'),
    ]
    profilecatygory = models.CharField(max_length=20, choices=choices, default='Mijoz')

    def __str__(self):
        return f"{self.user.username}'s profile"

class Profile_m(models.Model):
    # 'related_name' nomi 'profile' dan 'user_profile_m' ga o'zgartirildi, to'qnashuvni bartaraf etish uchun
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile_m')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

class Profile_h(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_h')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    experience = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    instagram = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s hunarmand profile"

class Profile_c(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_c')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    favorite_hunarmands = models.ManyToManyField(Profile_h, blank=True)
    instagram = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s collector profile"

class Catygory(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
        


class Product(models.Model):
    hunarmand = models.ForeignKey(Profile_h, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    mijoz = models.ForeignKey(Profile_m, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    collector = models.ForeignKey(Profile_c, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    catygory = models.ForeignKey(Catygory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"

class Zakaz(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='zakaz')
    mijoz = models.ForeignKey(Profile_m, on_delete=models.CASCADE, related_name='zakaz')
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField()
    image = models.ImageField(upload_to='zakaz_images/', blank=True, null=True)
    status_choices = [
        ('tayyorlanmoqda', 'Tayyorlanmoqda'),
        ("yo'lda", "Yo'lda"),
        ('yetkazib berildi', 'Yetkazib berildi'),
        ('bekor qilindi', 'Bekor qilindi'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='tayyorlanmoqda')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Zaказ #{self.id} for {self.product.name}"

class Product_col(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_col')
    collector = models.ForeignKey(Profile_c, on_delete=models.CASCADE, related_name='product_col')
    price = models.IntegerField()
    image = models.ImageField(upload_to='product_col_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Product_col #{self.id} for {self.product.name}"



class Product_col_images(models.Model):
    product_col = models.ForeignKey(Product_col, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_col_images/')
    def __str__(self):
        return f"Image for {self.product_col.product.name} collection"
