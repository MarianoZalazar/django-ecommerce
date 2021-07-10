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
        except:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')
        
class CreateCustomerForm(forms.ModelForm):
    
    class Meta:
        model = CustomerModel
        fields = ('first_name', 'last_name')
    
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
        

class UserShippingDataForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=200)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)
    zipcode = forms.CharField(max_length=200)    

    
    
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)   
        except:
            return email
        raise forms.ValidationError(f'Email {email} is already in use')
    
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

class UserDataForm(forms.Form):
    first_name = forms.CharField(max_length=50, label='First Name')
    last_name = forms.CharField(max_length=50, label='Last Name')
    email = forms.EmailField(max_length=200, label='Email')
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Repeat password',
        strip=False,
        widget=forms.PasswordInput()
    )
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError('Confirm your password')
        if password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return password2
        
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)   
        except:
            return email
        raise forms.ValidationError(f'is already in use')
    
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