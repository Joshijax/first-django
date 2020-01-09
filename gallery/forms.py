from django import forms
from .models import uploads, renamefile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UploadFileForm(forms.ModelForm):
    
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'placeholder':'input your password', 'class': 'custom-file-input',  'oninput' : 'input_filename();',  }))
    class Meta:
        model = uploads
        fields = ('file' ,)

class ContactForm(AuthenticationForm):
    
       email = forms.EmailField(required=True,label='email')
       password = forms.CharField(widget=forms.PasswordInput)
       class Meta:
            model = User
            fields = ('email', 'password', ) 


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username' }))
    email = forms.EmailField(max_length=254, label='email', help_text='Required. Inform a valid email address.', widget= forms.TextInput
                           (attrs={'placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'input your password' }))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password' }))

    class Meta:
        model = User
        fields = ('username' , 'email', 'password1', 'password2', )
        
class LoginUpForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username' }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'input your password' }))
    

    class Meta:
        model = User
        fields = ('username' , 'password', )

class renamee(forms.Form):
    rename = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'rename','class' :'form-control', 'required': 'required' }))
