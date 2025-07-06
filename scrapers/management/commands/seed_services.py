# scrapers/management/commands/seed_services.py

from django.core.management.base import BaseCommand
from django.db import transaction

from scrapers.models import Service


class Command(BaseCommand):
    """
    A Django management command to seed the database with an initial list of subscription services.

    This command is idempotent, meaning it can be run multiple times without creating
    duplicate entries. It uses a predefined list of top services to populate the
    Service model.

    Usage: python manage.py seed_services
    """
    help = 'Seeds the database with an initial list of subscription services.'

    # The list of services from your research.
    # I've added a website URL for each, which is useful for our models.
    SERVICES_TO_ADD = [
        {"name": "Netflix", "website": "https://www.netflix.com"},
        {"name": "Amazon Prime", "website": "https://www.amazon.com/prime"},
        {"name": "YouTube Premium", "website": "https://www.youtube.com/premium"},
        {"name": "Spotify", "website": "https://www.spotify.com"},
        {"name": "Hulu", "website": "https://www.hulu.com"},
        {"name": "Paramount+", "website": "https://www.paramountplus.com"},
        {"name": "Max", "website": "https://www.max.com"},
        {"name": "Disney+", "website": "https://www.disneyplus.com"},
        {"name": "Amazon Music", "website": "https://music.amazon.com"},
        {"name": "Apple Music", "website": "https://www.apple.com/apple-music/"},
        {"name": "Peacock", "website": "https://www.peacocktv.com"},
        {"name": "Nintendo Switch Online", "website": "https://www.nintendo.com/switch/online-service/"},
        {"name": "Xbox Game Pass", "website": "https://www.xbox.com/game-pass"},
        {"name": "PlayStation Plus", "website": "https://www.playstation.com/ps-plus/"},
        {"name": "ESPN+", "website": "https://plus.espn.com"},
        {"name": "Chewy (Autoship)", "website": "https://www.chewy.com"},
        {"name": "Apple TV+", "website": "https://tv.apple.com"},
        {"name": "Starz", "website": "https://www.starz.com"},
        {"name": "AMC+", "website": "https://www.amcplus.com"},
        {"name": "Dollar Shave Club", "website": "https://www.dollarshaveclub.com"},
        {"name": "HelloFresh", "website": "https://www.hellofresh.com"},
        {"name": "Sling TV", "website": "https://www.sling.com"},
        {"name": "FuboTV", "website": "https://www.fubo.tv"},
        {"name": "Ipsy", "website": "https://www.ipsy.com"},
        {"name": "FabFitFun", "website": "https://fabfitfun.com"},
        {"name": "Bespoke Post", "website": "https://www.bespokepost.com"},
        {"name": "KiwiCo", "website": "https://www.kiwico.com"},
        {"name": "Universal Yums", "website": "https://www.universalyums.com"},
        {"name": "ButcherBox", "website": "https://www.butcherbox.com"},
        {"name": "Nvidia GeForce Now", "website": "https://www.nvidia.com/geforce-now/"},
        {"name": "EA Play", "website": "https://www.ea.com/ea-play"},
        {"name": "Ubisoft+", "website": "https://plus.ubisoft.com"},
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        """
        The main logic for the command.

        This method iterates through the list of services and creates them in the
        database if they don't already exist.
        """
        self.stdout.write(self.style.SUCCESS('Starting to seed the database with services...'))

        created_count = 0
        skipped_count = 0

        for service_data in self.SERVICES_TO_ADD:
            # get_or_create is an efficient and safe way to add data.
            # It checks if an object with the given parameters exists before creating it.
            # 'defaults' are used to provide additional fields if a new object is created.
            service, created = Service.objects.get_or_create(
                name=service_data["name"],
                defaults={'website': service_data["website"]}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  Successfully created Service: "{service.name}"'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'  Skipped, Service already exists: "{service.name}"'))
                skipped_count += 1

        self.stdout.write(self.style.SUCCESS('---------------------------------'))
        self.stdout.write(self.style.SUCCESS(
            f'Seeding complete. Created {created_count} new services. Skipped {skipped_count} existing services.'))
