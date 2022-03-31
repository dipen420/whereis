from django.contrib import messages
from django.shortcuts import render, redirect

from users.forms import UserRegisterForm


def register_view(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)

        if register_form.is_valid():
            register_form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        register_form = UserRegisterForm()
    return render(request, 'users/register.html', {'register_form': register_form})
