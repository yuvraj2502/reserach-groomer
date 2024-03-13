from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from groomer import settings
from django.core.mail import EmailMessage


sender_email = settings.EMAIL_HOST_USER



def user_is_staff(user):
    return user.is_staff



def send_job_request_email(full_name, email, phone, resume, cover_letter):
    subject = "Job request"
    email_body = render_to_string('app/email_templates/jobs_admin.txt', {'full_name':full_name,'phone':phone,'email':email,'cover_letter':cover_letter})
    from_email = sender_email
    recipient_list = [sender_email] 
 
    email_message = EmailMessage(subject, email_body, from_email, recipient_list)

    email_message.attach(resume.name, resume.read(), resume.content_type)

    email_message.send(fail_silently=False)