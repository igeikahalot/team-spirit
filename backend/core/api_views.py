"""
API представления
"""

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from .models import Discipline, Player, Achievement, Match, News, Partner, TeamInfo
from .serializers import (
    DisciplineSerializer, PlayerSerializer, AchievementSerializer,
    MatchSerializer, NewsSerializer, NewsListSerializer, TeamInfoSerializer
)


class DisciplineListAPI(generics.ListAPIView):
    """API: Список дисциплин"""
    queryset = Discipline.objects.filter(is_active=True)
    serializer_class = DisciplineSerializer


class PlayerListAPI(generics.ListAPIView):
    """API: Список игроков"""
    serializer_class = PlayerSerializer

    def get_queryset(self):
        queryset = Player.objects.filter(is_active=True)
        discipline = self.request.query_params.get('discipline')
        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
        return queryset


class PlayerDetailAPI(generics.RetrieveAPIView):
    """API: Детали игрока"""
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class NewsListAPI(generics.ListAPIView):
    """API: Список новостей"""
    serializer_class = NewsListSerializer

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        category = self.request.query_params.get('category')
        discipline = self.request.query_params.get('discipline')
        featured = self.request.query_params.get('featured')
        limit = self.request.query_params.get('limit')

        if category:
            queryset = queryset.filter(category=category)
        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
        if featured:
            queryset = queryset.filter(is_featured=True)
        if limit:
            queryset = queryset[:int(limit)]

        return queryset


class MatchListAPI(generics.ListAPIView):
    """API: Список матчей"""
    serializer_class = MatchSerializer

    def get_queryset(self):
        queryset = Match.objects.all()
        status = self.request.query_params.get('status')
        discipline = self.request.query_params.get('discipline')
        limit = self.request.query_params.get('limit')

        if status:
            queryset = queryset.filter(status=status)
        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
        if limit:
            queryset = queryset[:int(limit)]

        return queryset


class AchievementListAPI(generics.ListAPIView):
    """API: Список достижений"""
    serializer_class = AchievementSerializer

    def get_queryset(self):
        queryset = Achievement.objects.all()
        discipline = self.request.query_params.get('discipline')
        year = self.request.query_params.get('year')
        top = self.request.query_params.get('top')

        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
        if year:
            queryset = queryset.filter(date__year=year)
        if top:
            queryset = queryset.filter(place__lte=int(top))

        return queryset


class TeamInfoAPI(APIView):
    """API: Информация о команде"""
    
    def get(self, request):
        team_info = TeamInfo.objects.first()
        if team_info:
            data = TeamInfoSerializer(team_info).data
        else:
            data = {}
        
        # Добавляем статистику
        data['stats'] = {
            'total_earnings': Achievement.objects.aggregate(total=Sum('prize_won'))['total'] or 0,
            'tournaments_won': Achievement.objects.filter(place=1).count(),
            'players_count': Player.objects.filter(is_active=True).count(),
            'disciplines_count': Discipline.objects.filter(is_active=True).count(),
        }
        
        return Response(data)
