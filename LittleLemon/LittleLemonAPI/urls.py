from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItemView, basename='menue-items')
urlpatterns = router.urls + [
    path('groups/manager/users/', views.ManagerViews.as_view(), name='manager-list'),
    path('groups/manager/users/<int:userId>/', views.ManagerViews.as_view(), name='manager-detail'),
    path('groups/delivery-crew/users/', views.DeliveryCrewViews.as_view(), name='crew-list'),
    path('groups/delivery-crew/users/<int:userId>/', views.DeliveryCrewViews.as_view(), name='crew-detail')
]