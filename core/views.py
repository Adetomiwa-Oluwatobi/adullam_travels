from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import SiteContent, Destination, Service, Testimonial, QuoteRequest
from urllib.parse import quote


def get_site_context():
    content_keys = SiteContent.objects.all()
    ctx = {item.key: item.value for item in content_keys}
    return ctx


def home(request):
    ctx = get_site_context()
    ctx['featured_destinations'] = Destination.objects.filter(featured=True)[:6]
    ctx['services'] = Service.objects.filter(active=True)[:6]
    ctx['testimonials'] = Testimonial.objects.filter(active=True)[:6]
    return render(request, 'core/home.html', ctx)


def services(request):
    ctx = get_site_context()
    ctx['services'] = Service.objects.filter(active=True)
    return render(request, 'core/services.html', ctx)


def destinations(request):
    ctx = get_site_context()
    ctx['destinations'] = Destination.objects.all()
    return render(request, 'core/destinations.html', ctx)


def about(request):
    ctx = get_site_context()
    return render(request, 'core/about.html', ctx)


def contact(request):
    ctx = get_site_context()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        destination = request.POST.get('destination', '').strip()
        travel_date_str = request.POST.get('travel_date', '').strip()
        travelers = request.POST.get('travelers', 1)
        message_text = request.POST.get('message', '').strip()

        travel_date = None
        if travel_date_str:
            try:
                from datetime import date
                travel_date = date.fromisoformat(travel_date_str)
            except ValueError:
                pass

        QuoteRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            destination=destination,
            travel_date=travel_date,
            travelers=travelers,
            message=message_text,
        )

        ig_message = (
            f"Hi Adullam Travels! My name is {name}. "
            f"I'm interested in travelling to {destination}. "
            f"Travel date: {travel_date_str or 'TBD'}. "
            f"Travelers: {travelers}. "
            f"Message: {message_text}"
        )
        ig_url = f"https://ig.me/m/adullamtravels?text={quote(ig_message)}"
        ctx['ig_redirect'] = ig_url
        ctx['submitted'] = True
        messages.success(request, 'Your request has been received! Click below to continue on Instagram.')
        return render(request, 'core/contact.html', ctx)

    return render(request, 'core/contact.html', ctx)
