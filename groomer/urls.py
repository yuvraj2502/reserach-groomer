
from django.contrib import admin
from django.urls import path
# from . import views,user_login
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    
    path('admin/', admin.site.urls),

    path('export/',views.export, name='export'),

    path('export-payment-records/', views.export_payment_records, name='export_payment_records'),

    path('export-user-records/', views.export_user_records, name='export_user_records'),

    path('', views.index , name = 'index'),

    path('payment-record/<int:id>',views.payment_record, name='payment-record'),

    path('add-to-project/<int:user_id>/<int:quotation_id>',views.add_project,name='add-to-project'),

    path('payment-detail/<int:id>',views.payment_detail,name='payment-detail'),

    path('quotation-request',views.quotation_request,name='quotation-request'),

    path('about', views.about , name = 'about'),
    
    path('contact', views.contact , name ='contact'),

    path('faq', views.faq , name = 'faq'),

    path('logout',views.dologout,name="logout"),

    path('dashboard',views.dashboard,name='dashboard'),

    path('user-alldetail/<int:id>',views.user_alldetail,name='user-alldetail'),

    path('project-detail/<int:id>',views.project_detail,name='project-detail'),

    path('project-reminder/<int:id>',views.project_reminder,name='project-reminder'),

    path('quotation-detail/<int:user_id>/<int:quotation_id>',views.quotation_detail,name='quotation-detail'),
    
    # path('project-response',views.project_response,name='project-response'),
 
    path('quotation-response/<int:id>',views.quotation_response,name='quotation-response'),

    path('info_topic/<int:id>',views.info_topic,name='info_topic'),

    path('register',views.register,name='register'),

    path('verify-otp', views.verify_otp, name='verify_otp'),

    path('login',views.dologin,name='dologin'),
    
    path('logout',views.dologout,name='dologout'),

    path('jobs',views.jobs,name='jobs'),

    path('job-request',views.job_request,name='job-request'),

    path('user-dashboard',views.user_dashboard,name='user-dashboard'),

    path('forget-password',views.forget_password,name='forget_password'),

    path('reset_verify_otp',views.reset_verify_otp,name='reset_verify_otp'),

    path('project-registration',views.project_registration,name="project-registration"),

    path('all-quotations',views.all_quotations,name='all-quotations'),

    # Not needed now 
    # path('project-list/',views.project_list,name='project-list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)