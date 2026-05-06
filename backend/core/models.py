"""
Модели для информационного сайта Team Spirit
"""

from django.db import models
from django.utils import timezone


class Discipline(models.Model):
    """Игровая дисциплина"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', unique=True)
    icon = models.ImageField('Иконка', upload_to='disciplines/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'
        ordering = ['name']

    def __str__(self):
        return self.name


class Role(models.Model):
    """Роль игрока (редактируется через админку)"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Код', unique=True, help_text='Например: carry, support, coach')
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок сортировки', default=0)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    """Социальная сеть (типы соц. сетей)"""
    PLATFORM_CHOICES = [
        ('twitter', 'Twitter/X'),
        ('instagram', 'Instagram'),
        ('twitch', 'Twitch'),
        ('youtube', 'YouTube'),
        ('vk', 'VKontakte'),
        ('telegram', 'Telegram'),
        ('steam', 'Steam'),
        ('faceit', 'FACEIT'),
        ('discord', 'Discord'),
        ('tiktok', 'TikTok'),
        ('other', 'Другое'),
    ]

    name = models.CharField('Название', max_length=100)
    platform = models.CharField('Платформа', max_length=20, choices=PLATFORM_CHOICES)
    icon_class = models.CharField('CSS класс иконки', max_length=100, blank=True, help_text='Опционально: класс иконки FontAwesome или другой')

    class Meta:
        verbose_name = 'Тип социальной сети'
        verbose_name_plural = 'Типы социальных сетей'
        ordering = ['name']

    def __str__(self):
        return self.name


class Player(models.Model):
    """Игрок команды"""
    nickname = models.CharField('Никнейм', max_length=100)
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    discipline = models.ForeignKey(
        Discipline, 
        on_delete=models.CASCADE, 
        related_name='players',
        verbose_name='Дисциплина'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        related_name='players',
        verbose_name='Роль',
        blank=True,
        null=True
    )
    photo = models.ImageField('Фото', upload_to='players/', blank=True, null=True)
    country = models.CharField('Страна', max_length=100, default='Россия')
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    join_date = models.DateField('Дата вступления', default=timezone.now)
    bio = models.TextField('Биография', blank=True)
    is_active = models.BooleanField('В составе', default=True)

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        ordering = ['discipline', 'nickname']

    def __str__(self):
        return f'{self.nickname} ({self.role.name if self.role else "Без роли"})'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class PlayerSocialLink(models.Model):
    """Социальные сети игрока"""
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='social_links',
        verbose_name='Игрок'
    )
    platform = models.CharField('Платформа', max_length=20, choices=SocialLink.PLATFORM_CHOICES)
    url = models.URLField('Ссылка')
    username = models.CharField('Имя пользователя', max_length=100, blank=True, help_text='Опционально: ник на платформе')

    class Meta:
        verbose_name = 'Соц. сеть игрока'
        verbose_name_plural = 'Соц. сети игроков'
        unique_together = ['player', 'platform']

    def __str__(self):
        return f'{self.player.nickname} - {self.get_platform_display()}'


