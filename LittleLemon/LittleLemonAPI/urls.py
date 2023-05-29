from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItemView, basename='menue-items')
urlpatterns = router.urls + [
    path('groups/manager/users/', views.ManagerViewSet.as_view(), name='manager-list'),
    path('groups/manager/users/<int:userId>/', views.ManagerViewSet.as_view(), name='manager-detail')
]