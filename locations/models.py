from django.db import models


class Country(models.Model):
    """
    Represents a country with its currency information.
    """
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True, help_text="ISO 3166-1 alpha-2 country code")
    currency_name = models.CharField(max_length=50)
    currency_code = models.CharField(max_length=3)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']