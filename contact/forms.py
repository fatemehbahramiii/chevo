from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "maxlength": 120}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "subject": forms.TextInput(attrs={"maxlength": 180}),
            "message": forms.Textarea(attrs={"rows": 5, "maxlength": 5000}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="ایمیل")
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
