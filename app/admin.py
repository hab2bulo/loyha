from decimal import Decimal
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    Profile,
    Product,
    ProductImage,
    Order,
    CollectionItem,
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ()
    fields = ("image",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "category", "price", "is_active", "created_at", "image_tag")
    search_fields = ("name", "owner__user__username", "owner__user__email")
    list_filter = ("category", "is_active")
    inlines = [ProductImageInline]
    readonly_fields = ("created_at",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;"/>', obj.image.url)
        return "-"
    image_tag.short_description = "Image"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "experience", "rating", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("role",)
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("favorite_hunarmands",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "buyer", "quantity", "price_at_purchase", "total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("product__name", "buyer__user__username", "buyer__user__email")
    readonly_fields = ("total_price", "created_at")
    actions = ("mark_as_tayyorlanmoqda", "mark_as_yolda", "mark_as_yetkazib_berildi", "mark_as_bekor_qilindi")

    def mark_as_tayyorlanmoqda(self, request, queryset):
        updated = queryset.update(status="tayyorlanmoqda")
        self.message_user(request, f"{updated} ta buyurtma 'tayyorlanmoqda' holatiga o'zgartirildi.")
    mark_as_tayyorlanmoqda.short_description = "Belgilangan buyurtmalarni 'tayyorlanmoqda' ga o‘zgartirish"

    def mark_as_yolda(self, request, queryset):
        updated = queryset.update(status="yolda")
        self.message_user(request, f"{updated} ta buyurtma 'yolda' holatiga o'zgartirildi.")
    mark_as_yolda.short_description = "Belgilangan buyurtmalarni 'yolda' ga o‘zgartirish"

    def mark_as_yetkazib_berildi(self, request, queryset):
        updated = queryset.update(status="yetkazib_berildi")
        self.message_user(request, f"{updated} ta buyurtma 'yetkazib_berildi' holatiga o'zgartirildi.")
    mark_as_yetkazib_berildi.short_description = "Belgilangan buyurtmalarni 'yetkazib_berildi' ga o‘zgartirish"

    def mark_as_bekor_qilindi(self, request, queryset):
        updated = queryset.update(status="bekor_qilindi")
        self.message_user(request, f"{updated} ta buyurtma 'bekor_qilindi' holatiga o'zgartirildi.")
    mark_as_bekor_qilindi.short_description = "Belgilangan buyurtmalarni 'bekor_qilindi' ga o‘zgartirish"


@admin.register(CollectionItem)
class CollectionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "collector", "price", "created_at")
    search_fields = ("product__name", "collector__user__username")
    readonly_fields = ("created_at",)


# If any model was missed, register it plainly (fallback)
admin.site.site_header = "Loyha Admin"
admin.site.site_title = "Loyha Admin"
admin.site.index_title = "Boshqaruv paneli"
