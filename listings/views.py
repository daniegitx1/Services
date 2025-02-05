from django.shortcuts import render, redirect
from .forms import ListingForm
from .models import Listing, Category
from datetime import date


from django.shortcuts import render
from .models import Listing, Category
from datetime import date

def service_list(request):
    today = date.today()
    selected_category = request.GET.get('category', 'Emergencies')  # Default to Emergencies

    # Get only listings that are within the valid start and end date range
    valid_listings = Listing.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    )

    # Get all categories that have at least one valid listing (for dropdown)
    all_valid_categories = Category.objects.filter(listing__in=valid_listings).distinct()

    # Ensure "Emergencies" and "Restaurants" appear first in the dropdown
    emergencies = all_valid_categories.filter(name="Emergencies")
    restaurants = all_valid_categories.filter(name="Restaurants")
    other_categories = all_valid_categories.exclude(name__in=["Emergencies", "Restaurants"]).order_by("name")

    # Combine categories: "Emergencies" → "Restaurants" → Other alphabetical categories
    categories = list(emergencies) + list(restaurants) + list(other_categories)

    # If a category is selected, filter the listings accordingly
    if selected_category != "All":
        valid_listings = valid_listings.filter(category__name=selected_category)

    return render(request, 'listings/service_list.html', {
        'listings': valid_listings.order_by('post_title'),
        'categories': categories,  # Pass all non-empty categories for dropdown
        'selected_category': selected_category,
    })


def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')  # Redirect to the listings page after submission
    else:
        form = ListingForm()

    return render(request, 'listings/add_listing.html', {'form': form})
