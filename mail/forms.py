from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ComposeForm(forms.Form):
    recipient = forms.CharField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
