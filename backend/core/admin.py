"""
Административная панель для Team Spirit
"""

from django.contrib import admin
from .models import (
    Discipline, Player, Achievement, Match, News, Partner, TeamInfo,
    Role, SocialLink, PlayerSocialLink
)


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    list_editable = ['order']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform']
    list_filter = ['platform']
    search_fields = ['name']


class PlayerSocialLinkInline(admin.TabularInline):
    """Inline для редактирования соц. сетей игрока"""
    model = PlayerSocialLink
    extra = 1
    fields = ['platform', 'url', 'username']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'full_name', 'discipline', 'role', 'country', 'is_active']
    list_filter = ['discipline', 'role', 'is_active', 'country']
    search_fields = ['nickname', 'first_name', 'last_name']
    list_editable = ['is_active']
    date_hierarchy = 'join_date'
    inlines = [PlayerSocialLinkInline]
    fieldsets = (
        ('Основное', {
            'fields': ('nickname', 'first_name', 'last_name', 'photo')
        }),
        ('Команда', {
            'fields': ('discipline', 'role', 'is_active', 'join_date')
        }),
        ('Личная информация', {
            'fields': ('country', 'birth_date', 'bio'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'discipline', 'place', 'prize_won', 'date']
    list_filter = ['discipline', 'place', 'date']
    search_fields = ['title']
    date_hierarchy = 'date'


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['opponent', 'tournament', 'discipline', 'date', 'status', 'score_team', 'score_opponent']
    list_filter = ['discipline', 'status', 'date']
    search_fields = ['opponent', 'tournament']
    list_editable = ['status', 'score_team', 'score_opponent']
    date_hierarchy = 'date'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'discipline', 'is_featured', 'is_published', 'views', 'created_at']
    list_filter = ['category', 'discipline', 'is_featured', 'is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_published']
    date_hierarchy = 'created_at'


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'order', 'is_active']
    list_filter = ['tier', 'is_active']
    search_fields = ['name']
    list_editable = ['order', 'is_active']


@admin.register(TeamInfo)
class TeamInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'founded_year', 'headquarters', 'total_earnings']


# Настройка админки
admin.site.site_header = 'Team Spirit - Админ-панель'
admin.site.site_title = 'Team Spirit'
admin.site.index_title = 'Управление сайтом'
