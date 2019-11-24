from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages 
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
import pathlib
import functools
import os
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

# Create your views here.

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


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped

def is_logged_in(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated == True:
            return redirect('home')
        else:
            return f(request, *args, *kwargs)

    return wrap


@is_logged_in
def index(request):
    
    if request.method == 'POST':
           form = LoginUpForm(data=request.POST)
           if form.is_valid():
               username = form.cleaned_data['username']
               password = form.cleaned_data['password']
               user = authenticate(username=username, password=password)
              
               login(request, user)
               request.session['username'] = username
               messages.info(request, f"you are logged in as {username} ")
               return redirect('home')
               # assert False
              
    else:
        form = LoginUpForm()
      
    return render(request, 'login.html',  {'form': form,})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Hello world.')
        return redirect('/')
    else:
        return render(request, 'activation_invalid.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            pathlib.Path(r'\static', username).mkdir(exist_ok=True)
            dir = r'C:\Users\USER\Desktop\django text\gallery\static\{}'.format(username)
            if not os.path.exists(dir):
                
                os.mkdir(dir)
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    



@login_required(login_url='/')
def home(request):
    test = User.objects.get(id=1)
    return render(request, 'home.html', {'test': test})

def logout_request(request):
    del request.session['username']
    
    logout(request)
    
    return redirect('/')