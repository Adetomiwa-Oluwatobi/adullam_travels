from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Destination, Service, Testimonial, QuoteRequest, SiteContent


# ── AUTH ──────────────────────────────────────────────────────

def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard:home')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard:login')


# ── HOME ──────────────────────────────────────────────────────

@login_required(login_url='dashboard:login')
def dashboard_home(request):
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    ctx = {
        'total_quotes'     : QuoteRequest.objects.count(),
        'new_quotes'       : QuoteRequest.objects.filter(submitted_at__gte=week_ago).count(),
        'unread_quotes'    : QuoteRequest.objects.filter(viewed=False).count(),
        'total_destinations': Destination.objects.count(),
        'total_testimonials': Testimonial.objects.filter(active=True).count(),
        'total_services'   : Service.objects.filter(active=True).count(),
        'recent_quotes'    : QuoteRequest.objects.order_by('-submitted_at')[:5],
    }
    return render(request, 'dashboard/home.html', ctx)


# ── QUOTE REQUESTS ────────────────────────────────────────────

@login_required(login_url='dashboard:login')
def quotes_list(request):
    filter_by = request.GET.get('filter', 'all')
    qs = QuoteRequest.objects.all()
    if filter_by == 'unread':
        qs = qs.filter(viewed=False)
    elif filter_by == 'read':
        qs = qs.filter(viewed=True)
    ctx = {'quotes': qs, 'filter_by': filter_by,
           'unread_count': QuoteRequest.objects.filter(viewed=False).count()}
    return render(request, 'dashboard/quotes.html', ctx)


@login_required(login_url='dashboard:login')
def quote_detail(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)
    if not quote.viewed:
        quote.viewed = True
        quote.save(update_fields=['viewed'])
    return render(request, 'dashboard/quote_detail.html', {'quote': quote})


@login_required(login_url='dashboard:login')
def quote_delete(request, pk):
    quote = get_object_or_404(QuoteRequest, pk=pk)
    if request.method == 'POST':
        quote.delete()
        messages.success(request, 'Quote request deleted.')
        return redirect('dashboard:quotes')
    return render(request, 'dashboard/confirm_delete.html', {'object': quote, 'type': 'Quote Request', 'back': 'dashboard:quotes'})


# ── DESTINATIONS ──────────────────────────────────────────────

@login_required(login_url='dashboard:login')
def destinations_list(request):
    destinations = Destination.objects.all()
    return render(request, 'dashboard/destinations.html', {'destinations': destinations})


@login_required(login_url='dashboard:login')
def destination_add(request):
    if request.method == 'POST':
        Destination.objects.create(
            name=request.POST['name'],
            country=request.POST['country'],
            tagline=request.POST['tagline'],
            description=request.POST.get('description', ''),
            image_url=request.POST['image_url'],
            featured=request.POST.get('featured') == 'on',
            order=int(request.POST.get('order', 0)),
        )
        messages.success(request, f"Destination added successfully.")
        return redirect('dashboard:destinations')
    return render(request, 'dashboard/destination_form.html', {'action': 'Add', 'dest': None})


@login_required(login_url='dashboard:login')
def destination_edit(request, pk):
    dest = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        dest.name      = request.POST['name']
        dest.country   = request.POST['country']
        dest.tagline   = request.POST['tagline']
        dest.description = request.POST.get('description', '')
        dest.image_url = request.POST['image_url']
        dest.featured  = request.POST.get('featured') == 'on'
        dest.order     = int(request.POST.get('order', 0))
        dest.save()
        messages.success(request, 'Destination updated.')
        return redirect('dashboard:destinations')
    return render(request, 'dashboard/destination_form.html', {'action': 'Edit', 'dest': dest})


@login_required(login_url='dashboard:login')
def destination_delete(request, pk):
    dest = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        dest.delete()
        messages.success(request, 'Destination deleted.')
        return redirect('dashboard:destinations')
    return render(request, 'dashboard/confirm_delete.html', {'object': dest, 'type': 'Destination', 'back': 'dashboard:destinations'})


# ── TESTIMONIALS ──────────────────────────────────────────────

@login_required(login_url='dashboard:login')
def testimonials_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'dashboard/testimonials.html', {'testimonials': testimonials})


@login_required(login_url='dashboard:login')
def testimonial_add(request):
    if request.method == 'POST':
        Testimonial.objects.create(
            name=request.POST['name'],
            location=request.POST.get('location', ''),
            message=request.POST['message'],
            rating=int(request.POST.get('rating', 5)),
            avatar_url=request.POST.get('avatar_url', ''),
            active=request.POST.get('active') == 'on',
        )
        messages.success(request, 'Testimonial added.')
        return redirect('dashboard:testimonials')
    return render(request, 'dashboard/testimonial_form.html', {'action': 'Add', 'obj': None})


@login_required(login_url='dashboard:login')
def testimonial_edit(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        obj.name      = request.POST['name']
        obj.location  = request.POST.get('location', '')
        obj.message   = request.POST['message']
        obj.rating    = int(request.POST.get('rating', 5))
        obj.avatar_url= request.POST.get('avatar_url', '')
        obj.active    = request.POST.get('active') == 'on'
        obj.save()
        messages.success(request, 'Testimonial updated.')
        return redirect('dashboard:testimonials')
    return render(request, 'dashboard/testimonial_form.html', {'action': 'Edit', 'obj': obj})


@login_required(login_url='dashboard:login')
def testimonial_delete(request, pk):
    obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Testimonial deleted.')
        return redirect('dashboard:testimonials')
    return render(request, 'dashboard/confirm_delete.html', {'object': obj, 'type': 'Testimonial', 'back': 'dashboard:testimonials'})


# ── SERVICES ──────────────────────────────────────────────────

@login_required(login_url='dashboard:login')
def services_list(request):
    services = Service.objects.all()
    return render(request, 'dashboard/services.html', {'services': services})


@login_required(login_url='dashboard:login')
def service_edit(request, pk):
    obj = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        obj.title             = request.POST['title']
        obj.short_description = request.POST['short_description']
        obj.full_description  = request.POST['full_description']
        obj.icon              = request.POST.get('icon', 'fa-star')
        obj.order             = int(request.POST.get('order', 0))
        obj.active            = request.POST.get('active') == 'on'
        obj.save()
        messages.success(request, 'Service updated.')
        return redirect('dashboard:services')
    return render(request, 'dashboard/service_form.html', {'obj': obj})


# ── SITE CONTENT ──────────────────────────────────────────────

@login_required(login_url='dashboard:login')
def site_content(request):
    items = SiteContent.objects.all()
    if request.method == 'POST':
        for item in items:
            new_val = request.POST.get(f'content_{item.pk}', '').strip()
            if new_val != item.value:
                item.value = new_val
                item.save(update_fields=['value'])
        messages.success(request, 'Site content saved.')
        return redirect('dashboard:site_content')
    return render(request, 'dashboard/site_content.html', {'items': items})


# ── CONTEXT HELPER ────────────────────────────────────────────
# Monkey-patch unread_count into every dashboard response
from django.template.response import TemplateResponse as _TR
_orig_render = _TR.render

def _patched_render(self):
    if hasattr(self, 'context_data') and self.context_data is not None:
        if 'unread_count' not in self.context_data:
            try:
                self.context_data['unread_count'] = QuoteRequest.objects.filter(viewed=False).count()
            except Exception:
                pass
    return _orig_render(self)

_TR.render = _patched_render
