from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']  # Access authenticated user
            login(request, user)
            return redirect('home')  # Redirect to your desired home page after login
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})

'''def home(request):
    context = {}  # You can add context data for your homepage template here
    return render(request, 'home.html', context)'''

def home(request):
    # No template rendering needed
    return HttpResponse('Welcome to the Student Registration Portal!')   # Example response

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect back to login page after logout
