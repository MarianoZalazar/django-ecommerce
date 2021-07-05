from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account
from store.models import CustomerModel

class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Add a valid email addres")
    
    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2')
       
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
            return email
        except:
            raise forms.ValidationError(f'Email {email} is already in use')
        
class CreateCustomerForm():
    
    class Meta:
        model = CustomerModel
        field = ('first_name', 'last_name')
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if first_name.isalpha():
            return first_name.lower()
        else:
            raise forms.ValidationError('First Name must be alphabetical')
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if last_name.isalpha():
            return last_name.lower()
        else:
            raise forms.ValidationError('Last Name must be alphabetical')  