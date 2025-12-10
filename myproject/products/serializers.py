from rest_framework import serializers
from .models import Product
from common.validators import validate_age

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        validate_age(user)
        return data
