from django import forms

from .models import ShippingAddress


# class ShippingForm(forms.ModelForm):
#     class Meta:
#         model = ShippingAddress

#         fields = [
#             "full_name",
#             "email",
#             "address1",
#             # "address2",
#             "number",
#             "city",
#             "state",
#             "zipcode",
#         ]
#         exclude = ["user"]


class ShippingForm(forms.ModelForm):
    # phone_number = PhoneNumberField()
    # phone_number = PhoneNumberField(region="PL", widget=PhoneNumberPrefixWidget())

    class Meta:
        model = ShippingAddress
        fields = [
            "full_name",
            "email",
            "phone_number",
            "address1",
            "number",
            "city",
            "state",
            "zipcode",
        ]

        labels = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "address1": "Street Address",
            "number": "Number",
            "city": "City",
            "state": "State",
            "zipcode": "Zip Code",
        }

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Full Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email Address"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "address1": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Street Address"}
            ),
            "number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Number"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "state": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "State"}
            ),
            "zipcode": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Zip Code"}
            ),
        }
