import random
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from groomer import settings
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from .helpers import send_job_request_email, user_is_staff
from django.urls import reverse

# Set sender's email from Django settings
sender_email = settings.EMAIL_HOST_USER

# Excel Exporter Views
from django.http import HttpResponse
import pandas as pd


def export_payment_records(request):
    if not request.user.is_staff:
        return redirect('index')  # Assuming you have a 'home' URL name, change it accordingly.

    # Retrieve data from your model
    queryset = PaymentRecord.objects.all()

    # Create a list of dictionaries with the desired fields
    data = []

    for record in queryset:
        project_title = record.project.title if record.project else None
        project_type = record.project.project_type.name if record.project and record.project.project_type else None
        payment_date = record.payment_date
        amount = record.amount
        description = record.description

        if project_title and "outsource" in project_title.lower():
            continue

        data.append({
            'Project Type': project_type,
            'Project Title': project_title,
            'Payment Date': payment_date,
            'Amount': amount,
            'Description': description,
        })

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Convert datetime columns to string format without timezone
    df['Payment Date'] = df['Payment Date'].dt.strftime('%Y-%m-%d')

    # Set explicit data types for each column
    data_types = {
        'Project Type': 'object',    # Assuming project_type.title is a string
        'Project Title': 'object',   # Assuming title is a string
        'Payment Date': 'object',    # Converted to string format
        'Amount': 'int64',           # Assuming amount is an integer
        'Description': 'object',     # Assuming description is a string
    }

    df = df.astype(data_types)

    # Create a response with an Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Payment_records.xlsx"'

    try:
        # Make sure pandas and openpyxl are installed
        df.to_excel(response, index=False, engine='openpyxl')
    except ImportError:
        print("Pandas or openpyxl is not installed.")
    except Exception as e:
        print(f"Error generating Excel file: {e}")

    return response

def export_user_records(request):
    if not request.user.is_staff:
        return redirect('index')  # Assuming you have a 'home' URL name, change it accordingly.

    # Retrieve data from your model
    queryset = CustomUser.objects.exclude(is_staff=True)

    # Create a list of dictionaries with the desired fields
    data = []

    for record in queryset:

        name = record.name if record.name else None
        email = record.email if record.email else None
        contact_no = record.contact_no

        data.append({
            'Name': name ,
            'Email': email ,
            'Contact No.': contact_no,
        })

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Set explicit data types for each column
    data_types = {
        'Name': 'object',    # Assuming project_type.title is a string
        'Email': 'object',   # Assuming title is a string # Converted to string format
        'Contact No.': 'int64',           # Assuming amount is an integer
    }

    df = df.astype(data_types)

    # Create a response with an Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="User_records.xlsx"'

    try:
        # Make sure pandas and openpyxl are installed
        df.to_excel(response, index=False, engine='openpyxl')
    except ImportError:
        print("Pandas or openpyxl is not installed.")
    except Exception as e:
        print(f"Error generating Excel file: {e}")

    return response




def export(request):
    if not request.user.is_staff:
        return redirect('index')  
    
    return render(request, 'export.html')


# Index page
def index(request):
    banner = Banner.objects.filter(show=True).first()
    info_topics = InfoTopic.objects.all()
    faq = Faq.objects.all()
    review = Review.objects.all()
    context = {
        'banner': banner,
        'info_topics': info_topics,
        # 'teams':teams,
        'review':review,
        'faqs':faq,
    }
    return render(request, 'index.html', context)


def jobs(request):
    jobs = Jobs.objects.all()
    context = {
        'jobs':jobs,
    }
    
    return render(request,'jobs.html',context)

# About us page
def about(request):
    review = Review.objects.all()

    context = {
        'review':review
    }

    return render(request, 'about.html', context)

# Faq page
def faq(request):
    faq = Faq.objects.all()

    context = {
        'faqs': faq,
    }
    return render(request, 'faq.html', context)


# Contact us
def contact(request):
    info_topics = InfoTopic.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['message']

        c = Contact(name=name, email=email, message=msg)
        c.save()

        subject = "Thank You for Contacting Research Groomer"
        email_body = render_to_string('app/email_templates/contact_us.txt', {'name':name})

        # message = f'You got a contact request\nName: {name}\nEmail: {email}\nMessage: {msg}\n'
        
        # Mail to the Research Groomer
        # send_mail("Contact Request",message,sender_email,[sender_email],fail_silently=True)

        try:
            # Mail to the sender
            send_mail(subject, email_body ,sender_email, [email],fail_silently=True)
            messages.success(request,'Message send successfully')
            return redirect('contact')
        except:
            messages.error(request,'Oops something went wrong.')
            return redirect('contact')
        
    else:
        context = {
            'info_topics': info_topics,
        }
        return render(request, 'contact-us.html',context)


