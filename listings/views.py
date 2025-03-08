from django.shortcuts import redirect, render
from django.db.models import Q, Count
from datetime import date
from .forms import ListingForm
from .models import Listing, Category

def service_list(request):
    today = date.today()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    sort_order = request.GET.get('sort')

    # All valid listings
    valid_listings = Listing.objects.filter(
        start_date__lte=today,
        end_date__gte=today
    )

    # Category list for sidebar
    all_categories = Category.objects.annotate(valid_count=Count(
        'listing',
        filter=Q(listing__start_date__lte=today, listing__end_date__gte=today)
    ))

    emergencies = all_categories.filter(name="Emergencies")
    restaurants = all_categories.filter(name="Restaurants")
    other_categories = all_categories.exclude(name__in=["Emergencies", "Restaurants"]).order_by("name")
    categories = list(emergencies) + list(restaurants) + list(other_categories)

    # Determine filtered listings
    if search_query:
        filtered_listings = valid_listings.filter(
            Q(post_title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    elif selected_category and selected_category != "All":
        filtered_listings = valid_listings.filter(category__name=selected_category)
    else:
        selected_category = "All"  # important!
        filtered_listings = valid_listings

    # Apply sorting
    if sort_order == "newest":
        listings = filtered_listings.order_by("-created_at")
    elif sort_order == "oldest":
        listings = filtered_listings.order_by("created_at")
    else:
        listings = filtered_listings.order_by("post_title")

    return render(request, 'listings/service_list.html', {
        'listings': listings,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_order': sort_order,
    })


def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ListingForm()

    return render(request, 'listings/add_listing.html', {'form': form})
