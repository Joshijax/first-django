from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages 
from django.conf import settings
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from functools import wraps
import pathlib
from django.utils.text import slugify
from django.core.files import File
from .forms import UploadFileForm, SignUpForm, ContactForm,LoginUpForm, renamee
import functools
import urllib, mimetypes
from django.http import HttpResponse, Http404
from wsgiref.util import FileWrapper
from django.shortcuts import render
from django.db.models import Q
import os
from django.conf import settings
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import uploads, uploadss
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.utils.encoding import smart_str
from notify.signals import notify
# Create your views here.






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
def upload_file(request):
    

    if request.user.is_authenticated == True:
        user = request.user
        print(user)
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            file_type = 'image'
            config = ['.PNG', '.JPG', '.JPEG', '.GIF']
            config1 = [ '.PDF']
            config2 = [ '.MP4', '.3GP']   
            file_name=request.FILES['file']
            extension = os.path.splitext(str(request.FILES['file']))[1]
            extension = extension.upper()
            print(extension)
            if extension in config and form.is_valid():
                new_obj = uploads(file_name=request.FILES['file'],filetype='image',file=form.cleaned_data['file'], username=user, author=request.user)
                new_obj.save()
                
                notify.send(request.user, recipient=user, actor=request.user , verb='followed you.', nf_type='followed_by_one_user')

                messages.add_message(request, messages.SUCCESS, 'image succesfully uploaded')
                return redirect('image')
            if extension in config2 and form.is_valid():
                new_obj = uploads(file_name=request.FILES['file'],filetype='video',file=form.cleaned_data['file'], username=user, author=request.user)
                new_obj.save()
                messages.add_message(request, messages.SUCCESS, 'video succesfully uploaded')
                return redirect('video')
            messages.add_message(request, messages.SUCCESS, 'file not allowed')
            return redirect('home')
        return redirect('home')
    else:
        form = UploadFileForm()
    messages.add_message(request, messages.SUCCESS, 'Error')
    return redirect('home')  

@login_required(login_url='/')    
def image(request):
    form = UploadFileForm(request.POST, request.FILES)
    if request.user.is_authenticated == True:
        
        user = request.user
        file_type = 'image'
        tests = uploads.objects.all().filter(filetype= file_type,username=user).order_by('uploaded_at').reverse()
        paginator = Paginator(tests, 8)
        page = request.GET.get('page')

        tests = paginator.get_page(page)

        
    if page:
        return render(request, '__sub_image.html', {'tests': tests, 'form': form, 'media_url': settings.MEDIA_URL,})
    else:
        return render(request, 'image.html', {'tests': tests, 'form': form, 'media_url': settings.MEDIA_URL,})

@login_required(login_url='/')    
def video(request):
    form = UploadFileForm(request.POST, request.FILES)
    if request.user.is_authenticated == True:
        
        user = request.user
        file_type = 'video'
        tests = uploads.objects.all().filter(filetype= file_type,username=user).order_by('uploaded_at').reverse()
        test = uploads.objects.all().filter(filetype= file_type,username=user).order_by('uploaded_at').count()
        paginator = Paginator(tests, 8)
        page = request.GET.get('page')
        print(test)
        tests = paginator.get_page(page)

        
    if page:
        return render(request, '__sub_vid.html', {'tests': tests, 'test': test, 'form': form, 'media_url': settings.MEDIA_URL,})
    else:
        return render(request, 'vid.html', {'tests': tests, 'form': form, 'media_url': settings.MEDIA_URL,})

@login_required(login_url='/')
def search(request):
    q = request.GET.get('q')
    print(q)
    query_string = "SELECT * FROM gallery_uploads WHERE file_name  LIKE %s ORDER BY id ASC"
    search = uploads.objects.raw(query_string, ('%' + q + '%',))
    paginator = Paginator(search, 8)
    page = request.GET.get('page')
    
    search = paginator.get_page(page)
    if len(list(search)) > 0:
        messages.add_message(request, messages.SUCCESS, f'Result for search {q}')
    else:
        messages.warning(request, f'No Result for search {q}')
        
    return render(request, 'search.html',  {'search': search, 'media_url': settings.MEDIA_URL,})
@login_required(login_url='/')
def rename(request, file_name):
    
    if request.method == 'POST':
        form = renamee(request.POST)
        file=form.data['rename']
        ext = file_name.rsplit(".", 1)[1]
        newname = file+'.'+ext
        file_field = 'gallery/{}/{}'.format(request.user, newname)
        update = uploads.objects.get(file_name=file_name)
        update.file_name = newname
        update.file = file_field
        update.save()
        slug = slugify(newname, allow_unicode=True)
        print(slug)
        os.rename(settings.MEDIA_ROOT +'/gallery/{}/{}'.format(request.user, file_name), settings.MEDIA_ROOT +'/gallery/{}/{}'.format(request.user, newname))
        print(newname)
    else:
        form = rename()
    return HttpResponseRedirect("/image/show_image/44/{}".format(slug))


@login_required(login_url='/')
def show_image(request, id_image, slug):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = renamee(request.POST)
        # check whether it's valid:
        

    # if a GET (or any other method) we'll create a blank form
    else:
        form = renamee()

    tests = uploads.objects.all().filter(slug= slug, id=id_image)
    
    
    
    return render(request, 'view_image.html', {'tests': tests,'form':form, 'media_url': settings.MEDIA_URL,})
@login_required(login_url='/')
def delete(request, id_image, file_name):
    user = request.user
    
    tests = uploads.objects.get(id = id_image,)
    tests.delete()
    messages.add_message(request, messages.SUCCESS, f'image {file_name} successfully deleted')
    return redirect('image')


def download(request,file_name):
    user = request.user
    file_path = settings.MEDIA_ROOT +'/gallery/{}/'.format(user)+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s/' % str(file_name) 
    return response



@login_required(login_url='/')
def home(request):
    form = UploadFileForm(request.POST, request.FILES)
    
    
    return render(request, 'home.html', { 'form': form})

def logout_request(request):
    
    del request.session['username']
    
    logout(request)
    
    return redirect('/')