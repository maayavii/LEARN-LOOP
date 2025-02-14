from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


User = get_user_model()
class Post(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name="blogpost", blank=True)
    saves = models.ManyToManyField(User, related_name="blogsave", blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_saves(self):
        return self.saves.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})


# models.py
class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/')
    uploaded_at = models.DateTimeField(default=timezone.now)

class PostVideo(models.Model):
    post = models.ForeignKey(Post, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='post_videos/')
    uploaded_at = models.DateTimeField(default=timezone.now)

class PostDocument(models.Model):
    post = models.ForeignKey(Post, related_name='documents', on_delete=models.CASCADE)
    document = models.FileField(upload_to='post_documents/')
    uploaded_at = models.DateTimeField(default=timezone.now, )
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="blogcomment", blank=True)
    reply = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE)
    
    # Media fields
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)
    video = models.FileField(upload_to='comment_videos/', blank=True, null=True)
    voice = models.FileField(upload_to='comment_voice/', blank=True, null=True)
    
    # New fields for reporting
    reported_by = models.ManyToManyField(User, related_name='reported_comments', blank=True)
    is_hidden = models.BooleanField(default=False)
    
    def total_clikes(self):
        return self.likes.count()
    
    def total_reports(self):
        return self.reported_by.count()
    
    def __str__(self):
        return '%s - %s - %s' % (self.post.title, self.name, self.id)
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"pk": self.pk})
    
    def has_media(self):
        return bool(self.image or self.video or self.voice)

class CommentReport(models.Model):
    REPORT_REASONS = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('other', 'Other')
    ]
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    details = models.TextField(blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['comment', 'reported_by']
    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    total_posts = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    contribution_score = models.FloatField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    
    def __str__(self):
        return f"{self.user.username} - Contribution ({self.period_start.date()} to {self.period_end.date()})"
    
    @classmethod
    def calculate_monthly_contributions(cls):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=28)
        
        users = User.objects.all()
        for user in users:
            # Calculate total posts by the user
            total_posts = Post.objects.filter(
                author=user, 
                date_posted__range=[start_date, end_date]
            ).count()
            
            # Calculate total comments on all posts
            total_comments = Comment.objects.filter(
                post__author=user, 
                date_added__range=[start_date, end_date]
            ).count()
            
            # Scoring logic: 10 points per post, 5 points per comment
            contribution_score = (
                total_posts * 10 +   # 10 points per post
                total_comments * 5   # 5 points per comment
            )
            
            contribution, created = cls.objects.get_or_create(
                user=user,
                period_start=start_date,
                period_end=end_date,
                defaults={
                    'total_posts': total_posts,
                    'total_comments': total_comments,
                    'contribution_score': contribution_score
                }
            )
            
            if not created:
                contribution.total_posts = total_posts
                contribution.total_comments = total_comments
                contribution.contribution_score = contribution_score
                contribution.save()
        
        return cls.objects.filter(
            period_start=start_date, 
            period_end=end_date
        ).order_by('-contribution_score')
    
    class Meta:
        unique_together = ['user', 'period_start', 'period_end']
        ordering = ['-contribution_score']