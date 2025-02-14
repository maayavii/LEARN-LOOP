from django.db import models
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
""" Model for User Profile """

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.utils.encoding import force_str  # Replace force_text
from ckeditor.fields import RichTextField
# Add these at the top with your other imports
from django.core.validators import URLValidator, MaxLengthValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    following = models.ManyToManyField(User, related_name="following", blank=True)
    friends = models.ManyToManyField(User, related_name='my_friends', blank=True)
    posts = models.JSONField(default=list, blank=True)  # Storing posts as a list of dictionaries
    bio = models.TextField(
        blank=True,
        null=True,
        max_length=350,
        validators=[MaxLengthValidator(350)]
    )
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Add social media fields
    github = models.URLField(
        max_length=200, 
        blank=True, 
        null=True,
        validators=[URLValidator()]
    )
    linkedin = models.URLField(
        max_length=200, 
        blank=True, 
        null=True,
        validators=[URLValidator()]
    )
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        default='default.jpg',
        upload_to='profile_pics',
        blank=True,
        null=True
    )
    
    buy_me_coffee = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Buy Me a Coffee Link",
        help_text="Your Buy Me a Coffee profile link"
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def post_count(self):
        """Property to get the count of posts made by this user."""
        return self.posts.count()

# Choices for Relationship Status
STATUS_CHOICES = (
    ('send','sent'),
    ('accepted','accepted'),
    ('cancelled', 'cancelled'),
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friend_receiver')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)  # max_length should be 9
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"
