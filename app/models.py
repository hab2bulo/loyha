from decimal import Decimal
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

USER = settings.AUTH_USER_MODEL

ROLE_HUNARMAND = 'hunarmand'
ROLE_MIJoz = 'mijoz'
ROLE_COLLECTOR = 'collector'
ROLE_CHOICES = [
    (ROLE_HUNARMAND, 'Hunarmand'),
    (ROLE_MIJoz, 'Mijoz'),
    (ROLE_COLLECTOR, 'Collector'),
]

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(USER, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MIJoz)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Hunarmand-specific optional fields
    skills = models.TextField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    # Socials (optional for all roles)
    instagram = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    whatsapp = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    # Collector-specific
    interests = models.TextField(blank=True, null=True)
    favorite_hunarmands = models.ManyToManyField(
        'self', blank=True, related_name='favorited_by',
        limit_choices_to={'role': ROLE_HUNARMAND}, symmetrical=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_hunarmand(self):
        return self.role == ROLE_HUNARMAND

    def is_mijoz(self):
        return self.role == ROLE_MIJoz

    def is_collector(self):
        return self.role == ROLE_COLLECTOR

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Product(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=260, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['owner']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"


ORDER_STATUS = [
    ('tayyorlanmoqda', 'Tayyorlanmoqda'),
    ("yolda", "Yo'lda"),
    ('yetkazib_berildi', 'Yetkazib berildi'),
    ('bekor_qilindi', 'Bekor qilindi'),
]

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    buyer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='orders')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    image = models.ImageField(upload_to='order_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='tayyorlanmoqda')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # agar price_at_purchase berilmagan bo'lsa, hozirgi product narxini olamiz
        if not self.price_at_purchase:
            self.price_at_purchase = self.product.price
        # totalni hisoblaymiz
        self.total_price = (self.price_at_purchase or Decimal('0.00')) * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} — {self.product.name} x{self.quantity}"


class CollectionItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='collection_items')
    collector = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collection_items')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    image = models.ImageField(upload_to='collection_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collection item #{self.id} for {self.product.name}"