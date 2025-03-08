from django import template

register = template.Library()

@register.filter
def get_category_listings(listings, category):
    return listings.filter(category=category)

