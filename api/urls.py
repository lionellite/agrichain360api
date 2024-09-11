from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SensorDataViewSet, AlertViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sensordata', SensorDataViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
