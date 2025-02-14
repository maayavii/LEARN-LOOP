# blog/tasks.py
from celery import shared_task
from .models import UserContribution

@shared_task
def calculate_monthly_contributions():
    UserContribution.calculate_monthly_contributions()