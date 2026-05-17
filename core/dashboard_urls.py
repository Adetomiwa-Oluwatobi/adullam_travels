from django.urls import path
from . import dashboard_views as v

app_name = 'dashboard'

urlpatterns = [
    path('',                          v.dashboard_home,      name='home'),
    path('login/',                    v.dashboard_login,     name='login'),
    path('logout/',                   v.dashboard_logout,    name='logout'),

    path('quotes/',                   v.quotes_list,         name='quotes'),
    path('quotes/<int:pk>/',          v.quote_detail,        name='quote_detail'),
    path('quotes/<int:pk>/delete/',   v.quote_delete,        name='quote_delete'),

    path('destinations/',             v.destinations_list,   name='destinations'),
    path('destinations/add/',         v.destination_add,     name='destination_add'),
    path('destinations/<int:pk>/edit/',   v.destination_edit,   name='destination_edit'),
    path('destinations/<int:pk>/delete/', v.destination_delete, name='destination_delete'),

    path('testimonials/',             v.testimonials_list,   name='testimonials'),
    path('testimonials/add/',         v.testimonial_add,     name='testimonial_add'),
    path('testimonials/<int:pk>/edit/',   v.testimonial_edit,   name='testimonial_edit'),
    path('testimonials/<int:pk>/delete/', v.testimonial_delete, name='testimonial_delete'),

    path('services/',                 v.services_list,       name='services'),
    path('services/<int:pk>/edit/',   v.service_edit,        name='service_edit'),

    path('content/',                  v.site_content,        name='site_content'),
]
