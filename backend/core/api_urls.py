"""
API маршруты
"""

from django.urls import path
from . import api_views

urlpatterns = [
    path('disciplines/', api_views.DisciplineListAPI.as_view(), name='api_disciplines'),
    path('players/', api_views.PlayerListAPI.as_view(), name='api_players'),
    path('players/<int:pk>/', api_views.PlayerDetailAPI.as_view(), name='api_player_detail'),
    path('news/', api_views.NewsListAPI.as_view(), name='api_news'),
    path('matches/', api_views.MatchListAPI.as_view(), name='api_matches'),
    path('achievements/', api_views.AchievementListAPI.as_view(), name='api_achievements'),
    path('team-info/', api_views.TeamInfoAPI.as_view(), name='api_team_info'),
]
