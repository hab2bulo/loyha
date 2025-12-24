from decimal import Decimal
from rest_framework import serializers
from .models import Category, Profile, Product, ProductImage, Order, CollectionItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "product")


class ProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source="user.username")
    favorite_hunarmands = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Profile.objects.filter(role="hunarmand"), required=False
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "user_username",
            "role",
            "bio",
            "avatar",
            "skills",
            "portfolio",
            "experience",
            "rating",
            "instagram",
            "telegram",
            "whatsapp",
            "facebook",
            "youtube",
            "interests",
            "favorite_hunarmands",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "rating")


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = (
            "id",
            "owner",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "images",
            "is_active",
            "created_at",
        )
        read_only_fields = ("slug", "created_at", "owner")

    def create(self, validated_data):
        request = self.context.get("request")
        profile = getattr(request.user, "profile", None)
        if profile is None:
            raise serializers.ValidationError("User profile does not exist.")
        validated_data["owner"] = profile
        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.filter(is_active=True))
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "product",
            "buyer",
            "quantity",
            "price_at_purchase",
            "total_price",
            "image",
            "status",
            "created_at",
        )
        read_only_fields = ("total_price", "created_at", "status", "price_at_purchase")

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        product = validated_data["product"]
        price_snapshot = product.price
        validated_data["price_at_purchase"] = price_snapshot
        validated_data["total_price"] = (price_snapshot or Decimal("0.00")) * Decimal(validated_data["quantity"])
        profile = getattr(request.user, "profile", None)
        if profile is None:
            raise serializers.ValidationError("User profile does not exist.")
        validated_data["buyer"] = profile
        return super().create(validated_data)


class CollectionItemSerializer(serializers.ModelSerializer):
    collector = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CollectionItem
        fields = ("id", "product", "collector", "price", "image", "created_at")
        read_only_fields = ("created_at", "collector")

    def create(self, validated_data):
        request = self.context.get("request")
        profile = getattr(request.user, "profile", None)
        if profile is None:
            raise serializers.ValidationError("User profile does not exist.")
        validated_data["collector"] = profile
        return super().create(validated_data)