from django.contrib import admin

# Register your models here.
from .models import *


class TravelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'time_create', 'photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content') # поиск по ...
    list_editable = ('is_published',) # редактировать прямо из таблицы
    list_filter = ('is_published', 'time_create', 'time_update') # фильтровать по ...
    prepopulated_fields = {"slug": ("title",)} # чтобы в админке атоматически прописывался slag


class DepartureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Travel, TravelAdmin)
admin.site.register(Departure, DepartureAdmin)
