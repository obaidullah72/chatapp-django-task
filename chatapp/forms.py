# chatapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    # ✅ Custom validation for first_name and last_name
    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match("^[A-Za-z]+$", first_name):
            raise forms.ValidationError("First name must only contain letters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match("^[A-Za-z]+$", last_name):
            raise forms.ValidationError("Last name must only contain letters.")
        return last_name
