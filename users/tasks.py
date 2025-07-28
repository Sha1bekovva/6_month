from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta
from .models import UserActionLog

@shared_task
def save_user_action(user_id, action):
    UserActionLog.objects.create(user_id=user_id, action=action, timestamp=timezone.now())

@shared_task
def send_otp_email(user_email, code):
    subject = "Ваш код подтверждения"
    message = f"Здравствуйте! Ваш код подтверждения: {code}"
    from_email = "sajbekovaz33@gmail.com"
    send_mail(subject, message, from_email, [user_email])

@shared_task
def send_daily_report():
    print("Sending daily report...")
    print("Daily report sent")

@shared_task
def clear_old_logs():
    threshold_date = timezone.now() - timedelta(days=30)
    deleted_count, _ = UserActionLog.objects.filter(timestamp__lt=threshold_date).delete()
    print(f"Deleted {deleted_count} old log entries")
