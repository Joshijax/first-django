from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save, post_delete, post_init
from django.dispatch import receiver
from rest_framework.authtoken.models import Token 
import os




 

# Create your models here.
class Student(models.Model):
    
    roll_no = models.TextField()
    name = models.TextField(max_length = 40)
    stud_class = models.TextField()
    department = models.TextField()

def user_directory_path(instance, filename, **kwargs):
    file_path = 'gallery/{username}/{filename}'.format( username = str(instance.author.username), filename=filename)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return file_path
class renamefile(models.Model):
    file = models.CharField(max_length = 100, blank=True)
    

class uploads(models.Model):
    file = models.FileField(upload_to=user_directory_path, null=False, blank=False)
    filename = models.CharField(max_length = 100, blank=True)
    username = models.CharField(max_length = 100)
    file_name = models.CharField(max_length = 200)
    file_name1 = models.CharField(max_length = 200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=False, blank=False)
    filetype = models.CharField(max_length = 10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length = 150, unique=False)
  

    def __unicode__(self):
        return '%s' % (self.file.name)

    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(uploads,self).delete(*args,**kwargs)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.file_name, allow_unicode=True)
        super(uploads, self).save(*args, **kwargs)

  




class uploadss(models.Model):
    

    filenamee = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    filetype = models.CharField(max_length = 10)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length = 150, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.filenamee, allow_unicode=True)
        super(uploadss, self).save(*args, **kwargs)





@receiver(post_save, sender= settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


