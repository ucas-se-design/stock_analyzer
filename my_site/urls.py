"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',views.login),
    path('register',views.register),
    path('message',views.message),
    path('recoverpw',views.recoverpw),
    path('pages-login.html',views.login),
    path('pages-register.html',views.register),
    path('pages-recoverpw.html',views.recoverpw),
    path('message.html',views.message),
    path('start_login',views.start_login),
    path('start_register',views.start_register),
    path('home_page',views.home_page),
    path('recover',views.recover),
    path('index1.html',views.index1),
    path('index2.html',views.index2),
    path('index3.html',views.index3),
    path('more1',views.more1),
    path('more2',views.more2),
    path('more3',views.more3),
    path('exp',views.exps)
]
