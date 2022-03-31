from django.urls import path

from update_location.views import dashboard_view, set_location_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('<str:location>', set_location_view, name='set-location')
]
