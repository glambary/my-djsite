from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='general_home')
]
