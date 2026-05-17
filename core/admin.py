from django.contrib import admin
from django.utils.html import format_html
from .models import SiteContent, Destination, Service, Testimonial, QuoteRequest

admin.site.site_header = "Adullam Travels Admin"
admin.site.site_title = "Adullam Travels"
admin.site.index_title = "Content Management Dashboard"


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ['key', 'value_preview', 'description']
    search_fields = ['key', 'value']

    def value_preview(self, obj):
        return obj.value[:80] + '...' if len(obj.value) > 80 else obj.value
    value_preview.short_description = 'Value'


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'tagline', 'featured', 'order', 'image_preview']
    list_editable = ['featured', 'order']
    list_filter = ['featured', 'country']
    search_fields = ['name', 'country', 'tagline']

    def image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;" />', obj.image_url)
        return "—"
    image_preview.short_description = 'Preview'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_description', 'icon', 'order', 'active']
    list_editable = ['order', 'active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'rating', 'active', 'created_at']
    list_editable = ['active']
    list_filter = ['rating', 'active']


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'destination', 'travel_date', 'travelers', 'submitted_at', 'viewed']
    list_filter = ['viewed', 'submitted_at']
    search_fields = ['name', 'email', 'destination']
    readonly_fields = ['name', 'email', 'phone', 'destination', 'travel_date', 'travelers', 'message', 'submitted_at']
    list_editable = ['viewed']

    def has_add_permission(self, request):
        return False
