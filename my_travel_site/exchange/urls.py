from django.urls import path
from .views import *


urlpatterns = [
    #path('', TravelHome.as_view(), name='home'),
    path('', index, name='exchange_home')
]
