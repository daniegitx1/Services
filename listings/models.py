from django.db import models

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Listing Model
class Listing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Links to Category
    post_title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to='listings/', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title
