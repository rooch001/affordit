# core/admin.py
from django.contrib import admin

from .models import Profile, UserSubscription


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'monthly_income', 'hours_worked_weekly')


# core/admin.py

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    # CORRECTED: Use fields that exist on the UserSubscription model
    list_display = ('profile', 'service', 'plan_name', 'price', 'currency', 'added_on')
    # CORRECTED: The path to the category is now direct
    list_filter = ('service__category', 'currency')
