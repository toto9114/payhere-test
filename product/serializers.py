from rest_framework import serializers
from product.models import Product
from utils.jamo import extract_chosung


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = ('id', 'created_at', 'updated_at', 'deleted_at')
        fields = ('id', 'category', 'price', 'cost', 'name', 'content', 'barcode', 'expire', 'size')

    def create(self, validated_data):
        jamo = extract_chosung(validated_data['name'])
        validated_data['name_jamo'] = jamo

        product = Product(
            **validated_data
        )
        product.save()
        return product

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            jamo = extract_chosung(validated_data['name'])
            validated_data['name_jamo'] = jamo

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
