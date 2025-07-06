from django.contrib import admin
from .models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """
    Admin view for the Country model.
    """
    list_display = ('name', 'code', 'currency_name', 'currency_code')
    search_fields = ('name', 'code', 'currency_code')