import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from listings.models import Listing, Category
from django.conf import settings

class Command(BaseCommand):
    help = 'Import listings from CSV file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['file']
        if not csv_file or not os.path.isfile(csv_file):
            self.stderr.write(self.style.ERROR("Valid --file path is required."))
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            imported = 0
            skipped = 0

            for row in reader:
                try:
                    # Get or create category
                    category_name = row.get('category', '').strip()
                    category, _ = Category.objects.get_or_create(name=category_name)

                    # Parse dates and duration
                    start_date = datetime.strptime(row['start_date'], '%Y/%m/%d').date()
                    duration = int(row['duration']) if row['duration'] else 1

                    # Prepare Listing
                    listing = Listing(
                        type=row.get('type', 'standard'),
                        category=category,
                        post_title=row['post_title'].strip(),
                        summary=row['summary'].strip(),
                        description=row['description'].strip(),
                        client_name=row['client_name'].strip(),
                        phone_number=row['phone_number'].strip(),
                        email=row.get('email', '').strip() or None,
                        website=row.get('website', '').strip() or None,
                        start_date=start_date,
                        duration=duration
                    )

                    # Attach image if available
                    picture_name = row.get('picture', '').strip()
                    if picture_name:
                        full_path = os.path.join(settings.MEDIA_ROOT, 'listings', picture_name)
                        if os.path.exists(full_path):
                            listing.picture.name = f'listings/{picture_name}'

                    listing.full_clean()  # Validate
                    listing.save()
                    imported += 1

                except Exception as e:
                    self.stderr.write(f"Skipping row due to error: {e}")
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(f"Imported: {imported}, Skipped: {skipped}"))
