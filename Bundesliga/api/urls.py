
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('update/', views.UpdateView.as_view()),
    path('matches/', views.UpcomingMatches.as_view(), name='home'),
    path('teams/', views.TeamsListView.as_view(), name='teams'),
    path('teams/<int:team_id>/', views.TeamView.as_view()),
    path('teams/<int:team_id>/upcoming/', views.UpcomingMatchesForTeam.as_view())
    ]
