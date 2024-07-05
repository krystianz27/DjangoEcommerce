from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


# Registration form
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields["email"].required = True

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")

        if len(email) >= 350:
            raise forms.ValidationError("Email is too long")

        return email


class UpdateUserForm(forms.ModelForm):
    current_password = forms.CharField(
        label="Current Password", widget=forms.PasswordInput(), required=False
    )
    new_password1 = forms.CharField(
        label="New Password", widget=forms.PasswordInput(), required=False
    )
    new_password2 = forms.CharField(
        label="Confirm New Password", widget=forms.PasswordInput(), required=False
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].required = True
        self.fields["email"].required = True

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password1 = cleaned_data.get("new_password1")
        new_password2 = cleaned_data.get("new_password2")

        # Check if any password fields are filled
        if any([current_password, new_password1, new_password2]):
            # Ensure current password is provided if any new password is set
            if not current_password:
                self.add_error(
                    "current_password",
                    "Current password is required to change password.",
                )

            # Validate new passwords match
            if new_password1 != new_password2:
                self.add_error(
                    "new_password2", "The two new password fields must match."
                )

        return cleaned_data

    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email already exists")

        if len(email) >= 350:
            raise forms.ValidationError("Email is too long")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password1 = self.cleaned_data.get("new_password1")

        if new_password1:
            user.set_password(new_password1)
            if commit:
                user.save()
        return user


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
