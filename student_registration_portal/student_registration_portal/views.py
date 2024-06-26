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
from django.contrib.auth.forms import UserCreationForm
from .models import Student  # Import the Student model

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page or another page after successful signup
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

    return HttpResponse("Unhandled request method", status=400)


@login_required
def home(request):
    program_data = {
        'Computer Science': ['','Diploma in Computer Science', 'Bachelor of Science (BS) in Computer Science', 'Master of Science (MS) in Computer Science'],
        'Information Technology': ['','Diploma in Information Technology','Bachelor of Science (BS) in Information Technology', 'Bachelor of Science (BS) in Cybersecurity', 'Master of Science (MS) in Information Technology'],
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
    if request.method == 'POST':
        # Extract form data
        student_name = request.POST.get('student_name')
        registration_number = request.POST.get('registration_number')
        student_index_number = request.POST.get('student_index_number')
        contact_no = request.POST.get('contact_no')
        state = request.POST.get('state')
        county = request.POST.get('county')
        next_of_kin = request.POST.get('next_of_kin')
        next_of_kin_contact = request.POST.get('next_of_kin_contact')
        gender = request.POST.get('gender')
        admission = request.POST.get('admission')
        date_of_birth = request.POST.get('date_of_birth')

        # Create a new student instance and save it to the database
        student = Student(
            student_name=student_name,
            registration_number=registration_number,
            student_index_number=student_index_number,
            contact_no=contact_no,
            state=state,
            county=county,
            next_of_kin=next_of_kin,
            next_of_kin_contact=next_of_kin_contact,
            gender=gender,
            admission=admission,
            date_of_birth=date_of_birth
        )
        student.save()

        # Generate the invoice PDF
        invoice = generate_invoice(request, department, program, year_of_study, semester, student_name, registration_number, student_index_number, contact_no, state, county, next_of_kin, next_of_kin_contact, gender, admission, date_of_birth)
        return invoice

    # If it's a GET request, render the registration page as before
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

def generate_invoice(request, department, program, year_of_study, semester,student_name,registration_number,student_index_number,contact_no,state,county,next_of_kin,next_of_kin_contact,gender, admission,date_of_birth):
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
        ['Student Name', student_name],
        ['Registration Number', str(registration_number)],
        ['Student Index Number', str(student_index_number)],
        ['Contact Number', str(contact_no)],
        ['State', state],
        ['County',county],
        ['Next of Kin',next_of_kin],
        ['Next of Kin Contact',str(next_of_kin_contact)],
        ['Gender',gender],
        ['Admission',admission],
        ['Date of Birth',str(date_of_birth)],
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
