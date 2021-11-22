from django.contrib import admin
from django.urls import path, include
from login import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('logout/', views.logout),
    path('movieList/', views.movieList),
    path('actorList/', views.actorList),
    path('directorList/', views.directorList),
    path('companyList/', views.companyList),
    path('movie/', views.movie),
    path('actor/', views.actor),
    path('director/', views.director),
    path('company/', views.company),
]