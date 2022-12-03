from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib import messages
from django.views.decorators.http import require_POST

from .forms import AdminLoginForm

# Create your views here.


def login(request):
    """
    Login view for admin
    """

    form = AdminLoginForm()
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            # remember = form.cleaned_data['remember']
            user = authenticate(request, username=username, password=password)
            if user:
                dj_login(request, user)
                # if remember:
                #     request.session.set_expiry(0)
                messages.success(request, "Login Successfull!")
                return redirect('home')
            else:
                messages.error(
                    request, "You don't have staff permissions to login, contact your administrator")
        else:
            messages.error(request, form.errors)
    return render(request, 'account/login.html', {'form': form})


@require_POST
def logout(request):
    """
    Logout view for admin
    """

    dj_logout(request)
    messages.success(request, "You have logged out successfully!")
    response = HttpResponseRedirect(reverse('login'))
    response['HX-Redirect'] = reverse('login')
    return response
