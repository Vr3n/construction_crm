from django.shortcuts import render

# Create your views here.


def logout(request):
    render(request, "<h1>LOgout</h1>")


def login(request):
    render(request, "<h1>Login</h1>")


def register(request):
    render(request, "<h1>Register</h1>")
