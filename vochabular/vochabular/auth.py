from django.contrib.auth import get_user_model

def user_handler(payload):
    # TODO(worxli): get a readl username here
    username = payload.get('email')
    User = get_user_model()
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        User.objects.create_user(username, username, None)
    return username
