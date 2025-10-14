from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils import timezone
from .models import UserSession

def login_handler(sender, request, user, **kwargs):
    UserSession.objects.create(user=user, login_time=timezone.now())

def logout_handler(sender, request, user, **kwargs):
    try:
        session = UserSession.objects.filter(user=user, logout_time__isnull=True).latest('login_time')
        session.logout_time = timezone.now()
        session.save()
    except UserSession.DoesNotExist:
        pass

user_logged_in.connect(login_handler)
user_logged_out.connect(logout_handler)
