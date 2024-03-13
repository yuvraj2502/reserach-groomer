from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone


# Banner 
class Banner(models.Model):
    title = models.TextField()
    show = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Banners'


# Contact us
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Contact Us'


# Custom User
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    contact_no = models.CharField(_("contact number"), max_length=15, blank=True, null=True)
    name = models.CharField(_("name"), max_length=255, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name or self.email
    
    class Meta:
        verbose_name_plural = 'Users'


# Faq
class Faq(models.Model):
    question = models.TextField(null=True)
    ans = models.TextField(null=True) 
    
    def __str__(self):
        return self.question  
    
    class Meta:
        verbose_name_plural = 'FAQs'


# Info topic
class InfoTopic(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='info_topics', null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Info Topics'


# Job request
class JobRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_no = models.CharField(max_length=10)
    resume =  models.FileField(upload_to='resume/')
    cover_letter = models.TextField()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Job Requests'


# Jobs
class Jobs(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    calling_no = models.IntegerField(null=True)
    description = models.TextField(null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Jobs'



class ProjectType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Project Types'


# Project 
class Project(models.Model):
    STATUS_CHOICES = [
        ('Not started', 'Not Started'),
        ('Started', 'Started'),
        ('In progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    technology = models.CharField(max_length=500, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL,null=True)
    requested_on = models.DateTimeField(auto_now_add=True, null=True)
    total_amount = models.IntegerField(null=True, blank=True, default=0)
    paid_amount = models.IntegerField(null=True, blank=True, verbose_name='amount received', default=0)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Not started')
    start_date = models.DateField(null=True, blank=True, verbose_name='start date')
    file_link = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return f'{self.requested_by.name}-{self.title}'
    
    class Meta:
        verbose_name_plural = 'Projects'


# Payment Record
class PaymentRecord(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f'{self.project.title} - {self.amount}'
    
    class Meta:
        verbose_name_plural = 'Payment Records'


# Project Reminder
class ProjectReminder(models.Model):
    sended_on = models.DateTimeField(default=timezone.now, editable=True)
    response = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reminders')

    def __str__(self):
        return f'{self.project.requested_by.name} - {self.sended_on}'
    
    class Meta:
        verbose_name_plural = 'Project Reminders'


# Quotation
class Quotation(models.Model):        
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    description = models.TextField()
    contact_no = models.CharField(max_length=10, null=True)
    technology = models.CharField(max_length=200, null=True)
    project_type = models.CharField(max_length=20, null=True)
    requested_on =  models.DateTimeField(default=timezone.now, editable=True)
    quotation_submitted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} - {self.title}'
    
    class Meta:
        verbose_name_plural = 'Quotations'


# Quotation response
class QuotationResponse(models.Model):
    sended_on = models.DateTimeField(default=timezone.now, editable=True)
    response = models.TextField()
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='responses')

    def __str__(self):
        return f'{self.quotation.name} - {self.sended_on}'
    
    class Meta:
        verbose_name_plural = 'Quotation Responses'


# Review (Fake review)
class Review(models.Model):
    name = models.CharField(max_length=100, null=True)
    review_content = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='review',default="review/def_reveiw.jpg", null=True,blank=True)
    profession = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Reviews'


# Team
class Team(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team')
    designation = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Teams'


