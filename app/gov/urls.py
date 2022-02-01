from django.urls import path

from .views import index, logout

urlpatterns = [
    path('', index, name='gov-index'),
    path('logout', logout, name='gov-logout')
]
