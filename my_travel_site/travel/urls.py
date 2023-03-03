from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    # path('', index, name='home'),
    # path('departure/<int:departure_id>', show_departure, name='departure'),
    # path('departure/<slug:departure_slug>', show_departure, name='departure'),
    # path('tour/<int:tour_id>/', show_tour, name='tour'),
    # path('tour/<slug:tour_slug>/', show_tour, name='tour'),
    # path('addtour/', addtour, name='addtour'),
    # path('login/', login, name='login'),
    # path('about/', about, name='about'),
    # path('contact/', contact, name='contact'),
    path('', cache_page(60)(TravelHome.as_view()), name='home'),
    path('departure/<slug:departure_slug>', TravelDeparture.as_view(), name='departure'),
    path('tour/<slug:tour_slug>', ShowTour.as_view(), name='tour'),
    path('addtour/', AddTour.as_view(), name='addtour'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactFormView.as_view(), name='contact'),

]
