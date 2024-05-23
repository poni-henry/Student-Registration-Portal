from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

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

def signup_view(request):
    if request.method == 'POST':
        # Handle sign-up form submission
        pass
    else:
        return render(request, 'signup.html')

@login_required
def home(request):
    program_data = {
        'Computer Science': ['Bachelor of Science (BS) in Computer Science', 'Bachelor of Arts (BA) in Computer Science', 'Master of Science (MS) in Computer Science', 'Ph.D. in Computer Science'],
        'Information Technology': ['Bachelor of Science (BS) in Information Technology', 'Cybersecurity', 'Master of Science (MS) in Information Technology'],
    }

    context = {
        'cs_programs': program_data.get('Computer Science', []),
        'it_programs': program_data.get('Information Technology', []),
    }
    return render(request, 'home.html', context)

@login_required
def enroll(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        program = request.POST.get('program')
        year_of_study = request.POST.get('year_of_study')
        semester = request.POST.get('semester')
        context = {
            'department': department,
            'program': program,
            'year_of_study': year_of_study,
            'semester': semester,
        }
        return render(request, 'enroll.html', context)
    return redirect('home')

@login_required
def register_page(request, department=None, program=None, year_of_study=None, semester=None):
    context = {
        'department': department,
        'program': program,
        'year_of_study': year_of_study,
        'semester': semester,
    }
    return render(request, 'registration.html', context)

@login_required
def confirm_enrollment(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        program = request.POST.get('program')
        year_of_study = request.POST.get('year_of_study')
        semester = request.POST.get('semester')
        # Redirect to the registration page with necessary parameters
        return redirect('register_page', department=department, program=program, year_of_study=year_of_study, semester=semester)
    return redirect('home')  # Redirect to home if not a POST request

def generate_invoice(request, department, program, year_of_study, semester):
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Invoice content
    data = [
        ['Department', department],
        ['Program', program],
        ['Year of Study', str(year_of_study)],
        ['Semester', str(semester)],
        # Add more details as needed
    ]

    # Create a table for the invoice content
    table = Table(data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add table to the PDF document
    doc.build([table])

    # Rewind the buffer
    buffer.seek(0)

    # Create a response object with the PDF content
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response

def logout_view(request):
    logout(request)
    return redirect('login')
