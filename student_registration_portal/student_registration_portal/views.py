from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after successful login
        else:
            error_message = 'Invalid username or password'
    return render(request, 'login.html', {'form': form, 'error_message': error_message})

@login_required
def home(request):
    program_data = {
        'cs': ['Bachelor of Science (BS) in Computer Science', 'Bachelor of Arts (BA) in Computer Science', 'Master of Science (MS) in Computer Science', 'Ph.D. in Computer Science'],
        'it': ['Bachelor of Science (BS) in Information Technology', 'Cybersecurity', 'Master of Science (MS) in Information Technology'],
    }

    context = {
        'cs_programs': program_data.get('cs', []),
        'it_programs': program_data.get('it', []),
    }
    return render(request, 'home.html', context)

@login_required
def enroll(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        program = request.POST.get('program')
        context = {
            'department': department,
            'program': program,
        }
        return render(request, 'enroll.html', context)
    return redirect('home')

@login_required
def confirm_enrollment(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        program = request.POST.get('program')
        # Add logic to save enrollment details
        # Redirect to a success page or back to home
        return redirect('home')
    return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('login')
