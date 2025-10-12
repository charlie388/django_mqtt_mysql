from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        import myapp.signals

# apps.py 或 signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def stamp_session_device(sender, user, request, **kwargs):
    s = request.session
    s['ua'] = request.META.get('HTTP_USER_AGENT', '')[:255]
    s.save()
