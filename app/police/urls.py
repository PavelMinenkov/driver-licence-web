from django.urls import path

from .views import index, logout, request_passport, request_driver_school_diploma, verify_face

urlpatterns = [
    path('', index, name='police-index'),
    path('request_passport', request_passport, name='police-request-passport'),
    path('request_driver_school_diploma', request_driver_school_diploma, name='police-request-driver-school-diploma'),
    path('logout', logout, name='police-logout'),
    path('verify', verify_face, name='police-verify-face')
]
