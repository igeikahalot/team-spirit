"""
Сериализаторы для REST API
"""

from rest_framework import serializers
from .models import Discipline, Player, Achievement, Match, News, Partner, TeamInfo


class DisciplineSerializer(serializers.ModelSerializer):
    players_count = serializers.SerializerMethodField()

    class Meta:
        model = Discipline
        fields = ['id', 'name', 'slug', 'icon', 'description', 'is_active', 'players_count']

    def get_players_count(self, obj):
        return obj.players.filter(is_active=True).count()


class PlayerSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Player
        fields = [
            'id', 'nickname', 'first_name', 'last_name', 'full_name',
            'discipline', 'discipline_name', 'role', 'role_display',
            'photo', 'country', 'birth_date', 'join_date', 'bio',
            'twitch', 'twitter', 'instagram', 'is_active'
        ]


class AchievementSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    place_display = serializers.CharField(source='get_place_display', read_only=True)

    class Meta:
        model = Achievement
        fields = [
            'id', 'title', 'discipline', 'discipline_name',
            'place', 'place_display', 'prize_pool', 'prize_won',
            'date', 'image', 'description'
        ]


class MatchSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    result = serializers.ReadOnlyField()

    class Meta:
        model = Match
        fields = [
            'id', 'discipline', 'discipline_name', 'tournament',
            'opponent', 'opponent_logo', 'date', 'status', 'status_display',
            'score_team', 'score_opponent', 'stream_url', 'vod_url', 'result'
        ]


class NewsSerializer(serializers.ModelSerializer):
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'category', 'category_display',
            'discipline', 'discipline_name', 'image', 'excerpt',
            'content', 'is_featured', 'views', 'created_at', 'updated_at'
        ]


class NewsListSerializer(serializers.ModelSerializer):
    """Сокращённый сериализатор для списка новостей"""
    discipline_name = serializers.CharField(source='discipline.name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'category', 'category_display',
            'discipline_name', 'image', 'excerpt', 'is_featured',
            'views', 'created_at'
        ]


class PartnerSerializer(serializers.ModelSerializer):
    tier_display = serializers.CharField(source='get_tier_display', read_only=True)

    class Meta:
        model = Partner
        fields = ['id', 'name', 'tier', 'tier_display', 'logo', 'website', 'description']


class TeamInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamInfo
        fields = '__all__'
