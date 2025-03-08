from django.db import models
from datetime import date, timedelta
from django.core.exceptions import ValidationError


# Category model assumed to be defined above
class Category(models.Model):
    name = models.CharField(max_length=100)

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
    post_title = models.CharField(
        max_length=200,
        verbose_name="Post title or topic"
    )
    summary = models.CharField(
        max_length=300,
        verbose_name="Service or product"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    client_name = models.CharField(
        max_length=100,
        verbose_name="Your name / Company name"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Phone number"
    )
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to='listings/', blank=True, null=True)
    duration = models.PositiveIntegerField(default=1)  # Duration in months
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate required fields
        missing_fields = []
        for field in ['post_title', 'summary', 'client_name', 'phone_number']:
            if not getattr(self, field):
                missing_fields.append(field)
        if missing_fields:
            raise ValidationError({field: "This field is required." for field in missing_fields})

        # Word limit validations
        if self.post_title:
            if len(self.post_title.strip().split()) > 12:
                raise ValidationError({'post_title': "Post title must be 12 words or fewer."})

        if self.summary:
            if len(self.summary.strip().split()) > 20:
                raise ValidationError({'summary': "Summary must be 20 words or fewer."})

        if self.description:
            word_limit = 60 if self.type == 'standard' else 120
            if len(self.description.strip().split()) > word_limit:
                raise ValidationError({'description': f"Description must be {word_limit} words or fewer for this listing type."})

    def save(self, *args, **kwargs):
        # Auto-calculate end_date based on duration
        if self.start_date and self.duration:
            self.end_date = self.start_date + timedelta(days=30 * self.duration)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.post_title
