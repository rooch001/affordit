# locations/management/commands/seed_countries.py
from django.core.management.base import BaseCommand
from django.db import transaction
from locations.models import Country

class Command(BaseCommand):
    help = 'Seeds the database with a list of countries and currencies.'

    # A comprehensive list of countries and their currencies
    COUNTRIES_DATA = [
        {'code': 'US', 'name': 'USA', 'currency_name': 'US Dollar', 'currency_code': 'USD'},
        {'code': 'CA', 'name': 'Canada', 'currency_name': 'Canadian Dollar', 'currency_code': 'CAD'},
        {'code': 'IN', 'name': 'India', 'currency_name': 'Indian Rupee', 'currency_code': 'INR'},
        {'code': 'GB', 'name': 'UK', 'currency_name': 'Pound Sterling', 'currency_code': 'GBP'},
        {'code': 'AU', 'name': 'Australia', 'currency_name': 'Australian Dollar', 'currency_code': 'AUD'},
        {'code': 'DE', 'name': 'Germany', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'FR', 'name': 'France', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'ES', 'name': 'Spain', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'IT', 'name': 'Italy', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'JP', 'name': 'Japan', 'currency_name': 'Japanese Yen', 'currency_code': 'JPY'},
        {'code': 'BR', 'name': 'Brazil', 'currency_name': 'Brazilian Real', 'currency_code': 'BRL'},
        {'code': 'MX', 'name': 'Mexico', 'currency_name': 'Mexican Peso', 'currency_code': 'MXN'},
        {'code': 'AR', 'name': 'Argentina', 'currency_name': 'Argentine Peso', 'currency_code': 'ARS'},
        {'code': 'NL', 'name': 'Netherlands', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'SE', 'name': 'Sweden', 'currency_name': 'Swedish Krona', 'currency_code': 'SEK'},
        {'code': 'NO', 'name': 'Norway', 'currency_name': 'Norwegian Krone', 'currency_code': 'NOK'},
        {'code': 'DK', 'name': 'Denmark', 'currency_name': 'Danish Krone', 'currency_code': 'DKK'},
        {'code': 'FI', 'name': 'Finland', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'PL', 'name': 'Poland', 'currency_name': 'Polish Zloty', 'currency_code': 'PLN'},
        {'code': 'IE', 'name': 'Ireland', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'CH', 'name': 'Switzerland', 'currency_name': 'Swiss Franc', 'currency_code': 'CHF'},
        {'code': 'AT', 'name': 'Austria', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'BE', 'name': 'Belgium', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'PT', 'name': 'Portugal', 'currency_name': 'Euro', 'currency_code': 'EUR'},
        {'code': 'NZ', 'name': 'New Zealand', 'currency_name': 'New Zealand Dollar', 'currency_code': 'NZD'},
        {'code': 'SG', 'name': 'Singapore', 'currency_name': 'Singapore Dollar', 'currency_code': 'SGD'},
        {'code': 'HK', 'name': 'Hong Kong', 'currency_name': 'Hong Kong Dollar', 'currency_code': 'HKD'},
        {'code': 'TR', 'name': 'Turkey', 'currency_name': 'Turkish Lira', 'currency_code': 'TRY'},
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding countries into the database...'))
        created_count = 0
        for country_data in self.COUNTRIES_DATA:
            _, created = Country.objects.get_or_create(
                code=country_data['code'],
                defaults={
                    'name': country_data['name'],
                    'currency_name': country_data['currency_name'],
                    'currency_code': country_data['currency_code']
                }
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Seeding complete. Added {created_count} new countries.'))