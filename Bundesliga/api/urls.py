
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('Update/', views.UpdateView.as_view()),
    ]
