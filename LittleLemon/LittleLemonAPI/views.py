from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .serializers import MenuItemSerializer, ManagerSerializer, DeliveryCrewSerializer, CartSerializer, OrderSerializer, ManagerOrderSerializer
from .models import MenuItem, Cart, Order
from rest_framework.permissions import IsAuthenticated
from .custom_permissions import IsManager, is_manager_check, is_crew_check, is_customer_check
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.core.paginator import Paginator, EmptyPage
from rest_framework.decorators import api_view,throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class MenuItemView(ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['id', 'price', 'title', 'category__title']
    search_fields=['title', 'price', 'category__title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes.append(IsManager)

        return super(MenuItemView, self).get_permissions()


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def cart_view(request):
    if request.method == 'GET':
        author = Cart.objects.all()
        serialized_category = CartSerializer(author, many=True)
        return Response(serialized_category.data)
    elif request.method == 'POST':
        item = CartSerializer(data=request.data, context={'request': request})
        item.is_valid(raise_exception=True)
        item.save()
        return Response(item.data, status=status.HTTP_201_CREATED)
    else:
        Cart.objects.filter(user__id=request.user.id).delete()
        return Response({"message": "Cart is now empty"}, status=status.HTTP_200_OK)


class OrderListViews(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        orders = Order.objects.all()
        ordering = request.query_params.get('ordering')
        page = request.query_params.get('page', 1)
        perpage = request.query_params.get('perpage', 10)
        if is_customer_check(request):
            orders = orders.filter(user__id=request.user.id)
        elif is_crew_check(request):
            orders = orders.filter(delivery_crew__id=request.user.id)


        if ordering:
            ordering_fields = ordering.split(',')
            orders = orders.order_by(*ordering_fields)

        paginator = Paginator(orders, per_page=perpage)
        try:
            orders = paginator.page(number=page)
        except EmptyPage:
            orders = []

        serialized = OrderSerializer(orders, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not is_customer_check(request):
            return Response({"message": "Only Customers can access this"}, status=status.HTTP_403_FORBIDDEN)
        
        cart_items = Cart.objects.filter(user__id=request.user.id)
        if not cart_items:
            return Response({"message": "Your cart is empty"}, status=status.HTTP_200_OK)
        
        total = 0
        order = Order.objects.create(user=request.user, total=total)

        for cart_item in cart_items:
            order.order_items.create(
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            total += cart_item.price

        order.total = total
        order.save()   
        cart_items.delete()
        serialized = OrderSerializer(order)
        return Response(serialized.data, status=status.HTTP_200_OK)

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, pk):
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        if is_customer_check(request) and order.user != request.user:
            return Response({"message": "You are not allowed to access this order"}, status=status.HTTP_403_FORBIDDEN)
        elif is_crew_check(request) and order.delivery_crew != request.user:
            return Response({"message": "You are not allowed to access this order"}, status=status.HTTP_403_FORBIDDEN)

        serialized = OrderSerializer(order)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        if not is_manager_check(request):
            return Response({"message": "You are not allowed to access"}, status=status.HTTP_403_FORBIDDEN)
       
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"message": "Ordered Deleted"}, status=status.HTTP_200_OK)



    def patch(self, request, pk):
        if is_customer_check(request):
            return Response({"message": "You are not allowed to access"}, status=status.HTTP_403_FORBIDDEN)
       
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Response({"message": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

        if is_manager_check(request):
            item = ManagerOrderSerializer(data=request.data)
            item.is_valid(raise_exception=True)
            
            try:
               delivery_crew = User.objects.get(username=item.validated_data['username'])
            except User.DoesNotExist:
                return Response({"message": "Delivery Crew Not Found"}, status=status.HTTP_404_NOT_FOUND)

            if not delivery_crew.groups.filter(name='Delivery Crew').exists():
                return Response({"message": "The Selected user is not a delivery crew"}, status=status.HTTP_403_FORBIDDEN)

            order.delivery_crew = delivery_crew
            order.save()
            return Response({"message": "Deliver Crew Set"}, status=status.HTTP_200_OK)
        
        # Delivery cew
        if order.delivery_crew != request.user:
            return Response({"message": "You are not allowed to access this order"}, status=status.HTTP_403_FORBIDDEN)
        
        order.status = 1
        order.save()
        return Response({"message": "Ordered Delivered"}, status=status.HTTP_200_OK)


class ManagerViews(APIView):
    permission_classes = [IsAuthenticated, IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

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
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
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