"""WSGI config for os_hardening project."""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'os_hardening.settings')

application = get_wsgi_application()
