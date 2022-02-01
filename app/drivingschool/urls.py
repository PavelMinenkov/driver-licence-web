from django.urls import path

from .views import index, logout

urlpatterns = [
    path('', index, name='drivingschool-index'),
    path('logout', logout, name='drivingschool-logout')
]
