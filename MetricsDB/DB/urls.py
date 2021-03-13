from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.Homepage, name='Homepage'),
    path('variants/<int:variant_id>/', views.Variantpage, name='Variantpage'),
    path('projects/<Project_No>/', views.Projectpage, name='Projectpage'),
    path('datainput/', views.Datainputpage, name='Datainputpage'),
    path('bulkinput/', views.Bulkinputpage, name='Bulkinputpage'),
]
