import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'lyceum_django_education_project.settings'
)

application = get_wsgi_application()
