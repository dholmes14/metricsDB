from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.Homepage, name='Homepage'),
    path('searchsample/', views.Searchsamplepage, name='Searchsamplepage'),
    path('projects/<Project_No>/', views.Projectpage, name='Projectpage'),
    path('bulkinput/', views.Bulkinputpage, name='Bulkinputpage'),
    path('HS_metrics_input/', views.HS_metrics_inputpage, name='HS_metrics_inputpage'),
]
