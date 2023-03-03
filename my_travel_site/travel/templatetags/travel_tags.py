from django import template
from travel.models import *


register = template.Library()


@register.simple_tag()
def get_departures():
    return Departure.objects.all()


@register.inclusion_tag('travel/list_departures.html')
def show_departures(dep_selected=0):
    deps = Departure.objects.all()
    return {"departures": deps, "departure_selected": dep_selected}