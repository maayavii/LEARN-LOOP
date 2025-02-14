from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.
from django.db import models
from django.conf import settings

class Meeting(models.Model):
    title = models.CharField(max_length=200)
    channel_name = models.CharField(max_length=100, unique=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.channel_name}"

    def get_join_url(self):
        from django.urls import reverse
        return reverse('agora_view', kwargs={'channel': self.channel_name})

    def end_meeting(self):
        self.is_active = False
        self.is_ended = True
        self.ended_at = timezone.now()
        self.save()