from django import forms
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
# Register your models here.

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError("Passwords don't match")
    #     return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        # user.set_unusable_password()
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(BaseUserAdmin):

    add_form = UserCreationForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "is_faculty", "is_staff", "is_student"),
            },
        ),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_faculty',
                                            'is_student',"groups","user_permissions",)}),
       ( _("Personal info"), {"fields": ("first_name", "last_name",)}),
       (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        # ('Personal', {'fields': ('about',)}),
    )

    list_display = ['email', 'username', 'is_faculty', 'is_student','is_staff']
    search_fields = ['email', 'username']
    readonly_fields = ['id']
    filter_horizontal = (
    "groups",
    "user_permissions",
    )
