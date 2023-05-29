from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import MenuItemSerializer
from .models import MenuItem
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsManager

class MenuItemView(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes.append(IsManager)

        return super(MenuItemView, self).get_permissions()
