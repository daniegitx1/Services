import csv
from django.core.management.base import BaseCommand
from listings.models import Listing
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
file_path = os.path.join(BASE_DIR, 'exported_listings.csv')

class Command(BaseCommand):
    help = 'Export all listings to a CSV file'

    def handle(self, *args, **kwargs):
        file_path = 'exported_listings.csv'  # or use a full path

        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'type', 'category', 'post_title', 'summary', 'description',
                'client_name', 'phone_number', 'email', 'website',
                'start_date', 'duration', 'picture'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for listing in Listing.objects.all():
                writer.writerow({
                    'type': listing.type,
                    'category': listing.category.name if listing.category else '',
                    'post_title': listing.post_title,
                    'summary': listing.summary,
                    'description': listing.description,
                    'client_name': listing.client_name,
                    'phone_number': listing.phone_number,
                    'email': listing.email,
                    'website': listing.website,
                    'start_date': listing.start_date,
                    'duration': listing.duration,
                    'picture': listing.picture.name if listing.picture else ''
                })
        print("DEBUG: Writing to", file_path)

        self.stdout.write(self.style.SUCCESS(f'Exported listings to {file_path}'))