class Achievement(models.Model):
    """Достижения команды"""
    PLACE_CHOICES = [
        (1, '1 место'),
        (2, '2 место'),
        (3, '3 место'),
        (4, 'Топ-4'),
        (8, 'Топ-8'),
        (16, 'Топ-16'),
    ]

    title = models.CharField('Название турнира', max_length=200)
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name='Дисциплина'
    )
    place = models.IntegerField('Место', choices=PLACE_CHOICES)
    prize_pool = models.DecimalField('Призовой фонд ($)', max_digits=12, decimal_places=2, default=0)
    prize_won = models.DecimalField('Выигрыш ($)', max_digits=12, decimal_places=2, default=0)
    date = models.DateField('Дата')
    image = models.ImageField('Изображение', upload_to='achievements/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Достижение'
        verbose_name_plural = 'Достижения'
        ordering = ['-date']

    def __str__(self):
        return f'{self.title} - {self.get_place_display()}'


class Match(models.Model):
    """Матчи команды"""
    STATUS_CHOICES = [
        ('upcoming', 'Предстоящий'),
        ('live', 'Идёт'),
        ('finished', 'Завершён'),
    ]

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name='matches',
        verbose_name='Дисциплина'
    )
    tournament = models.CharField('Турнир', max_length=200)
    opponent = models.CharField('Соперник', max_length=200)
    opponent_logo = models.ImageField('Логотип соперника', upload_to='opponents/', blank=True, null=True)
    date = models.DateTimeField('Дата и время')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='upcoming')
    score_team = models.IntegerField('Счёт Team Spirit', default=0)
    score_opponent = models.IntegerField('Счёт соперника', default=0)
    stream_url = models.URLField('Ссылка на трансляцию', blank=True)
    vod_url = models.URLField('Ссылка на запись', blank=True)

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'
        ordering = ['-date']

    def __str__(self):
        return f'Team Spirit vs {self.opponent} ({self.tournament})'

    @property
    def result(self):
        if self.status == 'finished':
            if self.score_team > self.score_opponent:
                return 'win'
            elif self.score_team < self.score_opponent:
                return 'loss'
            return 'draw'
        return None


class News(models.Model):
    """Новости"""
    CATEGORY_CHOICES = [
        ('announcement', 'Анонс'),
        ('result', 'Результат'),
        ('roster', 'Ростер'),
        ('interview', 'Интервью'),
        ('other', 'Другое'),
    ]

    title = models.CharField('Заголовок', max_length=300)
    slug = models.SlugField('URL', unique=True)
    category = models.CharField('Категория', max_length=20, choices=CATEGORY_CHOICES, default='other')
    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.SET_NULL,
        related_name='news',
        verbose_name='Дисциплина',
        blank=True,
        null=True
    )
    image = models.ImageField('Изображение', upload_to='news/', blank=True, null=True)
    excerpt = models.TextField('Краткое описание', max_length=500)
    content = models.TextField('Содержание')
    is_featured = models.BooleanField('Избранное', default=False)
    is_published = models.BooleanField('Опубликовано', default=True)
    views = models.PositiveIntegerField('Просмотры', default=0)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Partner(models.Model):
    """Партнёры и спонсоры"""
    TIER_CHOICES = [
        ('title', 'Титульный спонсор'),
        ('main', 'Главный партнёр'),
        ('official', 'Официальный партнёр'),
        ('technical', 'Технический партнёр'),
    ]

    name = models.CharField('Название', max_length=200)
    tier = models.CharField('Уровень', max_length=20, choices=TIER_CHOICES)
    logo = models.ImageField('Логотип', upload_to='partners/')
    website = models.URLField('Сайт')
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'
        ordering = ['tier', 'order']

    def __str__(self):
        return f'{self.name} ({self.get_tier_display()})'


class TeamInfo(models.Model):
    """Общая информация о команде"""
    about = models.TextField('О команде')
    founded_year = models.IntegerField('Год основания', default=2015)
    headquarters = models.CharField('Штаб-квартира', max_length=200, default='Москва, Россия')
    total_earnings = models.DecimalField('Общий призовой фонд ($)', max_digits=15, decimal_places=2, default=0)
    logo = models.ImageField('Логотип', upload_to='team/', blank=True, null=True)
    banner = models.ImageField('Баннер', upload_to='team/', blank=True, null=True)
    
    # Социальные сети
    twitter = models.URLField('Twitter', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    youtube = models.URLField('YouTube', blank=True)
    twitch = models.URLField('Twitch', blank=True)
    vk = models.URLField('VK', blank=True)
    telegram = models.URLField('Telegram', blank=True)
    
    contact_email = models.EmailField('Email для связи', blank=True)

    class Meta:
        verbose_name = 'Информация о команде'
        verbose_name_plural = 'Информация о команде'

    def __str__(self):
        return 'Team Spirit Info'
