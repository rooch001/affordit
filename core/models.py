# core/models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from scrapers.models import Service


class Profile(models.Model):
    """
    Stores additional information for each user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hours_worked_weekly = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Use a signal to automatically create a Profile when a new User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# REMOVED the faulty save_user_profile signal that was here.

class UserSubscription(models.Model):
    """
    Links a user to a subscription they are paying for, with user-defined pricing.
    """
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscriptions')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Now links to Service

    # User-defined fields
    plan_name = models.CharField(max_length=100, default="Individual")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    billing_cycle = models.CharField(max_length=50, default='monthly')

    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.service.name}"

    class Meta:
        # User can't have the same service multiple times with the same plan name
        unique_together = ('profile', 'service', 'plan_name')
