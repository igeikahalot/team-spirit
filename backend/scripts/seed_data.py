#!/usr/bin/env python
"""
Скрипт для заполнения базы данных начальными данными.
Запуск: python manage.py shell < scripts/seed_data.py
или: python scripts/seed_data.py (если DJANGO_SETTINGS_MODULE установлен)
"""

import os
import sys
import django
from datetime import date, datetime, timedelta
from decimal import Decimal

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_spirit.settings')
django.setup()

from core.models import Discipline, Player, Achievement, Match, News, Partner, TeamInfo

def create_seed_data():
    print("🎮 Создание начальных данных для Team Spirit...")
    
    # Создаём информацию о команде
    team_info, created = TeamInfo.objects.get_or_create(
        pk=1,
        defaults={
            'about': '''Team Spirit — российская киберспортивная организация, основанная в 2015 году.

Главным достижением команды является победа на The International 2021 — крупнейшем турнире по Dota 2 с призовым фондом более $40 миллионов. Эта историческая победа сделала Team Spirit одной из самых узнаваемых киберспортивных организаций в мире.

Team Spirit представлен в нескольких ведущих киберспортивных дисциплинах и продолжает развиваться, привлекая талантливых игроков со всего мира.''',
            'founded_year': 2015,
            'headquarters': 'Москва, Россия',
            'total_earnings': Decimal('20000000'),
            'twitter': 'https://twitter.com/Team__Spirit',
            'instagram': 'https://instagram.com/team__spirit',
            'youtube': 'https://youtube.com/@TeamSpiritDota2',
            'twitch': 'https://twitch.tv/team_spirit',
            'vk': 'https://vk.com/teamspiritru',
            'telegram': 'https://t.me/team_spirit',
            'contact_email': 'info@teamspirit.ru',
        }
    )
    if created:
        print("✅ Информация о команде создана")
    
    # Создаём дисциплины
    disciplines_data = [
        {'name': 'Dota 2', 'slug': 'dota2', 'description': 'Основной состав по Dota 2 — чемпионы The International 2021'},
        {'name': 'Counter-Strike 2', 'slug': 'cs2', 'description': 'Состав по Counter-Strike 2'},
        {'name': 'PUBG Mobile', 'slug': 'pubgm', 'description': 'Мобильный киберспорт — PUBG Mobile'},
    ]
    
    disciplines = {}
    for data in disciplines_data:
        disc, created = Discipline.objects.get_or_create(
            slug=data['slug'],
            defaults={'name': data['name'], 'description': data['description']}
        )
        disciplines[data['slug']] = disc
        if created:
            print(f"✅ Дисциплина создана: {data['name']}")
    
    # Создаём игроков Dota 2
    dota_players = [
        {'nickname': 'Yatoro', 'first_name': 'Илья', 'last_name': 'Мулярчук', 'role': 'carry', 'country': 'Украина'},
        {'nickname': 'Larl', 'first_name': 'Денис', 'last_name': 'Сигитов', 'role': 'mid', 'country': 'Россия'},
        {'nickname': 'Collapse', 'first_name': 'Магомед', 'last_name': 'Халилов', 'role': 'offlane', 'country': 'Россия'},
        {'nickname': 'Mira', 'first_name': 'Мирослав', 'last_name': 'Колпаков', 'role': 'support', 'country': 'Россия'},
        {'nickname': 'Miposhka', 'first_name': 'Ярослав', 'last_name': 'Найдёнов', 'role': 'captain', 'country': 'Россия'},
    ]
    
    for data in dota_players:
        player, created = Player.objects.get_or_create(
            nickname=data['nickname'],
            discipline=disciplines['dota2'],
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': data['role'],
                'country': data['country'],
                'join_date': date(2021, 1, 1),
            }
        )
        if created:
            print(f"✅ Игрок создан: {data['nickname']}")
    
    # Создаём достижения
    achievements_data = [
        {
            'title': 'The International 2021',
            'discipline': 'dota2',
            'place': 1,
            'prize_pool': Decimal('40018195'),
            'prize_won': Decimal('18208300'),
            'date': date(2021, 10, 17),
            'description': 'Историческая победа на главном турнире года'
        },
        {
            'title': 'The International 2023',
            'discipline': 'dota2',
            'place': 2,
            'prize_pool': Decimal('15000000'),
            'prize_won': Decimal('3000000'),
            'date': date(2023, 10, 29),
            'description': 'Второе место на TI12'
        },
        {
            'title': 'Riyadh Masters 2023',
            'discipline': 'dota2',
            'place': 1,
            'prize_pool': Decimal('15000000'),
            'prize_won': Decimal('5000000'),
            'date': date(2023, 7, 30),
            'description': 'Победа на крупном турнире в Саудовской Аравии'
        },
        {
            'title': 'ESL One Berlin Major 2023',
            'discipline': 'dota2',
            'place': 3,
            'prize_pool': Decimal('1000000'),
            'prize_won': Decimal('150000'),
            'date': date(2023, 5, 7),
        },
        {
            'title': 'DreamLeague Season 19',
            'discipline': 'dota2',
            'place': 1,
            'prize_pool': Decimal('1000000'),
            'prize_won': Decimal('400000'),
            'date': date(2023, 2, 26),
        },
    ]
    
    for data in achievements_data:
        disc_slug = data.pop('discipline')
        achievement, created = Achievement.objects.get_or_create(
            title=data['title'],
            date=data['date'],
            defaults={
                'discipline': disciplines[disc_slug],
                **data
            }
        )
        if created:
            print(f"✅ Достижение создано: {data['title']}")
    
    # Создаём матчи
    matches_data = [
        {
            'discipline': 'dota2',
            'tournament': 'DreamLeague Season 24',
            'opponent': 'Team Liquid',
            'date': datetime.now() + timedelta(days=3),
            'status': 'upcoming',
        },
        {
            'discipline': 'dota2',
            'tournament': 'DreamLeague Season 24',
            'opponent': 'Tundra Esports',
            'date': datetime.now() + timedelta(days=5),
            'status': 'upcoming',
        },
        {
            'discipline': 'dota2',
            'tournament': 'ESL One Bangkok',
            'opponent': 'OG',
            'date': datetime.now() - timedelta(days=2),
            'status': 'finished',
            'score_team': 2,
            'score_opponent': 1,
        },
        {
            'discipline': 'dota2',
            'tournament': 'ESL One Bangkok',
            'opponent': 'BetBoom Team',
            'date': datetime.now() - timedelta(days=5),
            'status': 'finished',
            'score_team': 2,
            'score_opponent': 0,
        },
    ]
    
    for data in matches_data:
        disc_slug = data.pop('discipline')
        match, created = Match.objects.get_or_create(
            tournament=data['tournament'],
            opponent=data['opponent'],
            date=data['date'],
            defaults={
                'discipline': disciplines[disc_slug],
                **data
            }
        )
        if created:
            print(f"✅ Матч создан: vs {data['opponent']}")
    
    # Создаём новости
    news_data = [
        {
            'title': 'Team Spirit побеждает на ESL One Bangkok',
            'slug': 'team-spirit-esl-one-bangkok-victory',
            'category': 'result',
            'discipline': 'dota2',
            'excerpt': 'Наша команда одержала уверенную победу на турнире ESL One Bangkok, обыграв в финале OG со счётом 3:1.',
            'content': '''Team Spirit продолжает демонстрировать великолепную форму!

На турнире ESL One Bangkok наши ребята показали отличную игру и заслуженно взяли первое место. В финале мы встретились с командой OG и одержали победу со счётом 3:1.

MVP турнира был признан Collapse за его невероятную игру на Mars и Axe.

Благодарим всех фанатов за поддержку!''',
            'is_featured': True,
        },
        {
            'title': 'Анонс нового состава по CS2',
            'slug': 'cs2-roster-announcement',
            'category': 'roster',
            'discipline': 'cs2',
            'excerpt': 'Team Spirit объявляет о формировании нового состава по Counter-Strike 2.',
            'content': '''Мы рады объявить о создании нового состава по Counter-Strike 2!

После долгих переговоров и просмотров мы собрали команду из талантливых игроков, которые будут представлять Team Spirit на международной арене CS2.

Подробности о составе будут объявлены в ближайшее время. Следите за нашими социальными сетями!''',
            'is_featured': True,
        },
        {
            'title': 'Интервью с Miposhka после победы на TI',
            'slug': 'miposhka-ti-interview',
            'category': 'interview',
            'discipline': 'dota2',
            'excerpt': 'Капитан Team Spirit рассказал о подготовке к турниру и эмоциях после победы.',
            'content': '''Ярослав "Miposhka" Найдёнов поделился впечатлениями после исторической победы на The International.

"Это был долгий путь. Мы много работали, анализировали соперников и верили друг в друга. Когда прозвучал последний GG, я не мог поверить, что мы сделали это."

Капитан также рассказал о планах команды на будущее и поблагодарил всех фанатов за невероятную поддержку.''',
        },
    ]
    
    for data in news_data:
        disc_slug = data.pop('discipline', None)
        news, created = News.objects.get_or_create(
            slug=data['slug'],
            defaults={
                'discipline': disciplines.get(disc_slug) if disc_slug else None,
                **data
            }
        )
        if created:
            print(f"✅ Новость создана: {data['title']}")
    
    # Создаём партнёров
    partners_data = [
        {'name': 'PARI', 'tier': 'title', 'website': 'https://pari.ru', 'order': 1},
        {'name': 'HyperX', 'tier': 'main', 'website': 'https://hyperx.com', 'order': 1},
        {'name': 'ASUS ROG', 'tier': 'main', 'website': 'https://rog.asus.com', 'order': 2},
        {'name': 'Red Bull', 'tier': 'official', 'website': 'https://redbull.com', 'order': 1},
        {'name': 'Secretlab', 'tier': 'technical', 'website': 'https://secretlab.co', 'order': 1},
    ]
    
    for data in partners_data:
        partner, created = Partner.objects.get_or_create(
            name=data['name'],
            defaults=data
        )
        if created:
            print(f"✅ Партнёр создан: {data['name']}")
    
    print("\n🎉 Начальные данные успешно созданы!")
    print(f"   - Дисциплин: {Discipline.objects.count()}")
    print(f"   - Игроков: {Player.objects.count()}")
    print(f"   - Достижений: {Achievement.objects.count()}")
    print(f"   - Матчей: {Match.objects.count()}")
    print(f"   - Новостей: {News.objects.count()}")
    print(f"   - Партнёров: {Partner.objects.count()}")


if __name__ == '__main__':
    create_seed_data()
