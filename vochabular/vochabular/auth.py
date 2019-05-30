from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as DjangoUser
from django.db import models


class User(DjangoUser):
    LANGUAGE_CHOICES = (
        ('DE', 'Deutsch'),
        ('EN', 'English')
    )

    role = models.CharField(max_length=100)
    language = models.CharField(
        max_length=2, choices=LANGUAGE_CHOICES, default='DE')
    translator_languages = models.CharField(max_length=200)
    event_notifications = models.BooleanField(default=True)
    setup_completed = models.BooleanField(default=False)


def user_handler(payload):
    # TODO(worxli): get a real username here
    username = payload.get('email')
    User = get_user_model()
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        User.objects.create_user(username, username, None)
    return username


def get_key(cert_str):
    try:
        cert_obj = load_pem_x509_certificate(cert_str, default_backend())
    except Exception:
        raise Exception("Could not parse certificate!")
    return cert_obj.public_key()
