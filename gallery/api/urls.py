
from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from gallery.api.views import api_show_image, api_put_image, api_upload_image, api_delete_image, api_newUser
app_name  = 'gallery'

urlpatterns = [
    path('image/show_image/<id_image>/<str:slug>/', views.api_show_image, name='show_image')  ,  
    
    path('put/image/show_image/<id_image>/<str:slug>/', views.api_put_image, name="put_image"),
    path('del/image/show_image/<id_image>/<str:slug>/', views.api_delete_image, name="delete"),
    path('post/image/', views.api_upload_image, name="create"),
    path('signup', views.api_newUser, name="newUser"),
    path('', obtain_auth_token, name="login"),
    
]
