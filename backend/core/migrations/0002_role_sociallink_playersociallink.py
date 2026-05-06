# Generated migration for Role, SocialLink, and PlayerSocialLink models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # Create Role model
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(help_text='Например: carry, support, coach', unique=True, verbose_name='Код')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки')),
            ],
            options={
                'verbose_name': 'Роль',
                'verbose_name_plural': 'Роли',
                'ordering': ['order', 'name'],
            },
        ),
        # Create SocialLink model
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('platform', models.CharField(choices=[
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
                ], max_length=20, verbose_name='Платформа')),
                ('icon_class', models.CharField(blank=True, help_text='Опционально: класс иконки FontAwesome или другой', max_length=100, verbose_name='CSS класс иконки')),
            ],
            options={
                'verbose_name': 'Тип социальной сети',
                'verbose_name_plural': 'Типы социальных сетей',
                'ordering': ['name'],
            },
        ),
        # Create PlayerSocialLink model
        migrations.CreateModel(
            name='PlayerSocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[
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
                ], max_length=20, verbose_name='Платформа')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('username', models.CharField(blank=True, help_text='Опционально: ник на платформе', max_length=100, verbose_name='Имя пользователя')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='core.player', verbose_name='Игрок')),
            ],
            options={
                'verbose_name': 'Соц. сеть игрока',
                'verbose_name_plural': 'Соц. сети игроков',
                'unique_together': {('player', 'platform')},
            },
        ),
        # Remove old social fields from Player
        migrations.RemoveField(
            model_name='player',
            name='twitch',
        ),
        migrations.RemoveField(
            model_name='player',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='player',
            name='instagram',
        ),
        # Change role field from CharField to ForeignKey
        migrations.RemoveField(
            model_name='player',
            name='role',
        ),
        migrations.AddField(
            model_name='player',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='players', to='core.role', verbose_name='Роль'),
        ),
    ]
