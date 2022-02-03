from django.urls import path

from .views import index, logout, verify_face

urlpatterns = [
    path('', index, name='police-index'),
    path('logout', logout, name='police-logout'),
    path('verify', verify_face, name='police-verify-face')
]
