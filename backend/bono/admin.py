from django.contrib import admin
from .models import *
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

admin.site.register(Bonos)
admin.site.register(GeneratedBono)
admin.site.register(User)

""" # Custom UserAdmin forms to include custom fields
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'  # Include all fields

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)  # Add your custom fields here if needed for creation

# Custom UserAdmin
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('username', 'phone', 'email', 'is_staff', 'role')  # Add custom fields here
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_superadmin', 'is_admin', 'is_user','added_by', 'is_deleted', 'status', 'photo')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )
     """