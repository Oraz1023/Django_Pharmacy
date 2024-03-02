import io
from rest_framework import serializers

from .models import *

"""
Создание сериализаторов
"""
class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

        def create(self,validated_data):
            return Product.objects.create(**validated_data)

        def update(self,instance,validated_data):
            instance.__dict__.update(**validated_data)
            instance.save()
            return instance

        def delete(self, instance):
            instance.delete()

        def to_representation(self, instance):
            representation = super().to_representation(instance)
            # Дополнительные преобразования данных, если необходимо
            representation['additional_field'] = 'additional_value'
            return representation
            # instance.title = validated_data.get('title', instance.title)
            # instance.count = validated_data.get('count', instance.count)
            # instance.price = validated_data.get('price', instance.price)
            # instance.product_code = validated_data.get('product_code', instance.product_code)
            # instance.manufacturer = validated_data.get('manufacturer', instance.manufacturer)
            # instance.promotion = validated_data.get('promotion', instance.promotion)
            # instance.catalog = validated_data.get('catalog', instance.catalog)
            # instance.category = validated_data.get('category', instance.category)
            # instance.pop_brand = validated_data.get('pop_brand', instance.pop_brand)
            # instance.description = validated_data.get('description', instance.description)
            # instance.photo = validated_data.get('photo',instance.photo)
            # instance.save()
            # return instance



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class HealthBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Health_blog
        fields = '__all__'

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal_account
        fields = "__all__"

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = "__all__"


class MonthlyPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyPromotion
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PopularBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popular_brand
        fields = "__all__"


class PersonalAccountSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Personal_account
        fields = "__all__"