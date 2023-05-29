from rest_framework import serializers
from .models import MenuItem
from .models import User

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class ManagerSerializer(serializers.Serializer):   
    username = serializers.CharField(max_length=255) 

class DeliveryCrewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)