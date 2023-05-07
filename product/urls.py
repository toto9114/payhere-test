from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from product import views

router = DefaultRouter()
router.register('', views.ProductViewSets, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
