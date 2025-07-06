# scrapers/models.py
from django.db import models


class Service(models.Model):
    """
    Represents a subscription service (e.g., Netflix, Spotify).
    """
    CATEGORY_CHOICES = [
        ('Entertainment', 'Entertainment'),
        ('Productivity', 'Productivity'),
        ('Gaming', 'Gaming'),
        ('E-commerce', 'E-commerce'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100, unique=True)
    website = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
