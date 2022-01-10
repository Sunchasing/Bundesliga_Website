
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('update/', views.UpdateView.as_view()),
    # path('matches/', views.MatchesListView.as_view()),
    # path('matches/upcoming/', views.UpcomingMatchesListView.as_view()),
    # path('teams/', views.TeamsListView.as_view()),
    path('teams/<int:team_id>/', views.TeamView.as_view()),
    ]
