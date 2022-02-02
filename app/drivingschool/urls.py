from django.urls import path

from .views import index, logout, request_passport

urlpatterns = [
    path('', index, name='drivingschool-index'),
    path('logout', logout, name='drivingschool-logout'),
    path('request_passport', request_passport, name='drivingschool-request-passport')
]