# Info topics
def info_topic(request,id):
    info_topic = InfoTopic.objects.filter(id=id).first()

    data = {
        'info_topic':info_topic,
    }
    return render(request,'info_topic.html',data)
    

# Job request
def job_request(request):
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full-name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            resume = request.FILES.get('resume')
            cover_letter = request.POST.get('cover_letter')

            send_job_request_email(full_name, email, phone, resume, cover_letter)
            job = JobRequest.objects.create(name=full_name,email=email,contact_no=phone,resume=resume,cover_letter=cover_letter)
            job.save()
            messages.success(request,'Data submitted Successfully')
            
            return redirect('job-request')

        except Exception as e :
            print("An error occurred in the job request - ",e)
            messages.error(request,'OOPS! Something went wrong')
            return redirect('job-request')
            
    return render(request,'jobform.html')

# Ḍo login
def dologin(request):
    if request.user.is_authenticated:
        return redirect('index') 

    next = request.GET.get('next')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('user-dashboard')
        else:
            messages.error(request,'Wrong email id and password')
            return redirect('dologin')

    if next:
        messages.info(request,'Please login first')
        return redirect('dologin')
    
    return render(request, 'login.html')



def user_profile(request):
    return render(request,'profile.html')


@login_required(login_url='dologin')
def project_registration(request):
    if request.method == "POST":
        try:
            title = request.POST.get("title")
            technology = request.POST.get("technology")
            description = request.POST.get("projectDescription")
            project_type_name = request.POST.get("projectType")

            # Check if any of the required variables is None
            if None in (title, technology, description, project_type_name):
                raise ValueError("One or more required variables are None")

            # Get the user from the request (assuming you are using Django's built-in user system)
            user = request.user

            # Fetch the ProjectType instance by name
            project_type = ProjectType.objects.filter(name=project_type_name).first()

            # Check if project_type is not None
            if project_type is not None:
                # Create and save the Project instance
                project = Project(requested_by=user, title=title, technology=technology, description=description, project_type=project_type)
                project.save()

                messages.success(request, 'Project added successfully')
                return redirect('user-dashboard')
            else:
                raise ValueError("ProjectType not found for the given name")

        except Exception as e:
            print(str(e))
            messages.error(request, 'OOPS! Something went wrong')
            return redirect('project-registration')
    else:
        project_types = ProjectType.objects.all()

        context = {
            'project_types': project_types,
        }
        return render(request, 'project_registration.html', context)
    
    
# all quotations
@user_passes_test(user_is_staff)
def all_quotations(request):
    quotations = Quotation.objects.all().order_by('requested_on')
    data = {
        'quotations':quotations,
        }
    return render(request, 'all-quotations.html',data)


# Owner Dashboard
@user_passes_test(user_is_staff)
def dashboard(request):
    users = CustomUser.objects.exclude(is_staff=True)
    data = {
        'users':users,
    }
    return render(request, 'owner-dashboard.html',data)


# User all details
@user_passes_test(user_is_staff)
def user_alldetail(request,id):
    user = CustomUser.objects.filter(id=id).first()

    quotations = Quotation.objects.filter(email=user.email)
    projects = Project.objects.filter(requested_by=user)

    data ={
        'user':user,
        'projects':projects,
        'quotations':quotations,
    }
    return render(request,'user-alldetail.html',data)
    

@user_passes_test(user_is_staff)
def project_detail(request,id):
    if request.method == "POST":
        total = request.POST.get('totalAmount')
        start_date = request.POST.get('start_date')
        status = request.POST.get('status')
        file_link = request.POST.get('file_link')

        project = Project.objects.filter(id=id).first()
        
        project.total_amount = total
        project.start_date = start_date
        project.status = status
        project.file_link = file_link

        project.save()

        messages.success(request,"Changes updated successfully")
        redirect_url = reverse('user-alldetail', kwargs={'id': project.requested_by.id})
        return redirect(redirect_url)
        
    else:
        project = Project.objects.filter(id=id).first()
        data = {
            'project':project,
            'id':id,
        }
        return render(request,'project-detail.html',data)



