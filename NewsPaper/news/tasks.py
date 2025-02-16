from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.conf import settings
from .models import Post, Category

@shared_task
def send_weekly_newsletter():
    """Отправка еженедельного списка новостей подписчикам"""
    last_week = now() - timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        posts = Post.objects.filter(category=category, created_at__gte=last_week)
        if not posts.exists():
            continue

        subject = f"Еженедельная подборка новостей: {category.name}"
        message = "\n\n".join([f"{post.title} - {post.get_absolute_url()}" for post in posts])
        emails = [user.email for user in subscribers]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, emails)

    return "Рассылка завершена!"
