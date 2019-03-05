"""
Django settings for vochabular project deployed on heroku.
"""

from vochabular.settings import *
import django_heroku

# Activate Django-Heroku
django_heroku.settings(locals())
