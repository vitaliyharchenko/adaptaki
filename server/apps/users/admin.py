from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from rest_framework.authtoken.models import TokenProxy, Token

from .models import User


# https://www.django-rest-framework.org/api-guide/authentication/#with-django-admin
# TokenAdmin.raw_id_fields = ['user']
admin.site.unregister(TokenProxy)


class TokenAdmin(admin.StackedInline):
    model = Token


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["phone", "password", "first_name",
                  "last_name", "is_active", "is_staff"]


# Register your models here.
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", "first_name", "last_name",
                    "telegram_username", "date_joined", "class_of", "is_staff"]
    list_filter = ["is_staff"]
    readonly_fields = ['date_joined']
    inlines = [TokenAdmin]
    fieldsets = [
        (None, {"fields": ["phone", "password"]}),
        ("Персональная информация", {"fields": [
         "first_name", "last_name", "class_of"]}),
        ("Доступы", {"fields": ["is_staff", "is_active"]}),
        ("Телеграм", {"fields": ["telegram_id", "telegram_username"]}),
        ("Дополнительно", {"fields": ["date_joined"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["phone", 'first_name', 'last_name']
    ordering = ["phone", "date_joined"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
