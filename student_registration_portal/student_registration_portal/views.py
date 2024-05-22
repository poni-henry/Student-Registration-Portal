from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import LoginForm
from django.http import HttpResponse

'''def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']  # Access authenticated user
            login(request, user)
            return redirect('home')  # Redirect to your desired home page after login
    else:
        form = LoginForm()
    return render(request, 'login.html', context={'form': form})'''

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a successful login page or dashboard
            return redirect('dashboard')  # Replace with your redirect URL
        else:
            # Handle invalid login attempt
            error_message = 'Invalid username or password'
    else:
        error_message = None
    context = {'error_message': error_message}
    return render(request, 'login.html', context)

def home(request):
    context = {}  # You can add context data for your homepage template here
    return render(request, 'home.html', context)

def programs_view(request):
    if request.method == 'POST':
        selected_department = request.POST.get('department')

        # Sample Program Data (Replace with your actual data retrieval logic)
        program_data = {
            'cs': ['Computer Science', 'Software Engineering', 'Data Science'],
            'it': ['Information Technology', 'Cybersecurity', 'Network Administration'],
        }

        # Access programs based on selected department
        programs = program_data.get(selected_department, [])  # Return empty list if department not found

        context = {'selected_department': selected_department, 'programs': programs}
        return render(request, 'programs.html', context)

    # Handle GET requests (optional)
    return render(request, 'home.html')  # Can redirect back to home page if needed

from django.shortcuts import render

'''def home(request):
    # No template rendering needed
    return HttpResponse('Welcome to the Student Registration Portal!')   # Example response'''

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect back to login page after logout
