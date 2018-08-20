import os

from whitenoise import WhiteNoise

from django.core.wsgi import get_wsgi_application
from .settings.production import STATIC_ROOT, STATIC_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

application = get_wsgi_application()
application = WhiteNoise(application, root=STATIC_ROOT, prefix=STATIC_URL)
