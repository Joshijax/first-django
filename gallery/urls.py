from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

from django.urls import include, path
from django.conf.urls import url



urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_request, name="logout"),
    path('upload/', views.upload_file, name="upload_file"),
    path('download/<file_name>/', views.download, name="download"),
    path('search/', views.search, name="search"),
    path('image/', views.image, name="image"),
    path('vid/', views.video, name="video"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('image/show_image/<id_image>/<str:slug>', views.show_image, name='show_image'),
    path('delete/<id_image>/<file_name>/', views.delete, name='delete'),
    path('rename/<file_name>/', views.rename, name='rename'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]





urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)