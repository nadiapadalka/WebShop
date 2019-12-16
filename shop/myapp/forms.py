# -*- coding: utf-8 -*-

from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
            'password_check'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['password_check'].label = 'Repeat the password carefully'
        self.fields['first_name'].label = 'Name'
        self.fields['last_name'].label = 'Surname'
        self.fields['email'].label = 'Email'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already in use, try a different one.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("The adress is already in use, try a different one.")
        if password != password_check:
            raise forms.ValidationError("Passwords don't match,try again!")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'username'
        self.fields['password'].label = 'password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("There is no user with such a username.")

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError("The password is not correct.We recommend you to try again!")

class OrderForm(forms.Form):

    name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField()
    buying_type = forms.ChoiceField(widget=forms.Select(), choices=([("self", "By yourself"),("delivery","Delievery")]))
    address = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Name'
        self.fields['name'].help_text = '(please, put in your real name!)'
        self.fields['last_name'].label = 'Surname'
        self.fields['last_name'].help_text = '(please, put in your real surname!)'
        self.fields['phone'].label = 'Phone Number'
        self.fields['buying_type'].label = 'How you want to recieve the product?'
        self.fields['address'].label = 'Delievery adress'
        self.fields['comments'].label = 'Comments'
