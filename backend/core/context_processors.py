"""
Контекстные процессоры для глобального контекста шаблонов
"""

from .models import TeamInfo


def team_info(request):
    """Добавляет информацию о команде в глобальный контекст шаблонов"""
    return {
        'team_info_global': TeamInfo.objects.first()
    }
