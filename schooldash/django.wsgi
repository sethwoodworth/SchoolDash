import os
import sys

sys.path.append('/var/www/SchoolDash/schooldash/')
sys.path.append('/var/www/SchoolDash/schooldash')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler() 