@user_passes_test(user_is_staff)
def payment_record(request,id):
    if request.method == "POST":
        payment_date = request.POST.get('payment_date')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        project = Project.objects.filter(id=id).first()
        amount = int(amount)        
            
        # Create and save the new PaymentRecord instance
        PaymentRecord.objects.create(
            project=project,
            payment_date=payment_date,
            amount=amount,
            description=description
        )

        messages.success(request,"Changes updated successfully")
        redirect_url = reverse('payment-record', kwargs={'id': project.id})
        return redirect(redirect_url)

    else:
        project = Project.objects.filter(id=id).first()

        payment_records = PaymentRecord.objects.filter(project=project)
        paid=0

        for i in payment_records:
            paid = paid + i.amount

        
        project.paid_amount = paid
        project.save()

        context = {
            'payment_records': payment_records,
            'project': project,
        }

        return render(request, 'payment-record.html', context)
    


@user_passes_test(user_is_staff)
def add_project(request,quotation_id,user_id):
    user = CustomUser.objects.filter(id=user_id).first()
    quotation = Quotation.objects.filter(id=quotation_id).first()
    project_type = ProjectType.objects.filter(name=quotation.project_type).first()

    project = Project.objects.create(requested_by=user,title=quotation.title,description=quotation.description,technology=quotation.technology,project_type=project_type,requested_on = quotation.requested_on)
    project.save()
    redirect_url = reverse('user-alldetail', kwargs={'id': user.id})
    messages.success(request,'Quotation is added to project Successfully')
    return redirect(redirect_url)


def payment_detail(request,id):
    project = Project.objects.filter(id=id).first()
    payments = PaymentRecord.objects.filter(project=project)

    context = {
        'payments':payments,
        'project':project,
    }
    return render(request,'payment-detail.html',context)

@user_passes_test(user_is_staff)
def quotation_detail(request,quotation_id,user_id):
    quotation = Quotation.objects.filter(id=quotation_id).first()
    history = QuotationResponse.objects.filter(quotation=quotation_id)
    user = CustomUser.objects.filter(id=user_id).first()
    context = {
        'quotation':quotation,
        'history':history,
        'user':user,
    }
    return render(request,'quotation-detail.html',context)

@user_passes_test(user_is_staff)
def project_reminder(request,id):
    if request.method == "POST":
        project = Project.objects.filter(id=id).first()
        title = project.title
        response = request.POST.get('send-response')
        user = CustomUser.objects.filter(id=project.requested_by.id).first()

        subject = 'Research Groomer - Payment Reminder'
        email_body = render_to_string('app/email_templates/project_reminder.txt', {'name':user.name,'technology':project.technology,'project_type':project.project_type,'title':title,'response':response})
        recipient_email = user.email

        try:
            send_mail(subject, email_body, sender_email, [recipient_email], fail_silently=False)
            reminder = ProjectReminder(response=response,project=project)
            reminder.save()
            messages.success(request,'Response send successfully')
            redirect_url = reverse('project-reminder', kwargs={'id': project.id})
            return redirect(redirect_url)
        except:
            messages.error(request,'OOPS! something went wrong')
            redirect_url = reverse('project-reminder', kwargs={'id': project.id})
            return redirect(redirect_url)
        
    else:
        project = Project.objects.filter(id=id).first()
        history = ProjectReminder.objects.filter(project=project)
        data = {
            'project':project,
            'history':history,
        }
        return render(request,'p_reminder.html',data)




def dologout(request):
    request.session.flush()
    logout(request)
    return redirect('index')



@user_passes_test(user_is_staff)
def quotation_response(request,id):
    if request.method == "POST":
        quotation = Quotation.objects.filter(id=id).first()
        response = request.POST.get('send-response')

        subject = 'Research Groomer - Quotation Response'
        email_body = render_to_string('app/email_templates/quotation_response.txt', {'name':quotation.name,'technology':quotation.technology,'project_type':quotation.project_type,'title':quotation.title,'response':response,'requested_on':quotation.requested_on})
        recipient_email = quotation.email
        try:
            send_mail(subject, email_body, sender_email, [recipient_email], fail_silently=False)
            response = QuotationResponse.objects.create(response=response,quotation=quotation)
            quotation.quotation_submitted = True
            quotation.save()
            messages.success(request,'Response send successfully')
            redirect_url = reverse('quotation-response', kwargs={'id': quotation.id})
            return redirect(redirect_url)
        except:
            messages.error(request,'OOPS! something went wrong')
            redirect_url = reverse('quotation-response', kwargs={'id': quotation.id})
            return redirect(redirect_url)
    else:
        quotation = Quotation.objects.filter(id=id).first()
        history = QuotationResponse.objects.filter(quotation=quotation)
        context = {
            'quotation':quotation,
            'history':history,
        }
        return render(request, 'quotation-response.html',context)
    



    

