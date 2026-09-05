import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'psb_pondok.settings_production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

