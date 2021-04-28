"""
WSGI config for rtls_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
import site

site.addsitedir('/home/demouser/.virtualenvs/rtls-env/lib/python3.6/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtls_server.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

path = '/var/www/rtls_server'
if path not in sys.path:
    sys.path.append(path)