def quotation_request(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile_no = request.POST.get("mobile-no")
        title = request.POST.get("title")
        technology = request.POST.get("technology")
        description = request.POST.get("projectDescription")
        project_type = request.POST.get("projectType")

        if len(mobile_no) != 10:
            messages.error(request, 'Contact number should be exactly 10 digits.')
            return redirect('quotation-request')


        quotation = {
            'name':name,
            'email':email,
            'mobile_no':mobile_no,
            'title':title,
            'technology':technology,
            'description':description,
            'project_type':project_type,
        }

        mail_to_user = render_to_string('app/email_templates/quotation_request.txt', quotation)
            
        try:
            quotation = Quotation.objects.create(name=name,email=email,description=description,project_type=project_type,technology=technology,contact_no=mobile_no,title=title)
            quotation.save()
            messages.success(request,'Your data is submitted successfully')        
        except :
            messages.error(request,'OOPS! Something went wrong.Please fill the form once again')
            return redirect('quotation-request')
        
        # confirmation mail to user 
        send_mail(subject="Research Groomer - Quotation Confirmation",message=mail_to_user, from_email=settings.EMAIL_HOST_USER, recipient_list=[email], fail_silently=True)

        return redirect('quotation-request')
    
    else:
        project_types = ProjectType.objects.all()
        context = {
            'project_types':project_types,
        }
        return render(request, 'quotation-request.html',context)


def generate_otp():
    return ''.join(random.choice('0123456789') for _ in range(6))


def send_otp_email(recipient_email, otp,name):
    subject = 'Registration in Research Groomer'
    email_body = render_to_string('app/email_templates/otp_email.txt', {'name': name, 'otp': otp})
    sender_email = settings.EMAIL_HOST_USER
    send_mail(subject, email_body, sender_email, [
              recipient_email], fail_silently=False)


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        email = request.session.get('email')
        password = request.session.get('password')
        contact_no = request.session.get('contact_no')
        name = request.session.get('name')

        if user_otp == stored_otp:
            try:
                new_user = CustomUser.objects.create_user(
                email=email,name=name,contact_no=contact_no, password=password)
                new_user.save()

                messages.success(request,"Registration done successfully")
                return redirect('dologin')
            except:
                messages.error(request,'OOPS! Something went wrong. Please register')
                return redirect('register')
        else:
            messages.error(request,'Invalid OTP')
            return redirect('verify_otp')

    return render(request, 'verify_otp.html')



@login_required(login_url='dologin')
def user_dashboard(request):
    user = request.user
    projects = Project.objects.filter(requested_by=user)
    data={
        'projects':projects,
    }
    return render(request,'userdashboard.html',data)


def register(request):
    if request.user.is_authenticated:
            return redirect('index') 

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_no = request.POST.get('number')
        name = request.POST.get('name')

        if len(contact_no) != 10:
            messages.error(request, 'Contact number should be exactly 10 digits.')
            return redirect('register')

        user = CustomUser.objects.filter(email=email).exists()

        if user:
            messages.info(request,'Email already registered')
            return redirect('register')

        if email is not None and password is not None:
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email
            request.session['password'] = password
            request.session['contact_no']=contact_no
            request.session['name']=name

            try:
                send_otp_email(email, otp,name)
            except:
                messages.error(request,"OOPS! Some technical issue")
                return redirect('register')

            return redirect('verify_otp')

    return render(request, 'register.html')


def forget_password(request):

    if request.method=="POST":
        email = request.POST.get('email')

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            messages.info(request,'Email id is not registered')
            return redirect('forget_password')
        
        try:
            otp = generate_otp()
            subject = 'Reset Password'
            email_body = render_to_string('app/email_templates/reset_password.txt', {'otp': otp})
            sender_email = settings.EMAIL_HOST_USER
            send_mail(subject, email_body, sender_email, [email], fail_silently=False)
            request.session['stored_otp']=otp
            request.session['email']=email
            return redirect('reset_verify_otp')
        except:
            messages.error(request,"OOPS! Some technical issue")
            return redirect('forget_password')

    return render(request,'forget_password.html')


def reset_verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        password = request.POST.get('password')
        stored_otp = request.session.get('stored_otp')
        email = request.session.get('email')

        if entered_otp==stored_otp:
            user = CustomUser.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            messages.success(request,'Password changed successfully')
            return redirect('dologin')
        else:
            messages.info(request,'Invalid OTP')
            return redirect('reset_verify_otp')

    return render(request,'reset_password.html')