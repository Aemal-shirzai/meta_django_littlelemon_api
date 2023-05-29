from rest_framework import serializers
from .models import MenuItem, Cart
from .models import User

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ['user', 'price']

    def get_price(self, obj):   
        return obj.get('quantity') * obj.get('unit_price')

    def create(self, validated_data):
        validated_data["price"] = self.get_price(validated_data)
        validated_data["user"] = self.context['request'].user
        return super().create(validated_data)

class ManagerSerializer(serializers.Serializer):   
    username = serializers.CharField(max_length=255) 

class DeliveryCrewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)