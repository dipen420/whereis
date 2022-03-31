from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from update_location.models import CurrentLocation
from update_location.utils import get_locations


@login_required
def dashboard_view(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        location = request.POST.get('location')
        location_data = get_locations(location=location.upper(), country=country.upper())
        return render(request, 'update_location/dashboard.html', {'locations': location_data})
    return render(request, 'update_location/dashboard.html')


@login_required
def set_location_view(request, location):
    current_location, created = CurrentLocation.objects.get_or_create(user=request.user, location=location)

    if not created:
        current_location.location = location
        current_location.save()

    messages.success(request, f'Your location is updated')
    return redirect('dashboard')
