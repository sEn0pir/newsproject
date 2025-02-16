from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            "Добро пожаловать!",
            f"Привет, {instance.username}! Спасибо за регистрацию на News Portal.",
            DEFAULT_FROM_EMAIL,
            [instance.email],
        )
