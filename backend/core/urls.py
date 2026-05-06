"""
URL маршруты для основного приложения
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('discipline/<slug:slug>/', views.DisciplineDetailView.as_view(), name='discipline_detail'),
    path('player/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('matches/', views.MatchesView.as_view(), name='matches'),
    path('achievements/', views.AchievementsView.as_view(), name='achievements'),
    path('partners/', views.PartnersView.as_view(), name='partners'),
    path('about/', views.AboutView.as_view(), name='about'),
]
