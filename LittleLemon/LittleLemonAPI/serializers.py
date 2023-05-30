from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem, Category
from .models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']

    def get_order_items(self, obj):
        order_items = obj.order_items.all()
        return OrderItemSerializer(order_items, many=True).data


class ManagerOrderSerializer(serializers.Serializer):   
    username = serializers.CharField(max_length=255) 

class ManagerSerializer(serializers.Serializer):   
    username = serializers.CharField(max_length=255) 

class DeliveryCrewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)