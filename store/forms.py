from django import forms
from account.models import Account

class UserShippingDataForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    is_logged = forms.CharField(max_length=10)
    email = forms.EmailField(max_length=200)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    state = forms.CharField(max_length=200)
    zipcode = forms.CharField(max_length=200)    
    total = forms.FloatField(required=False)
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if self.cleaned_data['is_logged']:
            return email
        try:
            account = Account.objects.get(email=email)   
        except:
            return email
        raise forms.ValidationError('is already in use')
    
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
        
    def clean_is_logged(self):
        is_logged = self.cleaned_data['is_logged']
        if is_logged == 'True':
            return True
        else:
            return False