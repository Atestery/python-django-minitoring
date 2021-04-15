 
from django.urls import path
from . import views
from django.conf.urls import url


from django.conf.urls import url
from . import views

# -*- coding: utf-8 -*-
urlpatterns = [
    path('', views.index, name='home'),
    #path('about', views.about, name='about'),
    #path('readfile', views.readfile, name='readfile'),

]
# Create your views here.

