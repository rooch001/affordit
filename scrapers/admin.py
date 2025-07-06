# scrapers/admin.py
from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'website')
    list_filter = ('category',)
    search_fields = ('name',)
