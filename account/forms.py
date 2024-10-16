from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.hashers import check_password

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput


# Registration form
class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.fields["email"].required = True

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

        return username

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
        if any([new_password1, new_password2]):
            # Ensure current password is provided if any new password is set
            if not current_password:
                self.add_error(
                    "current_password",
                    "Current password is required to change password.",
                )
            else:
                # Validate current password
                user = self.instance  # Get the current user object
                if not check_password(current_password, user.password):
                    self.add_error(
                        "current_password",
                        "Current password is incorrect.",
                    )

            # Validate new passwords match
            if new_password1 and new_password2 and new_password1 != new_password2:
                self.add_error(
                    "new_password2", "The two new password fields must match."
                )

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Username already exists")

        return username

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
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = forms.CharField(widget=PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

        if username:
            cleaned_data["username"] = username.lower()

        return cleaned_data
