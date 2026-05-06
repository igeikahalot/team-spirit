"""
Представления для сайта Team Spirit
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Sum, Count
from .models import Discipline, Player, Achievement, Match, News, Partner, TeamInfo


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_info'] = TeamInfo.objects.first()
        context['featured_news'] = News.objects.filter(is_published=True, is_featured=True)[:3]
        context['latest_news'] = News.objects.filter(is_published=True)[:6]
        context['upcoming_matches'] = Match.objects.filter(status='upcoming').order_by('date')[:5]
        context['recent_results'] = Match.objects.filter(status='finished').order_by('-date')[:5]
        context['disciplines'] = Discipline.objects.filter(is_active=True)
        context['partners'] = Partner.objects.filter(is_active=True)[:8]
        context['achievements'] = Achievement.objects.filter(place__lte=3).order_by('-date')[:6]
        
        # Статистика
        context['stats'] = {
            'total_earnings': Achievement.objects.aggregate(total=Sum('prize_won'))['total'] or 0,
            'tournaments_won': Achievement.objects.filter(place=1).count(),
            'players_count': Player.objects.filter(is_active=True).count(),
        }
        return context


class TeamView(TemplateView):
    """Страница команды с составами"""
    template_name = 'core/team.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_info'] = TeamInfo.objects.first()
        context['disciplines'] = Discipline.objects.filter(is_active=True).prefetch_related('players')
        return context


class DisciplineDetailView(DetailView):
    """Страница дисциплины"""
    model = Discipline
    template_name = 'core/discipline_detail.html'
    context_object_name = 'discipline'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.players.filter(is_active=True)
        context['achievements'] = self.object.achievements.all()[:10]
        context['matches'] = self.object.matches.all()[:10]
        return context


class PlayerDetailView(DetailView):
    """Страница игрока"""
    model = Player
    template_name = 'core/player_detail.html'
    context_object_name = 'player'


class NewsListView(ListView):
    """Список новостей"""
    model = News
    template_name = 'core/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 12

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        category = self.request.GET.get('category')
        discipline = self.request.GET.get('discipline')
        
        if category:
            queryset = queryset.filter(category=category)
        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Discipline.objects.filter(is_active=True)
        context['categories'] = News.CATEGORY_CHOICES
        return context


class NewsDetailView(DetailView):
    """Детальная страница новости"""
    model = News
    template_name = 'core/news_detail.html'
    context_object_name = 'news'

    def get_object(self):
        obj = super().get_object()
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_news'] = News.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)[:4]
        return context


class MatchesView(ListView):
    """Список матчей"""
    model = Match
    template_name = 'core/matches.html'
    context_object_name = 'matches'
    paginate_by = 20

    def get_queryset(self):
        queryset = Match.objects.all()
        status = self.request.GET.get('status')
        discipline = self.request.GET.get('discipline')
        
        if status:
            queryset = queryset.filter(status=status)
        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Discipline.objects.filter(is_active=True)
        context['upcoming'] = Match.objects.filter(status='upcoming').count()
        context['live'] = Match.objects.filter(status='live').count()
        return context


class AchievementsView(ListView):
    """Список достижений"""
    model = Achievement
    template_name = 'core/achievements.html'
    context_object_name = 'achievements'
    paginate_by = 20

    def get_queryset(self):
        queryset = Achievement.objects.all()
        discipline = self.request.GET.get('discipline')
        year = self.request.GET.get('year')
        
        if discipline:
            queryset = queryset.filter(discipline__slug=discipline)
        if year:
            queryset = queryset.filter(date__year=year)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplines'] = Discipline.objects.filter(is_active=True)
        context['total_prize'] = Achievement.objects.aggregate(total=Sum('prize_won'))['total'] or 0
        context['first_places'] = Achievement.objects.filter(place=1).count()
        return context


class PartnersView(TemplateView):
    """Страница партнёров"""
    template_name = 'core/partners.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_sponsors'] = Partner.objects.filter(tier='title', is_active=True)
        context['main_partners'] = Partner.objects.filter(tier='main', is_active=True)
        context['official_partners'] = Partner.objects.filter(tier='official', is_active=True)
        context['technical_partners'] = Partner.objects.filter(tier='technical', is_active=True)
        return context


class AboutView(TemplateView):
    """Страница о команде"""
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_info'] = TeamInfo.objects.first()
        context['stats'] = {
            'total_earnings': Achievement.objects.aggregate(total=Sum('prize_won'))['total'] or 0,
            'tournaments_won': Achievement.objects.filter(place=1).count(),
            'players_count': Player.objects.filter(is_active=True).count(),
            'disciplines_count': Discipline.objects.filter(is_active=True).count(),
        }
        return context
