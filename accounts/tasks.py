from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser

@shared_task
def delete_inactive_users():
    limit = timezone.now() - timedelta(days=30)
    deleted, _ = CustomUser.objects.filter(
        is_active=False,
        date_joined__lt=limit
    ).delete()
    return f"Deleted {deleted} inactive users"

@shared_task
def deactivate_expired_products():
    from products.models import Product
    Product.objects.filter(is_active=True, expires_at__lt=timezone.now()).update(is_active=False)

@shared_task
def send_welcome_email(email):
    from django.core.mail import send_mail

    send_mail(
        subject='Добро пожаловать',
        message='Вы успешно зарегистрировались.',
        from_email='noreply@myproject.com',
        recipient_list=[email],
        fail_silently=False,
    )
