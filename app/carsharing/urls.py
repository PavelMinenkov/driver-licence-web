from django.urls import path

from .views import index, logout, request_driver_license

urlpatterns = [
    path('', index, name='carsharing-index'),
    path('logout', logout, name='carsharing-logout'),
    path('request_driver_license', request_driver_license, name='carsharing-request-driver-license')
]
