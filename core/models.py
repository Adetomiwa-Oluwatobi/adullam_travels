from django.db import models


class SiteContent(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.CharField(max_length=255, blank=True, help_text="Admin hint for what this field controls")

    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"
        ordering = ['key']

    def __str__(self):
        return f"{self.key}: {self.value[:60]}"

    @classmethod
    def get(cls, key, default=''):
        try:
            return cls.objects.get(key=key).value
        except cls.DoesNotExist:
            return default


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(help_text="Paste an image URL (Unsplash works great)")
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name}, {self.country}"


class Service(models.Model):
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200)
    full_description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class e.g. fa-passport")
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    avatar_url = models.URLField(blank=True, help_text="Optional profile photo URL")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}★"


class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    destination = models.CharField(max_length=200)
    travel_date = models.DateField(null=True, blank=True)
    travelers = models.PositiveSmallIntegerField(default=1)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Quote Request"
        verbose_name_plural = "Quote Requests"

    def __str__(self):
        return f"{self.name} -> {self.destination} ({self.submitted_at.strftime('%b %d, %Y')})"
