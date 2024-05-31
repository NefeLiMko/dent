from rest_framework import serializers
from parsers.models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'

    def create(self, validated_data):
        instance , created = ProductModel.objects.get_or_create(name=validated_data['name'], articul=validated_data['articul'], price=validated_data['price'], site=validated_data['site'] )
        
        return instance