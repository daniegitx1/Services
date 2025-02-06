from django.db import models
from datetime import date, timedelta

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Listing Model
class Listing(models.Model):
    LISTING_TYPES = [
        ('standard', 'Standard Listing'),
        ('full', 'Full Listing'),
    ]

    type = models.CharField(max_length=10, choices=LISTING_TYPES, default='standard')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to='listings/', blank=True, null=True)
    duration = models.PositiveIntegerField(default=1)  # New field for duration in months
    start_date = models.DateField(default=date.today)  # Auto-set to today's date
    end_date = models.DateField(blank=True, null=True)  # Auto-calculated

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-calculate the end date based on duration
        if self.start_date and self.duration:
            self.end_date = self.start_date + timedelta(days=30 * self.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.post_title