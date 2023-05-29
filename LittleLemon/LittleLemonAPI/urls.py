from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItemView, basename='menue-items')
urlpatterns = router.urls