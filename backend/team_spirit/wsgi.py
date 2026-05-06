"""
WSGI config for Team Spirit project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_spirit.settings')
application = get_wsgi_application()
