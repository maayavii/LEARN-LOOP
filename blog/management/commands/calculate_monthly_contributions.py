# blog/management/commands/calculate_monthly_contributions.py
from django.core.management.base import BaseCommand
from blog.models import UserContribution

class Command(BaseCommand):
    help = 'Calculate monthly user contributions'

    def handle(self, *args, **kwargs):
        top_contributors = UserContribution.calculate_monthly_contributions()
        
        self.stdout.write(self.style.SUCCESS('Top 5 Contributors:'))
        for contributor in top_contributors[:5]:
            self.stdout.write(f"{contributor.user.username}: Score {contributor.contribution_score}")