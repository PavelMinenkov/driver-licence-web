from django.urls import path

from .views import index, check_health

urlpatterns = [
    path('', index, name='index'),
    path('check_health', check_health, name='check-health')
]
