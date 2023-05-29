from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .serializers import MenuItemSerializer, ManagerSerializer, DeliveryCrewSerializer
from .models import MenuItem
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsManager
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import APIView

class MenuItemView(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes.append(IsManager)

        return super(MenuItemView, self).get_permissions()

class ManagerViews(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = User.objects.filter(groups__name='Manager')
        serializer = ManagerSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(username=serializer.validated_data['username'])
        except User.DoesNotExist:
            return Response({"detail": "Invalid Username"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            manager_group = Group.objects.get(name='Manager')
        except Group.DoesNotExist:
            return Response({"detail": "Manager Group Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.groups.add(manager_group)
        user.save()
        return Response({"message": "user added to the manager group"}, status=status.HTTP_201_CREATED)

    def delete(self, request, userId=None):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            manager_group = Group.objects.get(name='Manager')
        except Group.DoesNotExist:
            return Response({"detail": "Manager Group Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(manager_group)
        user.save()
        return Response({"message": "user removed from the manager group"}, status=status.HTTP_200_OK)

class DeliveryCrewViews(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        queryset = User.objects.filter(groups__name='Delivery Crew')
        serializer = DeliveryCrewSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DeliveryCrewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = User.objects.get(username=serializer.validated_data['username'])
        except User.DoesNotExist:
            return Response({"detail": "Invalid Username"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            crew_group = Group.objects.get(name='Delivery Crew')
        except Group.DoesNotExist:
            return Response({"detail": "Delivery Crew Group Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.groups.add(crew_group)
        user.save()
        return Response({"message": "user added to the delivery crew group"}, status=status.HTTP_201_CREATED)

    def delete(self, request, userId=None):
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            return Response({"detail": "User Not Found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            crew_group = Group.objects.get(name='Delivery Crew')
        except Group.DoesNotExist:
            return Response({"detail": "Delivery Crew Group Not Found"}, status=status.HTTP_404_NOT_FOUND)
        
        user.groups.remove(crew_group)
        user.save()
        return Response({"message": "user removed from the delivery crew group"}, status=status.HTTP_200_OK)