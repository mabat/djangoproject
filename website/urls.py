"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
import django.contrib.auth.views
from django.contrib import admin
from django.conf.urls import url
from blog import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^welcome/', views.welcome, name = 'views.welcome'),
    url(r'^accounts/login/$', django.contrib.auth.views.login, name = 'login'),#redirect je definiranu settings.py LOGIN_REDIRECT_URL = '/blog/'
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout', kwargs={'next_page': '/welcome/'}), #kwargs preusmjeri na pocetnu stranicu nakon logout-a
    url(r'^accounts/registration_form/$', views.register_new, name = 'register_new'),
    url(r'^accounts/registration_accept/$', views.register_accept, name = 'register_accept'),
]
