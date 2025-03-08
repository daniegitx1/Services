from django.contrib import admin
from .models import Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_title', 'client_name', 'category', 'type', 'start_date')
    list_display_links = ('id', 'post_title')
    list_filter = ('category', 'type', 'start_date')
    search_fields = ('post_title', 'client_name', 'summary')
    ordering = ('id',)  # Default sort by ID
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
