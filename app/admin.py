from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "name", "is_staff", "is_active","last_login")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_('Personal info'), {"fields": ("name", "contact_no")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "name", "contact_no","password1", "password2", 
            )}
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email",)

    

admin.site.register(CustomUser, CustomUserAdmin)



class BaseAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            # If the user is not a superuser, remove the delete_selected action
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

@admin.register(Banner)
class BannerAdmin(BaseAdmin):
    list_display = ('title', 'show')
    list_filter = ('show',)
    search_fields = ('title',)

@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = ('name', 'email', 'message')
    search_fields = ('name', 'email')

@admin.register(Review)
class ReviewAdmin(BaseAdmin):
    list_display = ('name', 'review_content', 'display_image', 'profession')
    search_fields = ('name', 'review_content', 'profession')

    def display_image(self, obj):
        return format_html('<img src="{}" style="width:50px; height:50px;" />'.format(obj.image.url))

@admin.register(Faq)
class FaqAdmin(BaseAdmin):
    list_display = ('question', 'ans')
    search_fields = ('question',)

@admin.register(Jobs)
class JobsAdmin(BaseAdmin):
    list_display = ('name', 'location', 'calling_no',)
    search_fields = ('name', 'location', 'calling_no',)

@admin.register(InfoTopic)
class InfoTopicAdmin(BaseAdmin):
    list_display = ('name', 'display_image',)
    search_fields = ('name', )

    def display_image(self, obj):
        return format_html('<img src="{}" style="width:50px; height:50px;" />'.format(obj.image.url))

# @admin.register(Team)
# class TeamAdmin(BaseAdmin):
#     list_display = ('name', 'display_image', 'designation')
#     search_fields = ('name', 'designation')

#     def display_image(self, obj):
#         return format_html('<img src="{}" style="width:50px; height:50px;" />'.format(obj.image.url))

@admin.register(JobRequest)
class JobRequestAdmin(BaseAdmin):
    list_display = ('name', 'email', 'contact_no', 'display_resume', )
    search_fields = ('name', 'email',)

    def display_resume(self, obj):
        return format_html('<a href="{}" target="_blank">View Resume</a>'.format(obj.resume.url))



@admin.register(ProjectType)
class ProjectTypeAdmin(BaseAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(Project)
class ProjectAdmin(BaseAdmin):
    list_display = ('requested_by_name','title', 'status', )  # Add 'requested_by_name' to display the user name
    list_filter = ('status', 'start_date', 'requested_by__name')
    search_fields = ('requested_by__name', 'title', 'email', 'project_type__name')  # Adjusted search_fields
    date_hierarchy = 'start_date'

    def requested_by_name(self, obj):
        return obj.requested_by.name  # Assuming 'name' is the attribute of CustomUser model you want to display

    requested_by_name.short_description = 'Requested By'



@admin.register(Quotation)
class QuotationAdmin(BaseAdmin):
    list_display = ('name', 'title', 'email', 'description', 'quotation_submitted')
    search_fields = ('name', 'title', 'email', 'description')
    list_filter = ('quotation_submitted',)

@admin.register(PaymentRecord)
class PaymentAdmin(BaseAdmin):
    list_display = ('project', 'payment_date', 'amount', 'description')
    list_filter = ('project', 'payment_date')
    date_hierarchy = 'payment_date'
    search_fields = ('project__name', 'amount', 'description')



@admin.register(ProjectReminder)
class ProjectReminderAdmin(BaseAdmin):
    list_display = ('project', 'sended_on',)
    list_filter = ('project',)
    search_fields = ('project__name',)



@admin.register(QuotationResponse)
class QuotationResponseAdmin(BaseAdmin):
    list_display = ('quotation', 'sended_on',)
    list_filter = ('quotation',)

